import pandas as pd
import numpy as np
import json
import requests


class Index(object):
    """
    doctstring
    """
    urls = {'cpi': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/1.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2017-Q4',
            'mte': 'http://stat.data.abs.gov.au/sdmx-json/data/CPI/2.50.10001.10.Q/all?detail=DataOnly&dimensionAtObservation=AllDimensions&startPeriod=2000-Q1&endPeriod=2017-Q4'}

    DEFAULT_FILENAME = 'index_series.json'

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

    def inflate(self, single_period_param, index_obj):

        period = single_period_param.name
        print(index_obj.cpi.loc[period])
        print(index_obj.cpi.loc[period - 1])

        # inflation functions
        def x1_func(column):
            # can we access class and instance attributes here?
            # such as any indexation series
            return single_period_param[column] * -10

        def chained(column, rate):
            return single_period_param[column] * rate

        def cpi_inflate(column, series):
            return single_period_param[column] * (1 + index_obj.cpi.loc[period])

        func_mapper = {'x1_func': x1_func, 'chained': chained}
        # args_mapper = {'x2': ('x1', 0.5)}

        # since the slice of the data frame gives us a pandas Series object
        # the columns are now actually rows of the Series object

        for column in single_period_param.index:
            # index_func_name = data['param1']['index'][column]
            # func = func_mapper[index_func_name]
            # args = args_mapper.get(column, (column,))
            # args = args_mapper[column]
            # args = data['param1']['chained_args'].get(column, (column,))
            # print('column:', column)
            # print('args:', args)
            # param[column] = func(*args)
            single_period_param.loc[column] += 0.99
        return single_period_param

    def inflate_single_column(self, row_col_param, index_obj, index_method, index_args):
        def cpi_inflate(value):
            return value * (1 + rate) 

        def chained_param(column, rate):
            return 1

        row_col_param += 0.99
        return row_col_param


# ind = Index(use_api_data=True)
# print('========')
# print('this is using Index class')
# print('========')
# ind = Index(use_api_data=False)
# print(ind.indices)
# print(dir(ind))
# print(ind.cpi.head())
# print(ind.mte.head())
# ind.inflate(param1)

# print(ind.urls)
# print(Index.get_api_data('cpi'))
# print(Index.get_api_data('cpi_change'))
# print(Index.get_api_data('cpi_change_'))
