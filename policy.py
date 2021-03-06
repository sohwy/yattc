"""
Policy class
"""


import pandas as pd
import re
from base_policy import BaseClass
import rent_assistance as rent


class Policy(BaseClass):
    """
    Policy class
    """
    POL_FACTORY = {
            'rent': rent.RentAssistance.factory,
            'ftb': None,
            'nsa': None
            }

    def __init__(self, period=None, periods=BaseClass.DEFAULT_PERIODS,
                 *args, **kwargs):
        self._start = pd.Period(periods[0])
        self._end = pd.Period(periods[-1])
        if period:
            self._current_period = pd.Period(period)
        else:
            self._current_period = self._start
        self.pol_map = {
                'rent': None,
                'ftb': None,
                'nsa': None
                }
        # set default policies for the current period
        self.set_period(self.current_period)

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

    # def set_default_policies(self, period):
    def set_period(self, period):
        """
        Set default policies. Can be used to initialise policies and to
        set policies to a given period.

        Policies that will be initialised:
            rent.RentAssistance
            ftb.Ftb
            nsa.Nsa
        """
        period = pd.Period(period)
        if period < self.start_period or period > self.end_period:
            raise ValueError('Policy period must be '
                             + 'between [{}, {}]'.format(self.start_period,
                                                         self.end_period))
        for policy in self.POL_FACTORY.keys():
            # TODO: remove this later when all policy factories are built
            # need this if block for now because of NoneType not callable
            if self.POL_FACTORY[policy]:
                setattr(self, policy, self.POL_FACTORY[policy](period))
                self.pol_map.update({policy: getattr(self, policy).__class__})
        self._current_period = period

    # def set_policy(self, reform_input):
    def implement_reform(self, reform_input):
        """
        Implement reform policies

        reform_input: dict, str
            Dictionary or JSON string containing the policy reform to
            implement
        """
        period_match = re.compile('\d{4,4}Q\d', re.IGNORECASE)
        reform = self.read_reform_json(reform_input)
        period_policies = {k: v for k, v in reform['policies'].items() if not
                           k.startswith('_')}
        for period, policies in period_policies.items():
            # if period is like a date e.g. 2015Q1, then convert it into a
            # pandas Period object
            if period_match.match(period):
                period = pd.Period(period)
            for policy in policies:
                if policy not in self.POL_FACTORY.keys():
                    msg = 'Invalid policy name specified: {}'
                    raise ValueError(msg.format(policy))
                setattr(self, policy, self.POL_FACTORY[policy](period))
                self.pol_map.update({policy: getattr(self, policy).__class__})




pol1 = Policy()
pol2 = Policy('2013Q3')
pol3 = Policy('2013Q4')
print('pol1:', pol1.policies)
print('pol2:', pol2.policies)
print('pol3:', pol3.policies)
# z = {'policies': {'2015Q1': ['rent']}}
z = {'policies': {'reform': ['rent']}}
# pol1.set_policy(z)
pol1.implement_reform(z)
print('pol1:', pol1.policies)
print(pol1.current_period)
# pol2.set_policy('reform_params.json')
pol2.implement_reform('reform_params.json')
print('pol2:', pol2.policies)
print(pol3.current_period)
pol3.set_period('2015Q1')
print(pol3.current_period)
print('pol3:', pol3.policies)
print(pol3.rent.calc_rent_assistance.__name__)
pol3.set_period('2013Q3')
print(pol3.current_period)
print('pol3:', pol3.policies)
print(pol3.rent.calc_rent_assistance.__name__)
