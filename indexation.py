from functools import singledispatch
import pandas as pd
import numpy as np
class Indexation():
    def __init__(self):
        self.add = singledispatch(self.add)
        self.add.register(int, self.add_int)
        self.add.register(list, self.add_list)
        self.add.register(pd.Series, self.add_pd_series)
        self.add.register(pd.DataFrame, self.add_pd_df)

    def add(self, a, b):
        raise NotImplementedError('Unsupported type')

    def add_int(self, a, b):
        print('type of a is ' + str(type(a)))
        return a + b

    def add_list(self, a, b):
        print('type of a is ' + str(type(a)))
        return a, b

    def add_pd_series(self, a, b):
        print('type of a is ' + str(type(a)))
        return a

    def add_pd_df(self, a, b):
        print('type of a is ' + str(type(a)))
        return a

    def inflate(self, x):
        return [self.inflate_func(z) for z in x]

    def inflate_func(self, x):
        return x + 1

a = pd.Series(range(3))
b = {'col1':[1, 1, 1], 'col2': [2, 2, 2]}
c = pd.DataFrame(data=b)
print(a)
print(c)
z = [1, 2]
y = [3, 4]
ind = Indexation()
print(ind.add(1, 2))
print(ind.add(z, y))
print(ind.add(a, 7))
print(ind.add(c, 7))
