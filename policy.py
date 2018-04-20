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

    VALID_POLICIES = ['rent']

    def __init__(self, periods=BaseClass.DEFAULT_PERIODS, *args, **kwargs):
        print(periods)
        self._start = periods[0]
        self._end = periods[-1]
        self._current_period = self._start
        print(self._current_period)

        self.set_default_policies()

        self.pol_map = {'rent': self.rent.__class__}

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
        return self.pol_map

    def set_default_policies(self, *args, **kwargs):
        """
        Set default policies

        Policies that will be initialised:
            rent.RentAssistance
            ftb.Ftb
            nsa.Nsa
        """
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

    def set_policy(self, policy_periods):
        """
        Set individual policy

        policy_periods: dict
            e.g. {period: [policy_1, policy_2, ... , policy_n]}
        """
        pol_factory = {"rent": rent.RentAssistance.factory}
        for period, policies in policy_periods.items():
            for policy in policies:
                if policy not in self.VALID_POLICIES:
                    raise ValueError('Unknown policy ' +
                                     'name specified: {}'.format(policy))
                setattr(self, policy, pol_factory[policy](period))
                self.pol_map.update({policy: getattr(self, policy).__class__})




pol1 = Policy()
pol2 = Policy()

z = {'2015Q1': ['rent']}
pol2.set_policy(z)
print(pol1.policies)
print(pol2.policies)

