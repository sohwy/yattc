"""
Rent assistance class
"""

import numpy as np
import time
from base_policy import BasePolicy
from numba import jit


class RentAssistance(BasePolicy):

    @staticmethod
    def factory(period):
        if period == '2013Q3':
            return RentAssistance2013Q3()
        elif period in BasePolicy.DEFAULT_PERIODS:
            return RentAssistanceDefault()
        else:
            raise ValueError('Invalid value for period: {}'.format(period))

    @staticmethod
    @jit(nopython=True)
    def calc_rent_assistance2(ftype, ftb_kids, rent, sharer, min_rent_thd,
                             max_ra_rate, ra_prop):
        """
        Calculate rent assistance payable

        ftype: family type
        ftb_kids: number of ftb kids
        rent: fortnightly rent paid
        sharer: whether sharer
        min_rent_thd: minimum rent threshold parameter
        max_ra_rate: maximum rent assistance payable parameter
        ra_prop: proportion of rent paid parameter

        returns
        ra_amt: amount of rent assistance payable
        """
        ra_amt = np.zeros_like(rent)
        for i in range(ftype.size):
            ftype_ra = ftype[i] + 2 * ftb_kids[i]
            min_rent = min_rent_thd[ftype_ra]  # relevant min rent threshold
            max_rate = max_ra_rate[ftype_ra] if not sharer[i] else \
                max_ra_rate[ftype_ra] * 0.5
            if rent[i] > min_rent:
                ra_amt[i] = max(min(((rent[i] - min_rent) * ra_prop),
                                max_rate), 0)
        return ra_amt

    @staticmethod
    @jit(nopython=True)
    def calc_rent_assistance(ftype, ftb_kids, rent, sharer, min_rent_thd,
                             max_ra_rate, ra_prop):
        """
        Calculate rent assistance payable

        ftype: family type
        ftb_kids: number of ftb kids
        rent: fortnightly rent paid
        sharer: whether sharer
        min_rent_thd: minimum rent threshold parameter
        max_ra_rate: maximum rent assistance payable parameter
        ra_prop: proportion of rent paid parameter

        returns
        ra_amt: amount of rent assistance payable
        """
        ra_amt = np.zeros_like(rent)
        for i in range(ftype.size):
            ftype_ra = ftype[i] + 2 * ftb_kids[i]
            min_rent = min_rent_thd[ftype_ra]  # relevant min rent threshold
            max_rate = max_ra_rate[ftype_ra]  # relevant max rent payable
            # if rent payment is less than the minimum rent threshold, no rent
            # assistance is payable
            if rent[i] < min_rent:
                ra_amt[i] = 0
            else:
                if sharer[i]:
                    max_rate *= 0.5
                ra_amt[i] = max(min(((rent[i] - min_rent) * ra_prop),
                                max_rate), 0)
        return ra_amt

    @staticmethod
    def calc_rent_assistance_py(ftype, ftb_kids, rent, sharer, min_rent_thd,
                                max_ra_rate, ra_prop):
        """
        Calculate rent assistance payable (pure python)

        ftype: family type
        ftb_kids: number of ftb kids
        rent: fortnightly rent paid
        sharer: whether sharer
        min_rent_thd: minimum rent threshold parameter
        max_ra_rate: maximum rent assistance payable parameter
        ra_prop: proportion of rent paid parameter

        returns
        ra_amt: amount of rent assistance payable
        """
        ra_amt = np.zeros_like(rent)
        for i in range(ftype.size):
            ftype_ra = ftype[i] + 2 * ftb_kids[i]
            min_rent = min_rent_thd[ftype_ra]  # relevant min rent threshold
            max_rate = max_ra_rate[ftype_ra]  # relevant max rent payable
            # if rent payment is less than the minimum rent threshold, no rent
            # assistance is payable
            if rent[i] < min_rent:
                ra_amt[i] = 0
            else:
                if sharer[i]:
                    max_rate *= 0.5
                ra_amt[i] = max(min(((rent[i] - min_rent) * ra_prop),
                                max_rate), 0)
        return ra_amt


class RentAssistanceDefault(RentAssistance):
    """
    Default Rent Assistance class
    """
    pass

class RentAssistance2013Q3(RentAssistance):
    """
    Rent Assistance class for 2013Q3

    Add: foo method
    """
    def foo(self):
        print(self.__class__.__name__)




z = RentAssistance.factory('2013Q4')
def test_calc(ra_func):
    """
    Test rent assistance calculation functions
    """
    print(30 * '-')
    name = ra_func.__name__
    print('testing {}'.format(name))

    # set up data
    size = int(10**5)
    ftype = np.random.randint(0, 2, size, dtype=np.int8)
    kids = np.random.randint(0, 3, size, dtype=np.int8)
    rent = np.random.choice([0.0, 100, 150, 200, 250, 300, 350, 400], size)
    sharer = np.full(size, True, dtype=bool)
    ra_prop = np.array(0.75)
    min_rent_thd = np.array([117.80, 191.00, 154.84, 229.18, 154.84, 229.18], dtype=np.float64)
    max_ra_rate = np.array([132.2, 124.6, 155.26, 155.26, 175.42, 175.42], dtype=np.float64)

    # check that outputs match
    f1 = z.calc_rent_assistance_py(ftype, kids, rent, sharer, min_rent_thd,
                                 max_ra_rate, ra_prop)
    f2 = ra_func(ftype, kids, rent, sharer, min_rent_thd, max_ra_rate, ra_prop)
    assert np.allclose(f1, f2), 'Results do not match'
    print('Results match')

    # time the function
    times = []
    for i in range(5):
        t0 = time.time()
        ra_func(ftype, kids, rent, sharer, min_rent_thd, max_ra_rate, ra_prop)
        t1 = time.time()
        times.append(t1 - t0)
    print('Execution time: {:.2g} sec'.format(np.median(times)))

print(z.calc_rent_assistance.__name__)

test_calc(z.calc_rent_assistance_py)
test_calc(z.calc_rent_assistance)
test_calc(z.calc_rent_assistance2)

size = int(10**5)
ftype = np.random.randint(0, 2, size, dtype=np.int8)
kids = np.random.randint(0, 3, size, dtype=np.int8)
rent = np.random.choice([0.0, 100, 150, 200, 250, 300, 350, 400], size)
sharer = np.full(size, False, dtype=bool)
ra_prop = np.array(0.75)
min_rent_thd = np.array([117.80, 191.00, 154.84, 229.18, 154.84, 229.18], dtype=np.float64)
max_ra_rate = np.array([132.2, 124.6, 155.26, 155.26, 175.42, 175.42], dtype=np.float64)
ra_amt = np.zeros_like(rent)

# @jit(nopython=True)
def calc_rent_assistance(ftype, ftb_kids, rent, sharer, min_rent_thd,
                         max_ra_rate, ra_prop):
    """
    Calculate rent assistance payable

    ftype: family type
    ftb_kids: number of ftb kids
    rent: fortnightly rent paid
    sharer: whether sharer
    min_rent_thd: minimum rent threshold parameter
    max_ra_rate: maximum rent assistance payable parameter
    ra_prop: proportion of rent paid parameter

    returns
    ra_amt: amount of rent assistance payable
    """
    ra_amt = np.zeros_like(rent)
    ftype_ra = ftype + 2 * ftb_kids
    for i in range(ftype.size):
        # ftype_ra = ftype[i] + 2 * ftb_kids[i]
        min_rent = min_rent_thd[ftype_ra[i]]  # relevant min rent threshold
        max_rate = max_ra_rate[ftype_ra[i]]  # relevant max rent payable
        # if rent payment is less than the minimum rent threshold, no rent
        # assistance is payable
        if rent[i] < min_rent:
            ra_amt[i] = 0
        else:
            if sharer[i]:
                max_rate *= 0.5
            ra_amt[i] = max(min(((rent[i] - min_rent) * ra_prop),
                            max_rate), 0)
    return ra_amt


