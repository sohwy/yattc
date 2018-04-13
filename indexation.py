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
        # read in index values
        if indices_dict is None:
            with open(self.DEFAULT_FILENAME) as f:
                self.indices = json.load(f)
        elif isinstance(indices_dict, dict):
            self.indices = indices_dict
        else:
            raise ValueError('indices_dict must be None or a dictionary')
        # set index series data
        self.set_default_series_vals(use_api_data)
        # array of final periods to check parameters and index series values
        # are properly aligned when an Index class is instantiated by
        # the Parameters class
        self.final_periods = np.array((self.cpi.index[-1],
                                       self.mte.index[-1]))

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
                    # TODO: properly catch mismatched period index and
                    # value length
                    assert len(idx) == len(data['values'])
                    index_df = pd.DataFrame(data['values'],
                                            index=idx,
                                            columns=['values'])
                    # calculate percentage change
                    index_df['pct_change'] = \
                        round(index_df['values'].pct_change(), 4)
                    # assign values to attribute of Index object
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


# ind = Index(use_api_data=True)
# print('========')
# print('this is using Index class')
# print('========')
ind = Index(use_api_data=False)
print(ind.indices)
# print(dir(ind))
print(ind.cpi)
print(ind.mte)
print(ind.final_periods)

# print(len(ind.cpi))
# print(ind.urls)
# print(Index.get_api_data('cpi'))
# print(Index.get_api_data('cpi_change'))
# print(Index.get_api_data('cpi_change_'))
