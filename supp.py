import numba
import numpy as np

obs = np.empty(10**5)

def util_all_calc(dsp_u21_amt, pta_amt, wda_amt, ftype, age, sex,
                  util_all_amt, pen_age_thr):
    """
    Calculate rate of utility allowance
    Arguments:
        Variables:
        dsp_u21_amt: dsp u21 amount
        pta_amt: partner allowance amount
        wda_amt: widow allowance amount
        ftype
        age
        sex
        Parameters:
        util_all_amt
        pen_age_thr
    Returns:
    Utility allowance amount
    """
    if dsp_u21_amt > 0 or (age < pen_age_thr[sex] and (pta_amt > 0 or wda_amt > 0)):
        return util_all_amt[ftype]
    return 0.

@numba.jit(nopython=True)
# @profile
def util_all_calc2(isp_amt, isp_type, ftype, age, sex,
                  util_all_amt, pen_age_thr):
    """
    Calculate rate of utility allowance
    Arguments:
        Variables:
        isp_amt
        isp_type
        ftype
        age
        sex
        Parameters:
        util_all_amt
        pen_age_thr
    Returns:
    Utility allowance amount
    """
    # pass_test = bool(isp_type in ['dsp'] or (age < pen_age_thr[sex] and isp_type in ['pta', 'wda']))
    # if isp_amt == 0:
        # return 0.
    # pass_test = bool(isp_type == 0 or (age < pen_age_thr[sex] and isp_type in [1, 2]))
    # if pass_test is False or isp_amt == 0:
    # if not pass_test or isp_amt == 0:
    # if not bool(isp_type == 0):
    if isp_amt == 0 or isp_type not in [0, 1, 2] or age > pen_age_thr[sex]:
        return 0.
    # if not age < pen_age_thr[sex] and isp_type in [1, 2]:
    # if age > pen_age_thr[sex]:
        # return 0.
    return util_all_amt[ftype]

def has_cshc(age, sex, isp_rcp, ati_p1, at1_p2, ftype, ch_deps,
             pen_age_thr, cshc_inc_lmt, cshc_addon):
    """
    Determine of person has CSHC
    Arguments:
        Variables:
        age
        sex
        isp_rcp
        ati_p1
        at1_p2
        ftype
        ch_deps
        Parameters:
        pen_age_thr
        cshc_inc_lmt
        cshc_addon
    Returns:
    Whether someone has CSHC
    """
    if age < pen_age_thr[sex] or isp_rcp:
        return False
    return bool((ati_p1 + ati_p2) / (ftype + 1) < cshc_inc_lmt[ftype] + ch_deps * cshc_addon)
    if age >= pen_age_thr[sex] and not isp_rcp:
        return bool((ati_p1 + ati_p2) / (ftype + 1) < cshc_inc_lmt[ftype] + ch_deps * cshc_addon)
    return False

def supp_calcs():
    util_all_amt_p1 = np.zeros(obs.size)
    util_all_amt_p2 = np.zeros(obs.size)
    cshc_holder_p1 = np.full(False, obs.size)
    cshc_holder_p2 = np.full(False, obs.size)
    for i in range(obs.size):
        util_all_amt_p1[i] = util_all_calc(dsp_u21_amt_p1[i], pta_amt_p1[i], wda_amt_p1[i], ftype[i], age_p1[i], sex_p1[i],
                                           util_all_amt, pen_age_thr)
        cshc_holder_p1 = has_cshc(age_p1[i], sex_p1[i], isp_rcp_p1[i], ati_p1[i], at1_p2[i], ftype[i], ch_deps[i],
                                  pen_age_thr, cshc_inc_lmt, cshc_addon)
        if age_p2 > 0:
            util_all_amt_p2[i] = util_all_calc(dsp_u21_amt_p2[i], pta_amt_p2[i], wda_amt_p2[i], ftype[i], age_p2[i], sex_p2[i],
                                               util_all_amt, pen_age_thr)
            cshc_holder_p2 = has_cshc(age_p2[i], sex_p2[i], isp_rcp_p2[i], ati_p1[i], at1_p2[i], ftype[i], ch_deps[i],
                                      pen_age_thr, cshc_inc_lmt, cshc_addon)

def main():
    for _ in range(obs.size):
        util_all_calc2(10, 'dsp', 0, 21, 0, np.array([100, 200]), np.array([65, 65]))

    in_args_1 = {
        'isp_amt': np.random.uniform(0, 10000, obs.size),
        'isp_type': np.random.choice(['dsp', 'pta', 'wda', 'nsa'], obs.size),
        'ftype': np.random.randint(0, 2, obs.size),
        'age': np.random.randint(0, 80, obs.size),
        'sex': np.random.randint(0, 2, obs.size),
        'util_all_amt': np.array([36.50, 91.25, 116.80, 116.80]),
        'pen_age_thr': np.array([36.50, 91.25, 116.80, 116.80]),
        }

if __name__ == '__main__':
    main()
