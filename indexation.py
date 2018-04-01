from functools import singledispatch
import pandas as pd
import numpy as np
import json
import requests


data = {
        'param1': {'data': [[1, 1], [1, 1], [1, 1], [1, 1]],
                   'index': {'x1': 'x1_func', 'x2': 'chained'},
                   'chained_args': {'x2': ('x1', 0.5)}
                   }
        }

df = pd.DataFrame(data['param1']['data'], columns=['x1', 'x2'])
print(df)
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
        print(a.columns)
        for col in a.columns:
            print(self.c_mapper.get(col))
            func = self.c_mapper.get(col)
            a[col] = func(self, a)
        return a

    def add_for_col1(self, x):
        return x['col1'] * 1

    def add_for_col2(self, x):
        return x['col1'] * -1

    def inflate(self, param):
        for column in param.columns:
            index_func_name = data['param1']['index'][column]
            print(index_func_name)
            rate = 1
            param[column] = getattr(self, index_func_name)(param, column, rate)
        return param

#     def x1_func(self, param, *args):
#         print(args)
#         return param[args[0]] * -1
# 
#     def x2_func(self, param, *args):
#         print(args)
#         return param[args[0]] + 10
# 
#     def chained(self, param, chained_to, rate):
#         return param[chained_to] * rate

    def inflate2(self, param):

        # inflation functions
        def x1_func(column):
            # can we access class and instance attributes here?
            # such as any indexation series
            print(self.add_for_col1)
            return param[column] * -10

        def chained(column, rate):
            return param[column] * rate

        func_mapper = {'x1_func': x1_func, 'chained': chained}
        # args_mapper = {'x2': ('x1', 0.5)}

        for column in param.columns:
            index_func_name = data['param1']['index'][column]
            func = func_mapper[index_func_name]
            # args = args_mapper.get(column, (column,))
            # args = args_mapper[column]
            args = data['param1']['chained_args'].get(column, (column,))
            print('column:', column)
            print('args:', args)
            param[column] = func(*args)
        return param


    c_mapper = {'col1': add_for_col1, 'col2': add_for_col2}

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
z = ind.add(c, 7)
print(ind.inflate2(df))
 

class Index(object):
    """
    doctstring
    """
    urls = {'cpi': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/1.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2017-Q4',
            'mte': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/2.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2017-Q4'}

    DEFAULT_FILENAME = 'indexation.json'

    def __init__(self, indices_dict=None, use_api_data=False):


        # some parameters just for testing
        self.param1 = pd.DataFrame(np.ones(30), index=pd.PeriodIndex(start='2000Q3', end='2007Q4', freq='Q'), columns=['x1'])
        # read in index values
        if indices_dict is None:
            with open(self.DEFAULT_FILENAME) as f:
                self.indices = json.load(f)
        elif isinstance(indices_dict, dict):
            self.indices = indices_dict
        else:
            raise ValueError('indices_dict must be None or a dictionary')

        self.set_default_series_vals(use_api_data)

    def set_default_series_vals(self, use_api_data=False):
        """
        Set as attributes the array of values for each parameter
        """
        if use_api_data:
            for index_name in self.urls.keys():
                index_df = self.get_api_data(index_name)
                setattr(self, index_name, index_df)
        else:
            if hasattr(self, 'indices'):
                for index_name, data in self.indices.items():
                    idx = pd.PeriodIndex(start=data['start_period'],
                                         end=data['end_period'],
                                         freq='Q')[::int(4 / data['freq'])]
                    index_df = pd.DataFrame(data['values'],
                                            index=idx,
                                            columns=['values'])
                    index_df['pct_change'] = round(index_df['values'].pct_change(), 4)
                    setattr(self, index_name, index_df)

    @classmethod
    def get_api_data(self, series):
        """
        EXPERIMENTAL - don't blame me if you use this and something goes wrong

        Get the index series using the ABS Stat API if Index object is
        initialised with parameter use_api_data=True
        """
        try:
            # get the api data and turn it into a json string
            api_data = requests.get(self.urls[series])
            api_data.raise_for_status()
            if api_data.status_code == requests.codes.ok:
                api_data = api_data.json()

            # get the periods of the data series
            p = api_data['structure']['dimensions']['observation'][5]['values']
            p = pd.PeriodIndex([value['id'] for value in p], freq='Q')

            # get the values of the data series
            vals = api_data['dataSets'][0]['observations'].values()

            # create the data frame
            combined = pd.DataFrame(list(vals), index=p, columns=['values'])
            combined['pct_change'] = round(combined['values'].pct_change(), 4)
            return combined
        except requests.exceptions.HTTPError as err:
            print('Bad url: {}'.format(err))
            raise

    def simple_inflate(self, series, pct_change):
        for i in range(1, 5):
            series[i] = series[i-1] * (1 + pct_change[i])

    def inflate(self, param):
        print(self.param1)

        # inflation functions
        def x1_func(column):
            # can we access class and instance attributes here?
            # such as any indexation series
            return param[column] * -10

        def chained(column, rate):
            return param[column] * rate

        def cpi_inflate(column, series):
            return param[column] * (1 + series)

        func_mapper = {'x1_func': x1_func, 'chained': chained}
        # args_mapper = {'x2': ('x1', 0.5)}

        for column in param.columns:
            index_func_name = data['param1']['index'][column]
            func = func_mapper[index_func_name]
            # args = args_mapper.get(column, (column,))
            # args = args_mapper[column]
            args = data['param1']['chained_args'].get(column, (column,))
            print('column:', column)
            print('args:', args)
            param[column] = func(*args)
        return param


# ind = Index(use_api_data=True)
print('========')
print('this is using Index class')
print('========')
ind = Index(use_api_data=False)
print(ind.indices)
print(dir(ind))
print(ind.cpi.head())
print(ind.mte.head())
ind.inflate(param1)

# print(ind.urls)
# print(Index.get_api_data('cpi'))
# print(Index.get_api_data('cpi_change'))
# print(Index.get_api_data('cpi_change_'))
