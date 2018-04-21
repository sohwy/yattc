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

    def __init__(self, period=None, periods=BaseClass.DEFAULT_PERIODS,
                 *args, **kwargs):
        print(periods)
        self._start = pd.Period(periods[0])
        self._end = pd.Period(periods[-1])
        print(self._start, self._end)
        if period:
            self._current_period = pd.Period(period)
        else:
            self._current_period = self._start
        print(self._current_period)

        self.set_default_policies(self.current_period)

        self.pol_map = {
                'rent': self.rent.__class__,
                'ftb': None,
                'nsa': None
                }

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

    def set_default_policies(self, period):
        """
        Set default policies

        Policies that will be initialised:
            rent.RentAssistance
            ftb.Ftb
            nsa.Nsa
        """
        if period < self.start_period or period > self.end_period:
            raise ValueError('Policy period must be '
                             + 'between [{}, {}]'.format(self.start_period,
                                                         self.end_period))
        self.rent = rent.RentAssistance.factory(period)
        if period != self.current_period:
            self.current_period = period

    def set_policy(self, policy_periods):
        """
        Set individual policy

        policy_periods: dict
            e.g. {period: [policy_1, policy_2, ... , policy_n]}
        """
        pol_factory = {
                'rent': rent.RentAssistance.factory,
                'ftb': None,
                'nsa': None
                }
        for period, policies in policy_periods.items():
            for policy in policies:
                if policy not in self.VALID_POLICIES:
                    raise ValueError('Invalid policy ' +
                                     'name specified: {}'.format(policy))
                setattr(self, policy, pol_factory[policy](pd.Period(period)))
                self.pol_map.update({policy: getattr(self, policy).__class__})




pol1 = Policy()
pol2 = Policy('2015Q3')

reform = pol1.read_reform_json('reform_params.json')
print(reform)

z = {'2015Q1': ['rent']}
pol2.set_policy(z)
print(pol1.policies)
print(pol2.policies)
print(pol2.current_period)
