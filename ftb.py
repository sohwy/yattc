"""
Family tax benefit
"""

import pandas as pd
import numpy as np
import time
from base_policy import BasePolicy
from numba import jit


class FamilyTaxBenefit(BasePolicy):

    def __init__(self):
        self.ftba_max_amt = ftba_max_amt
        self.ftba_method1_apportion = ftba_method1_apportion

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


class FamilyTaxBenefitDefault(FamilyTaxBenefit):
    pass


class FamilyTaxBenefitReform(FamilyTaxBenefit):
    pass


class FamilyTaxBenefit2013Q3(FamilyTaxBenefit):
    pass


class FamilyTaxBenefit2015Q1(FamilyTaxBenefit):
    def __init__(self):
        super().__init__()
        self.ftba_max_amt = ftba_max_amt_np


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

@jit(nopython=True)
def ftba_max_amt_s(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt,
                   ftba_es_rt, nbs_rt, ra_max_amt, max_rate=True):
    """
    ftb_kids: ftb kids
    ftba_std_rt: ftba standard rate parameter array
    ftba_es_rt: ftba energy supplement parameter array
    nbs_rt: newborn supplement rate parameter array
    ra_max_amt: rent assistance maximum amount
    """
    # set the standard rate and energy supplement rate depending on
    # whether we are calculating the maximum rate or base rate
    ftba_std_rt1 = ftba_std_rt[1 * max_rate]
    ftba_std_rt2 = ftba_std_rt[2 * max_rate]
    ftba_std_rt3 = ftba_std_rt[3 * max_rate]
    ftba_es_rt1 = ftba_es_rt[1 * max_rate]
    ftba_es_rt2 = ftba_es_rt[2 * max_rate]
    ftba_es_rt3 = ftba_es_rt[3 * max_rate]
    nbs_rt_ = nbs_rt[0]
    # standard rate
    ftba_std_max_amt = (ftb_0_12_ch * ftba_std_rt1
                        + ftb_13_15_ch * ftba_std_rt2
                        + ftb_16_19_sec_ch * ftba_std_rt3)
    # energy supplement
    ftba_es_max_amt = (ftb_0_12_ch * ftba_es_rt1
                       + ftb_13_15_ch * ftba_es_rt2
                       + ftb_16_19_sec_ch * ftba_es_rt3)
    # newborn supplement
    nbs_max_amt = nbs_rt_ * (365/91)
    # return ftba maximum amount
    ftba_max_amt = (ftba_std_max_amt
                    + ftba_es_max_amt
                    + nbs_max_amt
                    + ra_max_amt)
    return ftba_max_amt

@jit(nopython=True)
def foo(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt,
        nbs_rt, ra_max_amt, max_rate=True):
    res = np.zeros(ftb_0_12_ch.size)
    for i in range(ftb_0_12_ch.size):
        res[i] = ftba_max_amt_s(ftb_0_12_ch[i], ftb_13_15_ch[i], ftb_16_19_sec_ch[i],
                                ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt[i], max_rate)
    return res
        


def ftba_maint_inc_test_py(maint_inc, ftba_mifa, mifa_addon, mifa_tpr,
                           ftype, minc_recipients, child_supp_ch):
    """
    maint_inc_recipients: number of maintenance income recipients
    child_supp_ch: number of child support children
    """
    minc_reduction = np.zeros_like(maint_inc)
    for i in range(maint_inc.size):
        if maint_inc[i] <= 0 or minc_recipients[i] == 0:
            minc_reduction[i] = 0
        else:
            idx = ftype[i] * minc_recipients[i]
            mifa_base = ftba_mifa[idx]
            mifa_add = mifa_addon[idx]
            mifa = mifa_base + mifa_add * child_supp_ch[i]
            minc_reduction[i] = min(mifa,
                                    max(0, (maint_inc[i] - mifa) * mifa_tpr))
    return minc_reduction


@jit(nopython=True)
def ftba_maint_inc_test(maint_inc, ftba_mifa, mifa_addon, mifa_tpr,
                        ftype, minc_recipients, child_supp_ch):
    """
    maint_inc_recipients: number of maintenance income recipients
    child_supp_ch: number of child support children
    res: deduction due to maintenance income test
    """
    res = np.zeros_like(maint_inc)
    for i in range(maint_inc.size):
        if maint_inc[i] <= 0 or minc_recipients[i] == 0:
            res[i] = 0
        else:
            idx = ftype[i] * minc_recipients[i]
            mifa_base = ftba_mifa[idx]
            mifa_add = mifa_addon[idx]
            mifa = mifa_base + mifa_add * child_supp_ch[i]
            res[i] = min(mifa, max(0, (maint_inc[i] - mifa) * mifa_tpr[0]))
    return res


def ftba_maint_inc_test_np(maint_inc, ftba_mifa, mifa_addon, mifa_tpr,
                           ftype, minc_recipients, child_supp_ch):
    """
    maint_inc_recipients: number of maintenance income recipients
    child_supp_ch: number of child support children
    """
    # calculate mifa base amount
    idx = ftype * minc_recipients
    ftba_mifa0 = np.repeat(np.array(ftba_mifa[0]), ftype.size)
    ftba_mifa1 = np.repeat(np.array(ftba_mifa[1]), ftype.size)
    ftba_mifa2 = np.repeat(np.array(ftba_mifa[2]), ftype.size)
    mifa_add0 = np.repeat(np.array(mifa_addon[0]), ftype.size)
    mifa_add1 = np.repeat(np.array(mifa_addon[1]), ftype.size)
    mifa_add2 = np.repeat(np.array(mifa_addon[2]), ftype.size)
    condlist = [idx == 0, idx == 1, idx == 2]
    mifa_base_choicelist = [ftba_mifa0, ftba_mifa1, ftba_mifa2]
    mifa_add_choicelist = [mifa_add0, mifa_add1, mifa_add2]
    mifa_base = np.select(condlist, mifa_base_choicelist)
    mifa_add = np.select(condlist, mifa_add_choicelist)
    mifa = mifa_base + mifa_add * child_supp_ch
    res = np.minimum(mifa, np.maximum(0, (maint_inc - mifa) * mifa_tpr))
    res = np.where(minc_recipients > 0, res, 0)
    return res


def ftba_inc_test_py(ftb_inc, isp_recipient, free_area):
    """
    Calculate deduction from maximum ftba amount
    ftb_inc: income for family tax benefit purposes
    """
    res = np.zeros(ftb_inc.size)
    for i in range(res.size):
        if isp_recipient[i]:
            res[i] = 0
        else:
            res[i] = ftb_inc[i] - free_area
    return res


# def ftba_calc():
#     for i in range(ftb_inc.size):
#     # calculate under method 1
#         ftba_m1_max_amt = ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
#                                        ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt,
#                                        max_rate=True)
#         maint_inc_dedn = ftba_maint_inc_test(maint_inc, ftba_mifa, mifa_addon,
#                                              mifa_tpr, ftype, minc_recipients,
#                                              child_supp_ch)
#         inc_dedn_m1 = ftba_inc_test_py(ftb_inc, isp_recipient, 52706)
#         method1_amt = ftba_m1_max_amt - maint_inc_dedn - inc_dedn_m1
#         # calculate under method 2 for those with ATI > HIFA
#         if ftb_inc > 94316:
#             ftba_m2_max_amt = ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch,
#                                            ftb_16_19_sec_ch, ftba_std_rt,
#                                            ftba_es_rt, nbs_rt, ra_max_amt)
#             inc_dedn_m2 = ftba_inc_test_py(ftb_inc, isp_recipient, 94316)
#             method2_amt = ftba_m2_max_amt - inc_dedn_m2
#         if method1_amt > method2_amt:
#             res = method1


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


@jit(nopython=True)
def ftba_method1_apportion(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
                           ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt):
    # calculate max rate
    ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
                 ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt)
    # calculate base rate
    ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
                 ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt,
                 max_rate=False)

    # calculate difference between max and base amounts
    # ftba_std_over = ftba_std_max_amt - ftba_std_base_amt
    # ftba_es_over = ftba_es_max_amt - ftba_es_base_amt
    # nbs_over = nbs_base_amt
    # ra_over = ra_max_amt


