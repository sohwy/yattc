import numpy as np
import numba
import supp
import time
from func_tester import test_funcs


obs = np.empty(10**5)

##################
# util_all_calc2
##################
# isp_amt, isp_type, ftype, age, sex, util_all_amt, pen_age_thr
y = supp.util_all_calc2(10, 0, 0, 21, 0, np.array([100, 200]), np.array([65, 65]))
print(y)

y = supp.util_all_calc2(10, 0, 0, 21, 0, np.array([100, 200]), np.array([65, 65]))
def util_all_calc2_iter(isp_amt, isp_type, ftype, age, sex, util_all_amt, pen_age_thr):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = supp.util_all_calc2(isp_amt[i], isp_type[i], ftype[i], age[i], sex[i], util_all_amt, pen_age_thr)
    return res

@numba.jit(nopython=True)
def util_all_calc2_iter_jit(isp_amt, isp_type, ftype, age, sex, util_all_amt, pen_age_thr):
    res = np.zeros(obs.size)
    for i in range(obs.size):
        res[i] = supp.util_all_calc2(isp_amt[i], isp_type[i], ftype[i], age[i], sex[i], util_all_amt, pen_age_thr)
    return res

in_args_1 = {
        'isp_amt': np.random.uniform(0, 10000, obs.size),
        'isp_type': np.random.choice([0, 1, 2, 3, 4, 5], obs.size),
        'ftype': np.random.randint(0, 2, obs.size),
        'age': np.random.randint(0, 80, obs.size),
        'sex': np.random.randint(0, 2, obs.size),
        'util_all_amt': np.array([36.50, 91.25, 116.80, 116.80]),
        'pen_age_thr': np.array([36.50, 91.25, 116.80, 116.80]),
        }

def main(run=True):
    if run:
        test_funcs(util_all_calc2_iter, util_all_calc2_iter_jit, **in_args_1)


if __name__ == '__main__':
    main()
