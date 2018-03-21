"""
Inflation class
"""

# import json
import datetime
import numpy as np
# import pandas as pd


class Inflation():
    """
    Inflation class
    """

    DEFAULT_FILENAME = 'inflation.json'


    def __init__(self, inflation_dict=None):
        pass


last_known_date = datetime.date(2003, 3, 20)
print(type(last_known_date))

def increment_quarter(date):
    if not isinstance(date, datetime.date):
        raise ValueError('Input not a date object')
    if date.month not in (1, 3, 7, 9) or date.day not in (1, 20):
        raise ValueError('Not a valid parameter date')
    if date.month == 1:
        next_month = 3
        next_day = 20
        next_year = date.year
    elif date.month == 3:
        next_month = 7
        next_day = 1
        next_year = date.year
    elif date.month == 7:
        next_month = 9
        next_day = 20
        next_year = date.year
    elif date.month == 9:
        next_month = 1
        next_day = 1
        next_year = date.year + 1
    return (next_year, next_month, next_day)


print(increment_quarter(last_known_date))
# print(increment_quarter(10))
# quarters = [(2001, 7, 1), (2001, 9, 20), (2002, 1, 1), (2002, 3, 20)]
# quarters = [datetime.date(*date) for date in quarters]
# print(quarters)


# print(mapping)
# print(mapping[1])
# print(mapping[3])


def increment_quarter2(date):
    if not isinstance(date, datetime.date):
        raise ValueError('Input not a datetime object')
    if date.month not in (1, 3, 7, 9) or date.day not in (1, 20):
        raise ValueError('Not a valid parameter date')
    mapping = {1: (0, 3, 20), 3: (0, 7, 1), 7: (0, 9, 20), 9: (1, 1, 1)}
    date_tuple = mapping[date.month]
    return datetime.date(date.year + date_tuple[0],
                         date_tuple[1],
                         date_tuple[2])


#     next_year = date.year + date_tuple[0]
#     next_month = date_tuple[1]
#     next_day = date_tuple[2]
#     return (next_year, next_month, next_day)

print(increment_quarter2(last_known_date))




param = [0.19, 0.20, 0.21, 0.22]
len_known = 14

param_q = np.repeat(param, 4)[:len_known]
print(param_q)

start_known = datetime.date(2000, 7, 1)  # first known period
end_known = datetime.date(2001, 3, 20)  # last known period
forward_len = 4  # number of periods in forward period

# this creates the list of dates from the start to end of forwards period

def make_date_list(start_known, end_known, forward_len):
    # number of periods from start_known to end_known... roughly...
    current_len = round((end_known - start_known).days / 91.25 + 1)
    tot_periods = current_len + forward_len
    x = [start_known]
    for i in range(0, tot_periods - 1):
        x.append(increment_quarter2(x[-1]))
    return x

print(make_date_list(start_known, end_known, forward_len))

def expand_array(values, num_periods):
    values = np.array(values)
    ans = np.zeros(num_periods, dtype=np.float64)
    ans[:len(values)] = values
    extra = [float(values[-1]) for i in range(0, num_periods - len(values))]
    ans[len(values):] = extra
    return ans

param_expanded = expand_array(param, 8)
print(param_expanded)
print(type(param_expanded))




























