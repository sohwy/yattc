
"""
Parameters class
"""

import json
import pandas as pd
import numpy as np


class Parameters(object):
    """
    Parameters class
    """

    DEFAULT_FILENAME = 'test_params.json'
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

    def __init__(self, parameter_dict=None, periods=DEFAULT_PERIODS,
                 num_fwd_periods=DEFAULT_NUM_FWD_PERIODS):
#this is param-arrays branch
#         self._periods = periods
#         self._start = periods[0]
#         self._end = periods[-1]
#         self._current_period = self._start
        self._num_cur_periods = len(periods)
        self._num_fwd_periods = num_fwd_periods
        self._num_periods = self._num_cur_periods + self._num_fwd_periods
        # self._periods =  pd.Series(range(0, self._num_periods),
        #                            pd.PeriodIndex(start=self._start,
        #                                           periods=self._num_periods,
        #                                           freq='Q'))
        self._periods = pd.Series(range(0, self._num_periods),
                                  pd.PeriodIndex(start=periods[0],
                                                 periods=self._num_periods,
                                                 freq='Q'))
        self._start = self._periods.index[0]
        self._end = self._periods.index[-1]
        # self._start = pd.Period(periods[0], freq='Q')
        # self._end = pd.Period(periods[-1], freq='Q')
        self._current_period = self._start


        # Read in parameters
        if parameter_dict is None:
            with open(Parameters.DEFAULT_FILENAME) as f:
                self.vals = json.load(f)
        elif isinstance(parameter_dict, dict):
            self.vals = parameter_dict
        else:
            raise ValueError('parameter_dict must be None or a dictionary')

        # Set default parameter values after padding and inflating known values
        self.set_default_parameter_vals()

    @property
    def periods(self):
        """
        Date range for which parameters have values
        """
        return self._periods

    @property
    def start_period(self):
        """
        First period in which parameter values are known
        """
        # return self.periods.index[0]
        return self._start

    @property
    def end_period(self):
        """
        Final period in which parameter values are known
        """
        # return self.periods.index[-1]
        return self._end

    @property
    def current_period(self):
        """
        Current period
        """
        return self._current_period

    def set_default_parameter_vals(self):
        """
        Set as attributes the array of values for each parameter
        """
        if hasattr(self, 'vals'):
            for param, data in self.vals.items():
                print(param, data)
                values = data['values']
                column_names = data.get('columns', ['Values'])
                inflation_rates = data.get('index_method', None)
                if len(values) != self._num_cur_periods:
                    msg = 'Incorrect number of parameter values specified ' \
                          'in the parameter: {}'
                    raise ValueError(msg.format(param))
                setattr(self, param, self.expand_array(values,
                                                       inflation_rates,
                                                       column_names,
                                                       self._num_periods))
            self.set_period(self.current_period.year,
                            self.current_period.quarter)

    def expand_array(self, vals, inflation_rates, cols, expanded_rows):
        """
        Expand the given parameter vector to cover the forward period and
        inflate the parameter values

        Parameters
        ----------
        vals: list, numpy array
            List or numpy array of parameter values
        inflation_rates: list, numpy array
            List or numpy array of inflation rates to apply to vals
        expanded_dim: int
            Dimension of expanded parameter array
        param_name: str
            Descriptive name for the parameter

        Notes
        -----

        TODO
        ----
        (1)
            Add inflation

        (2)
            Set the data type for the pandas array
        """
        param = pd.DataFrame(vals,
                             index=pd.PeriodIndex(start=self.current_period,
                                                  periods=len(vals),
                                                  freq='Q'),
                             columns=cols)
        param = param.reindex(pd.PeriodIndex(start=self.current_period,
                                             periods=expanded_rows,
                                             freq='Q'))
        for i in range(len(vals), expanded_rows):
            param.iloc[i] = param.iloc[i-1]
        return param

    def set_period(self, target_year, target_quarter):
        """
        Set as attributes the values of each parameter for the current period

        Parameters
        ----------
        target_year : int
            Year of parameter period (e.g., 2000)

        target_quarter : int
            Quarter of parameter period (e.g., 4)

        Notes
        -----

        (1)
            The attribute being set is the parameter name without the leading
            underscore.
        """
        period = pd.Period(year=target_year, quarter=target_quarter, freq='Q')
        # check that period is within valid range
        if period < self.start_period or period > self.end_period:
            raise ValueError('Parameter period must be '
                             + 'between [{}, {}]'.format(self.start_period,
                                                         self.end_period))
        # set the parameter values to the parameter values for the given
        # input parameter period
        if hasattr(self, 'vals'):
            for param in self.vals:
                value_array = getattr(self, param)
                setattr(self, param[1:], value_array.loc[period])
            self._current_period = period

    def implement_forwards(self, forwards):
        """
        Implement forward period parameters by overwriting the default
        current legislated parameter values
        """
        pass

    def implement_reforms(self, reform):
        """
        Implement reform parameters by overwriting the parameter values

        Parameters
        ----------
        reform: valid reform dictionary
            Contains {period: {parameter: value}} pairs

        Notes
        -----

        TODO
        ----

        """
        if not isinstance(reform, dict):
            raise ValueError('Reform is not a dictionary')
        if reform is None:
            return
        reform_periods = sorted(list(reform.keys()))
        print(reform_periods)
        # check first reform period
        if pd.Period(reform_periods[0], freq='Q') < self.start_period:
            raise ValueError('Reform period must '
                             + 'be after {}'.format(self.start_period))
        # check last reform period
        if pd.Period(reform_periods[-1], freq='Q') > self.end_period:
            raise ValueError('Reform period must '
                             + 'be before {}'.format(self.end_period))
        # validate parameter reform names and types

        # implement the reforms period by period
        precall_current_period = self.current_period
        for period in reform_periods:
            self._current_period = pd.Period(period, freq='Q')
            self.update_parameter(period, reform[period])
        self.set_period(precall_current_period.year,
                        precall_current_period.quarter)

    def update_parameter(self, period, param_val_dict):
        """
        docstring
        input is a {period: {param: val},...,{param: val}} dict
        """
        # calculate dimension required for the expanded array
        expanded_dim = self.periods.iloc[-1] - self.periods.loc[period] + 1
        # iterate through each param: val pair in the reforms for the period
        # and overwrite the existing value in self.vals with the new values
        for param, values in param_val_dict.items():
            if param not in self.vals.keys():
                raise NameError('{} not a valid parameter name'.format(param))
            if not isinstance(values, list):
                raise ValueError('Parameter values must be a list')
            inflation_rates = self.vals.get('index_method')
            # idx = pd.PeriodIndex(start=self.current_period,
            #                      periods=len(values),
            #                      freq='Q')
            column_names = self.vals[param].get('columns', ['Values'])
            current_vals = getattr(self, param, None)
            new_vals = self.expand_array(values, inflation_rates,
                                         column_names, expanded_dim)
            current_vals[self.periods.loc[period]:] = new_vals

    def read_reform_json(self, reform_json):
        """
        Read in JSON file with reform parameters

        Parameters
        ----------
        reform_json : valid JSON file
            Contains {period: {parameter: value}} pairs

        Notes
        -----
        Can also be used to read in forward parameter files

        TODO
        ----
        (1)
            Validate parameter values and names

        (2)
            Proper exception handling

        (3)
            Validate period values
        """
        with open(reform_json) as f:
            json_str = json.load(f)
            # all comments should be objects whose name begin with underscore
            rfm = {k: v for k, v in json_str.items() if not k.startswith('_')}
            return rfm




p = Parameters()

reform = p.read_reform_json('reform_params.json')
print(reform)
p.implement_reforms(reform)

print(type(p._start))
# print(p._end, p.end_period)
# print(p._current_period, p.current_period)
print(p._periods, p.periods)
# print(p.vals.keys())
# print(dir(p))
print(p._param_1)
print(p.param_1)
print(p._param_2)
print(p.param_2)
print(p._param_3)
print(p.param_3)
