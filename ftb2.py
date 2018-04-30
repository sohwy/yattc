import numpy as np
import numba
obs = np.empty(10**5)


@numba.jit(nopython=True)
def ftba_std_amt_calc(ch_0012, ch_1315, ch_1619_sec, ftba_rt, use_max=True):
    """
    Calculate ftba standard rate maximum amount
    Also used to calculate ftba energy supplement amount

    Arguments:

        Variables:
            ch_0012: number of children 0-12
            ch_1315: number of children 13-15
            ch_1619_sec: number of children 16-19 in secondary school

        Parameters:
            ftba_rt: ftba rate (i.e. standard rate, energy supplement rate)

    Returns:
    ftba standard or energy supplement maximum amount
    """
    ftba_max_std_amt = (ch_0012 * ftba_rt[1 * use_max]
                        + ch_1315 * ftba_rt[2 * use_max]
                        + ch_1619_sec * ftba_rt[3 * use_max])
    return ftba_max_std_amt


@numba.jit(nopython=True)
def nbs_amt_calc(ch_00, ch_dep, nbs_rt):
    """
    Calculate newborn supplement amount
    Arguments:
        Variables:
            ch_00: number of children aged 0-1
            ch_dep: number of dependent children
        Parameters:
            nbs_rt: newborn supplement rate
    Returns:
    newborn supplement maximum amount
    """
    # no newborns or dependent children
    if ch_00 == 0 or ch_dep == 0:
        return 0
    # at least 1 newborn
    elif ch_00 > 1:
        return ch_00 * nbs_rt[1] * 365 / 91  # assign higher rate
    elif ch_00 == 1 and ch_dep == 1:
        return nbs_rt[1] * 365 / 91  # assign higher rate
    else:
        return nbs_rt[0] * 365 / 91  # assign lower rate


@numba.jit(nopython=True)
def ftba_inc_test_calc(ftb_inc, ftba_tpr, ftba_free_area):
    """
    Calculate income test reduction for FTBA
    Arguments:
        Variables:
            ftb_inc: income for ftb purposes
        Parameters:
            ftba_tpr: ftba income test taper rate
            ftba_free_area: ftba free area
    Returns:
    ftba reduction due to income test
    """
    if ftb_inc < ftba_free_area:
        return 0
    else:
        return (ftb_inc - ftba_free_area) * ftba_tpr


def maint_inc_test_calc(ch_maint, maint_inc_p1, maint_inc_p2,
                        maint_inc_base, maint_inc_add, maint_inc_tpr):
    """
    Calculate maintenance income test reduction
    Arguments:
        Variables:
            ch_maint: number of child support children
            maint_inc_p1: person 1 maintenance income
            maint_inc_p2: person 2 maintenance income
        Parameters:
            maint_inc_base: maintenance income base free area
            maint_inc_add: maintenance income free area addon per child
                maint_inc_tpr: ftba maintenance income test taper rate
        Returns:
        ftba reduction due to maintenance income test
        """
    maint_inc = maint_inc_p1 + maint_inc_p2
    if (maint_inc <= 0) or (ch_maint == 0):
        return 0
    # calculate MIFA as the base amount and any additional amount depending
    # on the number of child support children
    recipients = (maint_inc_p1 > 0) + (maint_inc_p2 > 0)
    mifa = maint_inc_base[recipients] + ch_maint * maint_inc_add
    # reduction is based on excess amount of maintenance income over MIFA
    maint_inc_redn = (maint_inc - mifa) * maint_inc_tpr
    return maint_inc_redn


def ftba_amt_calc(ftb_inc, ch_0012, ch_1315, ch_1619_sec, ch_00, ch_dep, ra_max_amt, ch_maint, maint_inc_p1, maint_inc_p2,
                  ftba_std_rt, ftba_es_rt, ftba_supp, ftba_supp_inc_lmt, nbs_rt, ftba_tpr, ftba_free_area, maint_inc_base, maint_inc_add, maint_inc_tpr):
    """
    Calculate ftba amount
    Arguments:
        Variables:
            ftb_inc: income for ftb purposes
            ch_0012: number of children 0-12
            ch_1315: number of children 13-15
            ch_1619_sec: number of children 16-19 in secondary school
            ch_00: number of children aged 0-1
            ch_dep: number of dependent children
            ra_max_amt: rent assistance amount before income testing
            ch_maint: number of child support children
            maint_inc_p1: person 1 maintenance income
            maint_inc_p2: person 2 maintenance income
        Parameters:
            ftba_std_rt: ftba standard rate
            ftba_es_rt: ftba energy supplement rate
            ftba_supp: ftba end of year supplement
            ftba_supp_inc_lmt: income limit to receive ftba_supp
            nbs_rt: newborn supplement rate
            ftba_tpr: ftba income test taper rate
            ftba_free_area: ftba free areas
            maint_inc_base: maintenance income base free area
            maint_inc_add: maintenance income free area addon per child
            maint_inc_tpr: ftba maintenance income test taper rate
    Returns:
    FTBA amount numpy array
    Iterate over all observations
    """
    # initialise output arrays
    m1_std_max = np.zeros(obs.size)
    m2_std_max = np.zeros(obs.size)
    m1_es_max = np.zeros(obs.size)
    m2_es_max = np.zeros(obs.size)
    supp_amt = np.zeros(obs.size)
    nbs_amt = np.zeros(obs.size)
    m1_inc_test_redn = np.zeros(obs.size)
    m2_inc_test_redn = np.zeros(obs.size)
    maint_inc_test_redn = np.zeros(obs.size)
    m1_max = np.zeros(obs.size)
    m2_max = np.zeros(obs.size)
    m1_amt = np.zeros(obs.size)
    m2_amt = np.zeros(obs.size)
    ftba_amt = np.zeros(obs.size)
    # precalculate constants

    for i in range(obs.size):
        # method 1 calculation
        # standard rate
        m1_std_max[i] = ftba_std_amt_calc(ch_0012[i], ch_1315[i],
                                          ch_1619_sec[i], ftba_std_rt)
        # energy supplement
        m1_es_max[i] = ftba_std_amt_calc(ch_0012[i], ch_1315[i],
                                         ch_1619_sec[i], ftba_es_rt)
        # newborn supplement
        nbs_amt[i] = nbs_amt_calc(ch_00[i], ch_dep[i], nbs_rt)
        # EOY supplement
        if ftb_inc[i] <= ftba_supp_inc_lmt:
            supp_amt[i] = ftba_supp * (ch_0012[i]
                                       + ch_1315[i]
                                       + ch_1619_sec[i])
        # calculate method 1 maximum amount
        m1_max[i] = (m1_std_max[i]
                     + m1_es_max[i]
                     + nbs_amt[i]
                     + supp_amt[i]
                     + ra_max_amt[i])

        # income test reduction amount
        m1_inc_test_redn[i] = ftba_inc_test_calc(ftb_inc, ftba_tpr[0],
                                                 ftba_free_area[0])
        # maintenance income test reduction
        maint_inc_test_redn[i] = maint_inc_test_calc(ch_maint[i],
                                                     maint_inc_p1[i],
                                                     maint_inc_p2[i],
                                                     maint_inc_base,
                                                     maint_inc_add,
                                                     maint_inc_tpr)
        # calculate method 1 amount
        m1_amt[i] = max(0, m1_max[i] - m1_inc_test_redn[i] - maint_inc_test_redn[i])
        # method 2 calculation (only if income > hifa)
        if ftb_inc[i] >= ftba_free_area[1]:
            # standard rate at base
            m2_std_max[i] = ftba_std_amt_calc(ch_0012[i],
                                              ch_1315[i],
                                              ch_1619_sec[i],
                                              ftba_std_rt,
                                              use_max=False)
            # energy supplement at base
            m2_es_max[i] = ftba_std_amt_calc(ch_0012[i],
                                             ch_1315[i],
                                             ch_1619_sec[i],
                                             ftba_es_rt,
                                             use_max=False)
            # calculate method 2 maximum amount
            m2_max[i] = (m2_std_max[i]
                         + m2_es_max[i]
                         + nbs_amt[i]
                         + supp_amt[i])
            # income test reduction amount
            m2_inc_test_redn[i] = ftba_inc_test_calc(ftb_inc,
                                                     ftba_tpr[1],
                                                     ftba_free_area[1])
            # calculate method 2 amount
            m2_amt[i] = max(0, m2_max[i] - m2_inc_test_redn[i])

        # compare method 1 with method 2 amount and award the higher
        ftba_amt[i] = max(m1_amt[i], m2_amt[i])
    return ftba_amt
