"""
Rent assistance class
"""

import pandas as pd
import numpy as np
from base_policy import BasePolicy
from numba import jit


class RentAssistance(BasePolicy):

    def __init__(self):
        self.calc_rent_assistance = calc_rent_assistance

    @staticmethod
    def factory(period):
        if period == pd.Period('2013Q3'):
            return RentAssistance2013Q3()
        elif period == pd.Period('2015Q1'):
            return RentAssistance2015Q1()
        elif period in BasePolicy.DEFAULT_PERIODS_PD:
            return RentAssistanceDefault()
        elif period == 'reform':
            return RentAssistanceReform()
        else:
            raise ValueError('Invalid value for period: {}'.format(period))


class RentAssistanceDefault(RentAssistance):
    pass


class RentAssistanceReform(RentAssistance):
    pass


class RentAssistance2013Q3(RentAssistance):
    pass


class RentAssistance2015Q1(RentAssistance):
    """
    Rent Assistance class for 2015Q1
    use slow calc_rent_assistance function
    """
    def __init__(self):
        self.calc_rent_assistance = calc_rent_assistance_py


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
        min_rent = min_rent_thd[ftype_ra]
        max_rate = max_ra_rate[ftype_ra] if not sharer[i] else \
            max_ra_rate[ftype_ra] * 0.5
        if rent[i] > min_rent:
            ra_amt[i] = max(min(((rent[i] - min_rent) * ra_prop),
                            max_rate), 0)
    return ra_amt


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
