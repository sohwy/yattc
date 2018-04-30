import ftb
import time
import pandas as pd
import numpy as np

z = ftb.FamilyTaxBenefit.factory(pd.Period('2015Q1'))
z = ftb.FamilyTaxBenefit.factory(pd.Period('2013Q3'))

size = int(10**5)
ftb_0_12_ch = np.random.randint(0, 3, size, dtype=np.int8)
ftb_13_15_ch = np.random.randint(0, 3, size, dtype=np.int8)
ftb_16_19_sec_ch = np.random.randint(0, 3, size, dtype=np.int8)
ftba_std_rt = np.array([1529.35, 4766.90, 6201.35, 6201.35], dtype=np.float64)
ftba_es_rt = np.array([36.50, 91.25, 116.80, 116.80, 36.50], dtype=np.float64)
nbs_rt = np.array([1595.23], dtype=np.float64)
ra_max_amt = np.random.randint(0, 500, size)
maint_inc = np.random.uniform(0, 5000, size)
minc_recipients = np.random.randint(0, 3, size)
ftype = np.random.randint(0, 2, size)
child_supp_ch = np.random.randint(0, 4, size)
ftba_mifa = np.array([1587.75, 1587.75, 3175.50])
ftba_mifa_addon = np.array([529.25, 529.25, 529.25])
mifa_tpr = np.array([0.5])
print(ra_max_amt.size)
print(ftb_0_12_ch)
print(ftb_13_15_ch)
print(ftba_std_rt)
print(ftba_es_rt)
print(ra_max_amt)

print(ftb.ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt))
print(ftb.ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt))
print(ftb.foo(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt))

print(ftb.ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False))
print(ftb.ftba_max_amt(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False))
print(ftb.foo(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt, max_rate=False))

ftba_max_amount = ftb.ftba_max_amt_np(2, 1, 1, ftba_std_rt, ftba_es_rt, 0, 0, max_rate=False)
ftba_max_amount2 = ftb.ftba_max_amt_np(2, 1, 1, np.repeat(ftba_std_rt[0], 4), np.repeat(ftba_es_rt[0], 4), 0, 0, max_rate=False)
ftba_max_amount3 = ftb.ftba_max_amt_s(2, 1, 1, ftba_std_rt, ftba_es_rt, np.array([0]), 0, max_rate=False)
print(ftba_max_amount)
print(ftba_max_amount2)
# print(ftba_max_amount3)

ftb.ftba_method1_apportion(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch, ftba_std_rt, ftba_es_rt, nbs_rt, ra_max_amt)


print(ftb.ftba_maint_inc_test(maint_inc, ftba_mifa, ftba_mifa_addon, mifa_tpr, ftype, minc_recipients, child_supp_ch))
print(ftb.ftba_maint_inc_test_np(maint_inc, ftba_mifa, ftba_mifa_addon, mifa_tpr, ftype, minc_recipients, child_supp_ch))

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
    f1 = ftb.ftba_max_amt_np(ftb_0_12_ch, ftb_13_15_ch, ftb_16_19_sec_ch,
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

def test_maint_inc(func1, func2, **kwargs):
    """
    Test functions
    """
    print(30 * '-')
    print('testing {} against {}'.format(func1.__name__, func2.__name__))

    # check that outputs match
    f1 = func1(**kwargs)
    f2 = func2(**kwargs)
    assert np.allclose(f1, f2), 'Results do not match'
    print('Results match')

    # time the function
    median_times = []
    for func in [func1, func2]:
        times = []
        for i in range(5):
            t0 = time.time()
            func(**kwargs)
            t1 = time.time()
            times.append(t1 - t0)
        print('Execution time: {:.5g} sec'.format(np.median(times)))
        median_times.append(np.median(times))
    print('Speed factor (func2/func1): {:.5g}'.format(median_times[0] / median_times[1]))

ftba_max_args = {'ftb_0_12_ch' : np.random.randint(0, 3, size, dtype=np.int8),
                 'ftb_13_15_ch' : np.random.randint(0, 3, size, dtype=np.int8),
                 'ftb_16_19_sec_ch' : np.random.randint(0, 3, size, dtype=np.int8),
                 'ftba_std_rt' : np.array([1529.35, 4766.90, 6201.35, 6201.35], dtype=np.float64),
                 'ftba_es_rt' : np.array([36.50, 91.25, 116.80, 116.80, 36.50], dtype=np.float64),
                 'nbs_rt' : np.array([1595.23], dtype=np.float64),
                 'ra_max_amt' : np.random.randint(0, 500, size)}

ftba_maint_inc_test_args = {'maint_inc': np.random.uniform(0, 5000, size),
                            'ftba_mifa': np.array([1587.75, 1587.75, 3175.50]),
                            'mifa_addon': np.array([529.25, 529.25, 529.25]),
                            'mifa_tpr': np.array([0.5]),
                            'ftype': np.random.randint(0, 2, size),
                            'minc_recipients': np.random.randint(0, 3, size),
                            'child_supp_ch': np.random.randint(0, 4, size)}

# test_calc(z.ftba_max_amt)
test_maint_inc(ftb.ftba_max_amt,
               ftb.foo,
               **ftba_max_args)
test_maint_inc(ftb.ftba_max_amt_np,
               ftb.ftba_max_amt,
               **ftba_max_args)
test_maint_inc(ftb.ftba_max_amt_py,
               ftb.foo,
               **ftba_max_args)
# test_maint_inc(ftb.ftba_maint_inc_test,
#                ftb.ftba_maint_inc_test_np,
#                **ftba_maint_inc_test_args)
# 
# test_maint_inc(ftb.ftba_maint_inc_test,
#                ftb.ftba_maint_inc_test_py,
#                **ftba_maint_inc_test_args)


# maint_inc = np.arange(-100, 5000, 100)
# famtype = np.arange(0, 2)
# minc_recipients = np.arange(0, 3)
# child_supp_ch = np.arange(0, 3)
# grid = np.array(np.meshgrid(maint_inc, famtype, minc_recipients, child_supp_ch)).T.reshape(-1, 4)
# print(grid)
# maint_inc = grid[:, 0]
# famtype = grid[:, 1]
# minc_recipients = grid[:, 2]
# child_supp_ch = grid[:, 3]
# 
# print(ftb.ftba_maint_inc_test(maint_inc, ftba_mifa, ftba_mifa_addon, mifa_tpr, famtype, minc_recipients, child_supp_ch))
