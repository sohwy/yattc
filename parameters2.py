
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
                short_name = data['short_name']
                inflation_rates = self.vals.get('index_method')
                if len(values) != self._num_cur_periods:
                    msg = 'Incorrect number of parameter values specified ' \
                          'in the parameter: {}'
                    raise ValueError(msg.format(param))
                setattr(self, param, self.expand_array(values,
                                                       inflation_rates,
                                                       self._num_periods,
                                                       short_name))
            self.set_period(self.current_period.year,
                            self.current_period.quarter)

    def expand_array(self, vals, inflation_rates, expanded_dim, param_name):
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
        # Create array of NaNs of length equal to the dimension of the
        # expanded parameter array
        expanded_param = pd.Series(np.full(expanded_dim, np.nan),
                                   pd.PeriodIndex(start=self.current_period,
                                                  periods=expanded_dim,
                                                  freq='Q'),
                                   name=param_name)
        # Replace NaN values with actual parameter values
        expanded_param[:len(vals)] = vals
        # Propogate the last known parameter value forward and inflate
        # iteratively replacing each of the NaNs
        for i in range(len(vals), expanded_dim):
            expanded_param.iloc[i] = expanded_param.iloc[i-1]
        return expanded_param

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
            current_vals = getattr(self, param, None)
            new_vals = self.expand_array(values, inflation_rates,
                                         expanded_dim, param)
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
# import io
# output = io.StringIO()
# with open('reform_params.json') as f:
#     for line in f:
#         if not line.lstrip().startswith('//'):
#             output.write(line)
#     reform = json.loads(output.getvalue())
# 
# print(reform)

reform = p.read_reform_json('reform_params.json')
print(reform)
p.implement_reforms(reform)







# print(p._start, p.start_period)
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
# print(p._param_3)
print(p.param_3)
# 
# print(' ')
# print(type(p._start), p.start_period)
# print(p.start_period.ordinal)
# print(' ')
# p.set_period(2004, 4)
# print(p.current_period)
# print(p.param_1)
# 
# 
# p.set_period(1999, 4)










# print(p._periods, p._start, p._end, p.vals)
# print(p.periods)

# with open('test_params.json') as f:
#     params = json.load(f)
# 
# print(params)
# print(params['param_a']['values'])
# 
# start_qtr = "2000Q3"
# end_qtr = "2004Q2"
# fwd_len = 4
# cur_len = 16
# tot_len = fwd_len + cur_len
# 
# def expand_array2(param):
#     ans = np.full(tot_len, np.nan)
#     ans = pd.Series(ans, pd.PeriodIndex(start=start_qtr, periods=tot_len, freq='Q'))
#     ans[:cur_len] = params['param_q']['values']
# 
# print(ans)
# 
# def inflate_value(value, current_quarter, method):
#     print(current_quarter)
#     if current_quarter in params['param_q']['index_quarters']:
#         return inflate_mapping[method](value)
#     return value
# 
# def inflate_cpi(value):
#     return value + 0.1
# 
# def inflate_mtawe(value):
#     return value - 0.1
# 
# inflate_mapping = {"cpi": inflate_cpi, "mtawe": inflate_mtawe}
# 
# for i in range(cur_len, tot_len):
#     ans.iloc[i] = inflate_value(ans.iloc[i-1], ans.index[i].quarter, "cpi")
# 
# print(ans)
