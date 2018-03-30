from functools import singledispatch
import pandas as pd
import numpy as np
import json
import requests


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


class Index(object):
    """
    doctstring
    """
    urls = {'cpi': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/1.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2017-Q4',
            'cpi_change': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/2.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2017-Q4',
            'cpi_change_': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/2.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2018xx'}

    DEFAULT_FILENAME = 'indexation.json'
    DEFAULT_PERIODS = ["2000Q3", "2000Q4",
                       "2001Q1", "2001Q2", "2001Q3", "2001Q4",
                       "2002Q1", "2002Q2", "2002Q3", "2002Q4",
                       "2003Q1", "2003Q2", "2003Q3", "2003Q4",
                       "2004Q1", "2004Q2", "2004Q3", "2004Q4"]
    # remember if you change DEFAULT_PERIODS to make sure you have updated
    # every parameter as well
    DEFAULT_START_PERIOD = DEFAULT_PERIODS[0]
    DEFAULT_END_PERIOD = DEFAULT_PERIODS[-1]
    DEFAULT_NUM_CUR_PERIODS = len(DEFAULT_PERIODS)
    DEFAULT_NUM_FWD_PERIODS = 12
    DEFAULT_NUM_PERIODS = DEFAULT_NUM_CUR_PERIODS + DEFAULT_NUM_FWD_PERIODS

    def __init__(self, indices_filename=None):
        if indices_filename is None:
            with open(self.DEFAULT_FILENAME) as f:
                self.indices = json.load(f)

    @classmethod
    def get_api_data(self, series):
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
            return combined
        except requests.exceptions.HTTPError as err:
            print('Bad url: {}'.format(err))
            return None


ind = Index()
print(ind.urls)
print(Index.get_api_data('cpi'))
print(Index.get_api_data('cpi_change'))
print(Index.get_api_data('cpi_change_'))
