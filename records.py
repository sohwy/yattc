"""
Records class
"""

import json
import pandas as pd
import numpy as np
import io
import os


class Records(object):

    DEFAULT_FILENAME = 'records.csv'
    DEFAULT_START_PERIOD = '2000Q3'
    DEFAULT_END_PERIOD = '2018Q2'
    DEFAULT_METADATA = 'records_variables.json'

    def __init__(self, records=None, records_metadata=None):
        self._start = pd.Period(self.DEFAULT_START_PERIOD, freq='Q')
        self._end = pd.Period(self.DEFAULT_END_PERIOD, freq='Q')
        self._current_period = self._start

        # read records metadata
        self.read_records_metadata(records_metadata)

        # read records data
        self.read_records_data(records)

    def read_records_data(self, data):
        """
        Read in records data file and set each variable in the data file as an
        attribute of the Records object
        """
        # read in records data either from data frame or flat file
        if isinstance(data, pd.DataFrame):
            records_data = data
        elif isinstance(data, str):
            if os.path.isfile(data):
                records_data = pd.read_csv(data)
        else:
            raise ValueError('rec_data must be a data frame or a flat file')
        # set attributes of Records object
        read_vars = set()
        for variable in list(records_data.columns.values):
            data_type = self.rec_metadata['read'][variable].get('type', 'object')
            read_vars.add(variable)
            setattr(self, variable, records_data[variable].astype(data_type))
        del records_data

    def read_records_metadata(self, metadata):
        if metadata is None:
            with open(self.DEFAULT_METADATA) as f:
                self.rec_metadata = json.load(f)
        elif isinstance(metadata, dict):
            self.rec_metadata = metadata
        else:
            raise ValueError('rec_metadata is not None or dict')

    @property
    def start_period(self):
        """
        First period
        """
        return self._start

    @property
    def end_period(self):
        """
        Final period
        """
        return self._end

    @property
    def current_period(self):
        """
        Current period
        """
        return self._current_period

    def increment_period(self):
        self._current_period += 1


data = 'variable1,variable2,variable3\na,b,1\na,b,2\nc,d,3'
print('-----')
z = pd.read_csv(io.StringIO(data))
print(z)
recs = Records(records=z)
print(recs.start_period)
print(recs.current_period)
recs.increment_period()
print(recs.current_period)
print(recs.variable1)
print(recs.variable2)
print(recs.variable3)
