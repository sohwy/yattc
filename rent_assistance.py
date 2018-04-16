"""
Rent assistance class
"""

import pandas as pd
import numpy as np
from numba import jit, prange, vectorize, int8, float64

# create dummy data
size = 10**4
ftype = np.random.randint(0, 2, size, dtype=np.int8)
kids = np.random.randint(0, 3, size, dtype=np.int8)
rent = np.random.choice([0.0, 100, 150, 200, 250, 300, 350, 400], size)
sharer = np.full(size, False, dtype=bool)
ra_prop = np.array(0.75)
min_rent_thd = np.array([117.80, 191.00, 154.84, 229.18, 154.84, 229.18], dtype=np.float64)
max_ra_rate = np.array([132.2, 124.6, 155.26, 155.26, 175.42, 175.42], dtype=np.float64)

# get family type for rent assistance purposes
# 0 = single, 1 = couple, 2 = single (1-2), 3 = single (3+)
# 4 = couple(1-2), 5 = couple (3+)

class RentAssistance(object):
    def __init__(self, period):
        pass



# numpy implementation
def get_ra_ftype_np(fam_type, ftb_kids):
    return fam_type + 2 * ftb_kids

# vectorized
@vectorize([int8(int8, int8)])
def get_ra_ftype_vec(fam_type, ftb_kids):
    ftype_ra = fam_type + 2 * ftb_kids
    return ftype_ra

# jitted
@jit()
def get_ra_ftype_jit(fam_type, ftb_kids):
    ftype_ra = np.zeros_like(fam_type)
    for i in range(fam_type.size):
        ftype_ra[i] = fam_type[i] + 2 * ftb_kids[i]
    return ftype_ra

z_np = get_ra_ftype_np(ftype, kids)
z_vec = get_ra_ftype_vec(ftype, kids)
z_jit = get_ra_ftype_jit(ftype, kids)
print(np.allclose(z_vec, z_jit))
print(np.allclose(z_np, z_jit))





# this can be jitted
@jit()
def bar(ftype_ra, min_rent_thd, max_ra_rate, ra_prop, rent, sharer):
    ans = np.zeros_like(rent)
    # get row stuff
    for i in range(ftype_ra.size):
        ftype = ftype_ra[i]
        min_rent = min_rent_thd[ftype]
        max_rate = max_ra_rate[ftype]
        # rent_amt = rent[i]
        if rent[i] - min_rent < 0:
            ans[i] = 0
        else:
            if sharer[i]:
                max_rate *= 0.5
            ans[i] = max(min(((rent[i] - min_rent) * ra_prop), max_rate), 0)
    return ans

rent_ass = bar(z_vec, min_rent_thd, max_ra_rate, ra_prop, rent, sharer)

print(z_vec)
print(min_rent_thd)
print(max_ra_rate)
print(rent)
print(sharer)

# df = pd.DataFrame([z_vec, rent, sharer, rent_ass]).T
# print(df)
