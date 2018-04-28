"""
Family tax benefit
"""

import pandas as pd
import numpy as np
import time
from base_policy import BasePolicy
from numba import jit


class FamilyTaxBenefit(BasePolicy):

    @staticmethod
    def factory(period):
        if period == pd.Period('2013Q3'):
            return FamilyTaxBenefit2013Q3()
        elif period == pd.Period('2015Q1'):
            return FamilyTaxBenefit2015Q1()
        elif period in BasePolicy.DEFAULT_PERIODS_PD:
            return FamilyTaxBenefitDefault()
        elif period == 'reform':
            return FamilyTaxBenefitReform()
        else:
            raise ValueError('Invalid value for period: {}'.format(period))


    @staticmethod
    def ftba_max_amt_np2(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
                         ftba_es_rt, nbs_rt, ra_max_amt, max_rate=True):
        """
        ftb_kids: ftb kids
        ftba_std_rt: ftba standard rate parameter array
        ftba_es_rt: ftba energy supplement parameter array
        nbs_rt: newborn supplement rate parameter array
        ra_max_amt: rent assistance maximum amount
        """
        ftba_ch = np.array((ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch))
        if not max_rate:
            ftba_std_rt = np.repeat(ftba_std_rt[0], 4)
            ftba_es_rt = np.repeat(ftba_es_rt[0], 5)
        ftba_std_rt = ftba_std_rt.reshape(4, 1)
        ftba_es_rt = ftba_es_rt.reshape(5, 1)
        # standard rate
        ftba_std_max_amt = ftba_ch * ftba_std_rt[1:4]
        # energy supplement
        ftba_es_max_amt = ftba_ch * ftba_es_rt[1:4]
        # newborn supplement
        nbs_max_amt = nbs_rt * (365/91)
        # return ftba maximum amount
        return np.array((ftba_std_max_amt, ftba_es_max_amt, nbs_max_amt, ra_max_amt))

    @staticmethod
    def ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
                        ftba_es_rt, nbs_rt, ra_max_amt, max_rate=True):
        """
        ftb_kids: ftb kids
        ftba_std_rt: ftba standard rate parameter array
        ftba_es_rt: ftba energy supplement parameter array
        nbs_rt: newborn supplement rate parameter array
        ra_max_amt: rent assistance maximum amount
        """
        if not max_rate:
            ftba_std_rt = np.repeat(ftba_std_rt[0], 4)
            ftba_es_rt = np.repeat(ftba_es_rt[0], 5)
        # standard rate
        ftba_std_max_amt = (ftb_0_12_ch * ftba_std_rt[1]
                            + ftb_13_15_ch * ftba_std_rt[2]
                            + ftb_16_19_sec_ch * ftba_std_rt[3])
        # energy supplement
        ftba_es_max_amt = (ftb_0_12_ch * ftba_es_rt[1]
                           + ftb_13_15_ch * ftba_es_rt[2]
                           + ftb_16_19_sec_ch * ftba_es_rt[3])
        # newborn supplement
        nbs_max_amt = nbs_rt * (365/91)
        # return ftba maximum amount
        ftba_max_amt = ftba_std_max_amt + ftba_es_max_amt + nbs_max_amt + ra_max_amt
        return ftba_max_amt


    @staticmethod
    def ftba_max_amt_py(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
                        ftba_es_rt, nbs_rt, ra_max_amt, max_rate=True):
        """
        ftb_kids: ftb kids
        ftba_std_rt: ftba standard rate parameter array
        ftba_es_rt: ftba energy supplement parameter array
        nbs_rt: newborn supplement rate parameter array
        ra_max_amt: rent assistance maximum amount
        """
        ftba_max_amt = np.zeros(ra_max_amt.size)
        ftba_std_max_amt = np.zeros(ra_max_amt.size)
        ftba_es_max_amt = np.zeros(ra_max_amt.size)
        nbs_max_amt = np.zeros(ra_max_amt.size)
        if not max_rate:
            ftba_std_rt = np.repeat(ftba_std_rt[0], 4)
            ftba_es_rt = np.repeat(ftba_es_rt[0], 5)
        for i in range(ftb_0_12_ch.size):
            # standard rate
            ftba_std_max_amt[i] = (ftb_0_12_ch[i] * ftba_std_rt[1]
                                   + ftb_13_15_ch[i] * ftba_std_rt[2]
                                   + ftb_16_19_sec_ch[i] * ftba_std_rt[3])
            # energy supplement
            ftba_es_max_amt[i] = (ftb_0_12_ch[i] * ftba_es_rt[1]
                                  + ftb_13_15_ch[i] * ftba_es_rt[2]
                                  + ftb_16_19_sec_ch[i] * ftba_es_rt[3])
            # newborn supplement
            nbs_max_amt[i] = nbs_rt * (365/91)
            # return ftba maximum amount
            ftba_max_amt[i] = (ftba_std_max_amt[i]
                               + ftba_es_max_amt[i]
                               + nbs_max_amt[i]
                               + ra_max_amt[i])
        return ftba_max_amt

    @staticmethod
    @jit(nopython=True)
    def ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
                     ftba_es_rt, nbs_rt, ra_max_amt, max_rate=True):
        """
        ftb_kids: ftb kids
        ftba_std_rt: ftba standard rate parameter array
        ftba_es_rt: ftba energy supplement parameter array
        nbs_rt: newborn supplement rate parameter array
        ra_max_amt: rent assistance maximum amount
        """
        ftba_max_amt = np.zeros(ra_max_amt.size)
        ftba_std_max_amt = np.zeros(ra_max_amt.size)
        ftba_es_max_amt = np.zeros(ra_max_amt.size)
        nbs_max_amt = np.zeros(ra_max_amt.size)
        # set the standard rate and energy supplement rate depending on
        # whether we are calculating the maximum rate or base rate
        ftba_std_rt1 = ftba_std_rt[1 * max_rate]
        ftba_std_rt2 = ftba_std_rt[2 * max_rate]
        ftba_std_rt3 = ftba_std_rt[3 * max_rate]
        ftba_es_rt1 = ftba_es_rt[1 * max_rate]
        ftba_es_rt2 = ftba_es_rt[2 * max_rate]
        ftba_es_rt3 = ftba_es_rt[3 * max_rate]
        for i in range(ftb_0_12_ch.size):
            # standard rate
            ftba_std_max_amt[i] = (ftb_0_12_ch[i] * ftba_std_rt1
                                   + ftb_13_15_ch[i] * ftba_std_rt2
                                   + ftb_16_19_sec_ch[i] * ftba_std_rt3)
            # energy supplement
            ftba_es_max_amt[i] = (ftb_0_12_ch[i] * ftba_es_rt1
                                  + ftb_13_15_ch[i] * ftba_es_rt2
                                  + ftb_16_19_sec_ch[i] * ftba_es_rt3)
            # newborn supplement
            nbs_max_amt[i] = nbs_rt[0] * (365/91)
            # return ftba maximum amount
            ftba_max_amt[i] = (ftba_std_max_amt[i]
                               + ftba_es_max_amt[i]
                               + nbs_max_amt[i]
                               + ra_max_amt[i])
        return ftba_max_amt
        # return ftba_std_max_amt, ftba_es_max_amt, nbs_max_amt


    def ftba_method2(ftba_std_amt, ftba_es_amt, nbs_amt, ftba_sup_rt,
                      ftba_tpr, ftba_high_inc_thr, ftb_inc, ftba_supp_inc_lmt):
        # calculate base rate, this the maximum rate under method 2
        base_rate = ftba_std_amt + ftba_es_amt + nbs_amt
        # calculate reduction
        income_deduction = (ftb_inc - ftba_high_inc_thr) * ftba_tpr
        ftba_amt = base_rate - income_deduction
        # calculate EOY FTBA supplement
        if ftb_inc > ftba_supp_inc_lmt:
            ftba_sup_amt = 0
        else:
            ftba_sup_amt = min(ftba_sup_rt, max(0, ftba_amt + ftba_sup_rt))
        return ftba_amt, ftba_sup_amt

    @staticmethod
    @jit(nopython=True)
    def ftba_method1_apportion(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
                               ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt):
        # calculate max rate
        ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch,
                                      ftb_16_19_sec_ch, ftba_std_rt,
                                      ftba_es_rt, nbs_rt, ra_max_amt)
        # calculate base rate
        ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch,
                                      ftb_16_19_sec_ch, ftba_std_rt,
                                      ftba_es_rt, nbs_rt, ra_max_amt,
                                      max_rate=False)

    def ftba_method2_apportion():
        pass


class FamilyTaxBenefitDefault(FamilyTaxBenefit):
    """
    Default Rent Assistance class
    """
    pass


class FamilyTaxBenefitReform(FamilyTaxBenefit):
    """
    Reform Rent Assistance class
    """
    pass


class FamilyTaxBenefit2013Q3(FamilyTaxBenefit):
    """
    Rent Assistance class for 2013Q3

    Add: foo method
    """
    def foo(self):
        print(self.__class__.__name__)


class FamilyTaxBenefit2015Q1(FamilyTaxBenefit):
    """
    Rent Assistance class for 2015Q1

    Add: foo method
    """
    def foo(self):
        print(self.__class__.__name__)

z = FamilyTaxBenefitDefault()

size = int(10**5)
ftb_0_12_ch = np.random.randint(0, 3, size, dtype=np.int8)
ftb_13_15_ch = np.random.randint(0, 3, size, dtype=np.int8)
ftb_16_19_sec_ch = np.random.randint(0, 3, size, dtype=np.int8)
ftba_std_rt = np.array([1529.35, 4766.90, 6201.35, 6201.35], dtype=np.float64)
ftba_es_rt = np.array([36.50, 91.25, 116.80, 116.80, 36.50], dtype=np.float64)
nbs_rt = np.array([1595.23], dtype=np.float64)
ra_max_amt = np.random.randint(0, 500, size)
print(ra_max_amt.size)
print(ftb_0_12_ch)
print(ftb_13_15_ch)
print(ftba_std_rt)
print(ftba_es_rt)
print(ra_max_amt)

print(z.ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt))
print(z.ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt))

print(z.ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False))
print(z.ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False))

ftba_max_amount = z.ftba_max_amt_np(2, 1, 1, ftba_std_rt, ftba_es_rt, 0, 0, max_rate=False)
ftba_max_amount2 = z.ftba_max_amt_np(2, 1, 1, np.repeat(ftba_std_rt[0], 4), np.repeat(ftba_es_rt[0], 4), 0, 0, max_rate=False)
print(ftba_max_amount)
print(ftba_max_amount2)

z.ftba_method1_apportion(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt)

def test_calc(func):
    """
    Test functions
    """
    print(30 * '-')
    name = func.__name__
    print('testing {}'.format(name))

    # set up data
    size = int(10**5)
    ftb_0_12_ch = np.random.randint(0, 3, size, dtype=np.int8)
    ftb_13_15_ch = np.random.randint(0, 3, size, dtype=np.int8)
    ftb_16_19_sec_ch = np.random.randint(0, 3, size, dtype=np.int8)
    ftba_std_rt = np.array([1529.35, 4766.90, 6201.35, 6201.35], dtype=np.float64)
    ftba_es_rt = np.array([36.50, 91.25, 116.80, 116.80, 36.50], dtype=np.float64)
    nbs_rt = np.array([1595.23], dtype=np.float64)
    ra_max_amt = np.random.randint(0, 500, size)

    # check that outputs match
    f1 = z.ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
                           ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False)
    f2 = func(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
              ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False)
    assert np.allclose(f1, f2), 'Results do not match'
    print('Results match')

    # time the function
    times = []
    for i in range(5):
        t0 = time.time()
        func(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
             ftba_es_rt, nbs_rt, ra_max_amt)
        t1 = time.time()
        times.append(t1 - t0)
    print('Execution time: {:.5g} sec'.format(np.median(times)))

test_calc(z.ftba_max_amt_np)
test_calc(z.ftba_max_amt)
# test_calc(z.ftba_max_amt_py)
