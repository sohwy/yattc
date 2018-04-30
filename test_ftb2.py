import numpy as np
import numba
import ftb2 as ftb
import time
from func_tester import test_funcs


obs = np.empty(10**5)

######################
# ftba_std_amt_calc
######################

y = ftb.ftba_std_amt_calc(1, 1, 0, np.array([1529.35, 4766.90, 6201.35, 6201.35]))
print(y)

y = ftb.ftba_std_amt_calc(1, 1, 0, np.array([36.50, 91.25, 116.80, 116.80]))
print(y)

def ftba_std_amt_calc_iter(ch_0012, ch_1315, ch_1619_sec, ftba_rt, use_max=True):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftba_std_amt_calc(ch_0012[i], ch_1315[i],
                                       ch_1619_sec[i], ftba_rt)
    return res

@numba.jit(nopython=True)
def ftba_std_amt_calc_iter_jit(ch_0012, ch_1315, ch_1619_sec, ftba_rt, use_max=True):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftba_std_amt_calc(ch_0012[i], ch_1315[i],
                                       ch_1619_sec[i], ftba_rt)
    return res

in_args = {
        'ch_0012': np.random.randint(0, 3, obs.size),
        'ch_1315': np.random.randint(0, 3, obs.size),
        'ch_1619_sec': np.random.randint(0, 3, obs.size),
        'ftba_rt': np.array([36.50, 91.25, 116.80, 116.80]),
        'use_max': True
        }

# test_funcs(ftba_std_amt_calc_iter, ftba_std_amt_calc_iter_jit, **in_args)


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

in_args = {
        'ch_00': np.random.randint(0, 3, obs.size),
        'ch_dep': np.random.randint(0, 3, obs.size),
        'nbs_rt': np.array([540.54, 1618.89])
        }

# test_funcs(nbs_amt_calc_iter, nbs_amt_calc_iter_jit, **in_args)


######################
# ftba_inc_test_calc
######################
# ftb_inc, ftba_tpr, ftba_free_area
for inc in np.arange(0, 100000, 5000):
    y = ftb.ftba_inc_test_calc(inc, 0.2, 52706)
    print(inc, y)

y = ftb.ftba_inc_test_calc(0, 0.3, 94316)
print(y)

def ftba_inc_test_calc_iter(ftb_inc, ftba_tpr, ftba_free_area):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = ftb.ftba_inc_test_calc(ftb_inc[i], 0.2, 52706)
    return res

ftba_inc_test_calc_iter_jit = numba.jit(nopython=True)(ftba_inc_test_calc_iter)

in_args = {
        'ftb_inc': np.random.uniform(0, 120000, obs.size),
        'ftba_tpr': np.array([0.2, 0.3])[0],
        'ftba_free_area': np.array([52706, 94316])[0]
        }

test_funcs(ftba_inc_test_calc_iter, ftba_inc_test_calc_iter_jit, **in_args)
