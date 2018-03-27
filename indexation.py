from functools import singledispatch

class Indexation():
    def __init__(self):
        self.add = singledispatch(self.add)
        self.add.register(int, self.add_int)
        self.add.register(list, self.add_list)

    def add(self, a, b):
        raise NotImplementedError('Unsupported type')

    def add_int(self, a, b):
        print('type of a is ' + str(type(a)))
        return a + b

    def add_list(self, a, b):
        print('type of a is ' + str(type(a)))
        return a, b


z = [1, 2]
y = [3, 4]
ind = Indexation()
print(ind.add(1, 2))
print(ind.add(z, y))
