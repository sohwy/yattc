import rent_assistance as ra
import pandas as pd
import numpy as np
import time

z = ra.RentAssistance.factory(pd.Period('2013Q3'))
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
    f1 = ra.calc_rent_assistance_py(ftype, kids, rent, sharer, min_rent_thd,
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
    print('Execution time: {:.5g} sec'.format(np.median(times)))

print(z.calc_rent_assistance.__name__)

test_calc(z.calc_rent_assistance)
