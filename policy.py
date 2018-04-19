"""
Policy class
"""


import pandas as pd
from base_policy import BaseClass
import rent_assistance as rent


class Policy(BaseClass):
    """
    Policy class
    """

    REQUIRED_POLICIES = ['rent']

    def __init__(self, periods=BaseClass.DEFAULT_PERIODS, *args, **kwargs):
        print(periods)
        self._start = periods[0]
        self._end = periods[-1]
        self._current_period = self._start
        print(self._current_period)

        self.init_policies()

        self.policies_dict = {'rent_assistance': self.rent.__class__}

    @property
    def start_period(self):
        return self._start

    @property
    def end_period(self):
        return self._end

    @property
    def current_period(self):
        return self._current_period

    @property
    def policies(self):
        return self.policies_dict

    def init_policies(self, *args, **kwargs):
        self.rent = \
            rent.RentAssistance.factory(kwargs.get('ra_pd',
                                                   self._current_period))

    def set_period(self, target_period):
        """
        Set policies to policies in the target period

        Parameters
        ----------

        Notes
        -----

        """
        period = pd.Period(target_period, freq='Q')
        # check that period is within valid range
        if period < self.start_period or period > self.end_period:
            raise ValueError('Policy period must be '
                             + 'between [{}, {}]'.format(self.start_period,
                                                         self.end_period))
        # set the policies to the policies for the given # input period
        if hasattr(self, 'vals'):
            for param in self.vals:
                value_array = getattr(self, param)
                setattr(self, param[1:], value_array.loc[period])
            self._current_period = period

    def set_policy(self):
        """
        Set individual policy
        """
        pass



pol1 = Policy()
pol2 = Policy()

# print(dir(pol.rent))
print(pol1.policies)
print(pol2.policies)

