"""
Parameters class
"""

import json
import datetime


class Parameters(object):
    """
    Parameters class
    """

    DEFAULT_FILENAME = 'current_parameters.json'
    FIRST_KNOWN_PERIOD = datetime.date(2000, 7, 1)
    LAST_KNOWN_PERIOD = datetime.date(2003, 3, 20)
    LAST_FORWARD_PERIOD = datetime.date(LAST_KNOWN_PERIOD.year + 3,
                                        LAST_KNOWN_PERIOD.month,
                                        LAST_KNOWN_PERIOD.day)
    DAYS_DELTA = LAST_FORWARD_PERIOD - FIRST_KNOWN_PERIOD
    DEFAULT_NUM_PERIODS = round(DAYS_DELTA.days / 91.25)

    def __init__(self, parameter_dict=None, start_year=FIRST_KNOWN_PERIOD,
                 num_years=DEFAULT_NUM_PERIODS):

        # read given parameter dictionary
        if parameter_dict is None:
            self.vals = self.read_parameter_file(Parameters.DEFAULT_FILENAME)
        elif isinstance(parameter_dict, dict):
            self.vals = parameter_dict
        else:
            raise ValueError('parameter_dict must be None or a dictionary')

        # handle num_years
        if num_years < 1:
            raise ValueError('num_years cannot be less than one')

        # initialise default parameter values
        syr = start_year.year
        lyr = start_year.year + num_years - 1
        print('initialising default paramter values')
        self.set_default_parameter_vals()

    def read_parameter_file(self, parameter_dict):
        with open(parameter_dict) as parameter_file:
            params = json.load(parameter_file)
        return params

    def initialise(self, start_year, num_years):
        pass

    def set_default_parameter_vals(self, known_years=9999999):
        for name, data in self.vals.items():
            print(name, data)
            setattr(self, name, data['value'])


p = Parameters(parameter_dict=None)
print(p.DEFAULT_FILENAME, p.FIRST_KNOWN_PERIOD, p.LAST_KNOWN_PERIOD,
      p.LAST_FORWARD_PERIOD, p.DEFAULT_NUM_PERIODS)
print('paramter values...')
print(p.vals)
print(p._param1)
print(getattr(p, '_param2'))

with open('current_parameters.json') as parameters_file:
    params = json.load(parameters_file)

print(params)
print(type(params))
