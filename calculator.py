"""
Calculator class
"""

import pandas as pd
import numpy as np
import copy
import io


# import yattc modules
from records import Records
from parameters import Parameters


class Calculator(object):
    def __init__(self, records=None, parameters=None, policy=None):
        # initialise embedded Records object
        if records is None:
            self.records = Records()
        elif isinstance(records, Records):
            self.records = copy.deepcopy(records)
        else:
            raise ValueError('records must be None or a Records object')
        self.stored_records = None
        # initialise embedded Parameters object
        if parameters is None:
            self.parameters = Parameters()
        elif isinstance(parameters, Parameters):
            self.parameters = copy.deepcopy(parameters)
        else:
            raise ValueError('parameters must be None or a Parameters object')
        # TODO: initialise Policy object

    def index_series(self, series):
        """
        Get index series from embedded Parameters object
        """
        return getattr(self.parameters.ind, series)

    def store_records(self, verbose=False):
        """
        Store embedded Records object
        """
        assert self.stored_records is None
        self.stored_records = copy.deepcopy(self.records)
        if verbose:
            print('Current embedded Records object stored')

    def restore_records(self, verbose=False):
        """
        Restore the embedded Records object to the stored copy made when
        store_records method was called
        """
        if not isinstance(self.stored_records, Records):
            raise AssertionError('there is no stored Records object')
        else:
            self.records = copy.deepcopy(self.stored_records)
            del self.stored_records
            self.stored_records = None
            if verbose:
                print('Embedded Records object restored')

    def get_value_attrs(self, value):
        """
        Method to get attributes of passed in value
        """
        return value.shape, value.dtype, value.index, type(value)

    def param(self, parameter, parameter_value=None):
        """
        Return named parameter from embedded Parameters object or change the
        value of the parameter in the embedded Parameters object.

        NOTES
        -----
        Changing the value of the parameter only affects the current period
        parameter value. No indexation is applied to subsequent periods.
        """

        err_msg = 'attributes of new parameter values for {} do not match ' \
                  'current value attributes'

        # no parameter value passed in, return current value
        if parameter_value is None:
            return getattr(self.parameters, parameter)
        # attributes of parameter value passed in do not match
        elif not isinstance(parameter_value, pd.Series) or \
            self.get_value_attrs(parameter_value) != \
                self.get_value_attrs(getattr(self.parameters, parameter)):
            raise ValueError(err_msg.format(parameter))
        # attributes match, change parameter value
        else:
            setattr(self.parameters, parameter, parameter_value)

    def var(self, variable, variable_value=None):
        """
        Return named variable from embedded Records object or change the
        value of the variable in the embedded Records object.
        """

        err_msg = 'attributes of new variable values for {} do not match ' \
                  'current value attributes'

        # no parameter value passed in, return current value
        if variable_value is None:
            return getattr(self.records, variable)
        # attributes of variable value passed in do not match
        elif not isinstance(variable_value, pd.Series) or \
            self.get_value_attrs(variable_value) != \
                self.get_value_attrs(getattr(self.records, variable)):
            raise ValueError(err_msg.format(variable))
        # attributes match, change variable value
        else:
            setattr(self.records, variable, variable_value)



data = 'variable1,variable2,variable3\na,b,1\na,b,2\nc,d,3'
z = pd.read_csv(io.StringIO(data))
recs = Records(records=z)
calc = Calculator(records=recs)
print(calc.records)
print(calc.parameters)

print(calc.param('param_1'))
calc.param('param_1', 1 + calc.parameters.param_1)
print(calc.param('param_1'))
# calc.param('param_1', 10)
print(calc.var('variable3'))
calc.var('variable3', 1 + calc.records.variable3)
print(calc.var('variable3'))
# calc.var('variable1', 'a')
