import numpy as np
import numba
import ftb2 as ftb
import time
from func_tester import test_funcs


obs = np.empty(10**5)
# obs = np.empty(2 * 10**4)

######################
# ftba_std_amt_calc
######################

# y = ftb.ftba_std_amt_calc(1, 1, 0, np.array([1529.35, 4766.90, 6201.35, 6201.35]))
# print(y)
# 
# y = ftb.ftba_std_amt_calc(1, 1, 0, np.array([36.50, 91.25, 116.80, 116.80]))
# print(y)
# 
# def ftba_std_amt_calc_iter(ch_0012, ch_1315, ch_1619_sec, ftba_rt, use_max=True):
#     res = np.zeros(obs.size)
#     for i in range(obs.size):
#         res[i] = ftb.ftba_std_amt_calc(ch_0012[i], ch_1315[i],
#                                        ch_1619_sec[i], ftba_rt)
#     return res
# 
# @numba.jit(nopython=True)
# def ftba_std_amt_calc_iter_jit(ch_0012, ch_1315, ch_1619_sec, ftba_rt, use_max=True):
#     res = np.zeros(obs.size)
#     for i in range(obs.size):
#         res[i] = ftb.ftba_std_amt_calc(ch_0012[i], ch_1315[i],
#                                        ch_1619_sec[i], ftba_rt)
#     return res
# 
# in_args_1 = {
#         'ch_0012': np.random.randint(0, 3, obs.size),
#         'ch_1315': np.random.randint(0, 3, obs.size),
#         'ch_1619_sec': np.random.randint(0, 3, obs.size),
#         'ftba_rt': np.array([36.50, 91.25, 116.80, 116.80]),
#         'use_max': True
#         }


y = ftb.ftba_std_amt_calc(1, 1, 0, np.array([1529.35, 4766.90, 6201.35, 6201.35]), np.array([36.50, 91.25, 116.80, 116.80]))
print(y)


def ftba_std_amt_calc_iter(ch_0012, ch_1315, ch_1619_sec, ftba_std_rt, ftba_es_rt, use_max=True):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftba_std_amt_calc(ch_0012[i], ch_1315[i],
                                       ch_1619_sec[i], ftba_std_rt, ftba_es_rt)
    return res

@numba.jit(nopython=True)
def ftba_std_amt_calc_iter_jit(ch_0012, ch_1315, ch_1619_sec, ftba_std_rt, ftba_es_rt, use_max=True):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftba_std_amt_calc(ch_0012[i], ch_1315[i],
                                       ch_1619_sec[i], ftba_std_rt, ftba_es_rt)
    return res

in_args_1 = {
        'ch_0012': np.random.randint(0, 3, obs.size),
        'ch_1315': np.random.randint(0, 3, obs.size),
        'ch_1619_sec': np.random.randint(0, 3, obs.size),
        'ftba_std_rt': np.array([1529.35, 4766.90, 6201.35, 6201.35]),
        'ftba_es_rt': np.array([36.50, 91.25, 116.80, 116.80]),
        'use_max': True
        }

######################
# nbs_amt_calc
######################
# ch_00, ch_dep, nbs_rt
y = ftb.nbs_amt_calc(0, 1, np.array([540.54, 1618.89]))
print(y)

y = ftb.nbs_amt_calc(2, 2, np.array([540.54, 1618.89]))
print(y)

def nbs_amt_calc_iter(ch_00, ch_dep, nbs_rt):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.nbs_amt_calc(ch_00[i], ch_dep[i], nbs_rt)
    return res

nbs_amt_calc_iter_jit = numba.jit(nopython=True)(nbs_amt_calc_iter)

in_args_2 = {
        'ch_00': np.random.randint(0, 3, obs.size),
        'ch_dep': np.random.randint(0, 3, obs.size),
        'nbs_rt': np.array([540.54, 1618.89])
        }

######################
# ftba_inc_test_calc
######################
# ftb_inc, ftba_tpr, ftba_free_area
y = ftb.ftba_inc_test_calc(76000, 0.2, 52706)
print(y)

y = ftb.ftba_inc_test_calc(0, 0.3, 94316)
print(y)

def ftba_inc_test_calc_iter(ftb_inc, ftba_tpr, ftba_free_area):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftba_inc_test_calc(ftb_inc[i], 0.2, 52706)
    return res

ftba_inc_test_calc_iter_jit = numba.jit(nopython=True)(ftba_inc_test_calc_iter)

in_args_3 = {
        'ftb_inc': np.random.uniform(0, 120000, obs.size),
        'ftba_tpr': np.array([0.2, 0.3])[0],
        'ftba_free_area': np.array([52706, 94316])[0]
        }

######################
# maint_inc_test_calc
######################
# ch_maint, maint_inc_p1, maint_inc_p2, maint_inc_base, maint_inc_add, maint_inc_tpr

y = ftb.maint_inc_test_calc(1, 1000, 0, 1, 1587.75, 529.25, 0.5)
print(y)

def maint_inc_test_calc_iter(ch_maint, maint_inc_p1, maint_inc_p2, maint_inc_recp, maint_inc_base, maint_inc_add, maint_inc_tpr):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.maint_inc_test_calc(ch_maint[i],
                                         maint_inc_p1[i],
                                         maint_inc_p2[i],
                                         maint_inc_recp[i],
                                         1587.75,
                                         529.25,
                                         0.5)
    return res

maint_inc_test_calc_iter_jit = numba.jit(nopython=True)(maint_inc_test_calc_iter)

in_args_4 = {
        'ch_maint': np.random.randint(0, 3, obs.size),
        'maint_inc_p1': np.random.uniform(0, 5000, obs.size),
        'maint_inc_p2': np.random.uniform(0, 5000, obs.size),
        'maint_inc_recp': np.random.randint(0, 3, obs.size),
        'maint_inc_base': 1587.75,
        'maint_inc_add': 529.25,
        'maint_inc_tpr': 0.5
        }



######################
# ftbb_std_amt_calc
######################

# y = ftb.ftbb_std_amt_calc(1, 90000, 100000, np.array([4055.15, 2843.15, 2843.15]))
y = ftb.ftbb_std_amt_calc(1, 90000, 100000, np.array([4055.15, 2843.15, 2843.15]), np.array([73.00, 51.10]))
print(y)

for ch_age in range(20):
    for income in range(0, 150000, 30000):
        y = ftb.ftbb_std_amt_calc(ch_age, income, 100000, np.array([4055.15, 2843.15, 2843.15]), np.array([73.00, 51.10]))
        print(ch_age, income, y)

def ftbb_std_amt_calc_iter(ch_young, ftb_inc_p1, ftbb_pri_inc_lmt, ftbb_std_amt, ftbb_es_amt ):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftbb_std_amt_calc(ch_young[i], ftb_inc_p1[i], ftbb_pri_inc_lmt, ftbb_std_amt, ftbb_es_amt)
    return res


@numba.jit(nopython=True)
def ftbb_std_amt_calc_iter_jit(ch_young, ftb_inc_p1, ftbb_pri_inc_lmt, ftbb_std_amt, ftbb_es_amt):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftbb_std_amt_calc(ch_young[i], ftb_inc_p1[i], ftbb_pri_inc_lmt, ftbb_std_amt, ftbb_es_amt)
    return res

in_args_5 = {
        'ch_young': np.random.randint(0, 20, obs.size),
        'ftb_inc_p1': np.random.uniform(0, 200000, obs.size),
        'ftbb_pri_inc_lmt': 100000,
        'ftbb_std_amt': np.array([4055.15, 2843.15, 2843.15]),
        'ftbb_es_amt': np.array([73.00, 51.10])
        }

######################
# ftbb_inc_test_calc
######################
# def ftbb_inc_test_calc(ftb_inc_p2, isp_rcp, ftbb_sec_inc_lmt, ftbb_tpr):

y = ftb.ftbb_inc_test_calc(60000, True, 5500, 0.2)
print(y)

def ftbb_inc_test_calc_iter(ftb_inc_p2, isp_rcp, ftbb_sec_inc_lmt, ftbb_tpr):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftbb_inc_test_calc(ftb_inc_p2[i], isp_rcp[i], ftbb_sec_inc_lmt, ftbb_tpr)
    return res


@numba.jit(nopython=True)
def ftbb_inc_test_calc_iter_jit(ftb_inc_p2, isp_rcp, ftbb_sec_inc_lmt, ftbb_tpr):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftbb_inc_test_calc(ftb_inc_p2[i], isp_rcp[i], ftbb_sec_inc_lmt, ftbb_tpr)
    return res


in_args_6 = {
        'ftb_inc_p2': np.random.uniform(0, 10000, obs.size),
        'isp_rcp': np.random.choice([False, True], obs.size),
        'ftbb_sec_inc_lmt': 5500,
        'ftbb_tpr': 0.5
        }


######################
# ftbb_amt_calc
######################

in_args_7 = {
        'ch_young': np.random.randint(0, 20, obs.size),
        'ftb_inc_p1': np.random.uniform(0, 200000, obs.size),
        'ftb_inc_p2': np.random.uniform(0, 10000, obs.size),
        'isp_rcp': np.random.choice([False, True], obs.size),
        'ftbb_pri_inc_lmt': 100000,
        'ftbb_sec_inc_lmt': 5500,
        'ftbb_std_amt': np.array([4055.15, 2843.15, 2843.15]),
        'ftbb_es_amt': np.array([73.00, 51.10]),
        'ftbb_supp': 375,
        'ftbb_tpr': 0.5
        }

# ftbb_amt_calc(ch_young, ftb_inc_p1, ftb_inc_p2, isp_rcp, ftbb_pri_inc_lmt, ftbb_sec_inc_lmt, ftbb_std_amt, ftbb_es_amt, ftbb_supp, ftbb_tpr):
ftb.ftbb_amt_calc(**in_args_7)


def main(run=True):
    if run:
        test_funcs(ftba_std_amt_calc_iter, ftba_std_amt_calc_iter_jit, **in_args_1)
        test_funcs(nbs_amt_calc_iter, nbs_amt_calc_iter_jit, **in_args_2)
        test_funcs(ftba_inc_test_calc_iter, ftba_inc_test_calc_iter_jit, **in_args_3)
        test_funcs(maint_inc_test_calc_iter, maint_inc_test_calc_iter_jit, **in_args_4)
        test_funcs(ftbb_std_amt_calc_iter, ftbb_std_amt_calc_iter_jit, **in_args_5)
        test_funcs(ftbb_inc_test_calc_iter, ftbb_inc_test_calc_iter_jit, **in_args_6)
        test_funcs(ftb.ftbb_amt_calc, ftb.ftbb_amt_calc, **in_args_7)


if __name__ == '__main__':
    main()
    # main(run=False)
