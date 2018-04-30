import time
import numpy as np


def test_funcs(func1, func2, **kwargs):
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
