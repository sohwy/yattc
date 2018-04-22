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
        # self.set_default_policies(self.current_period)
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
        # self.rent = rent.RentAssistance.factory(period)
        for policy in self.POL_FACTORY.keys():
            # TODO: remove this later when all policy factories are built
            # need this if block for now because of NoneType not callable
            if self.POL_FACTORY[policy]:
                setattr(self,
                        policy,
                        self.POL_FACTORY[policy](pd.Period(period)))
                self.pol_map.update({policy: getattr(self, policy).__class__})
        if period != self.current_period:
            self._current_period = period

    # def set_policy(self, reform_input):
    def implement_reform(self, reform_input):
        """
        Implement reform policies
        """
        reform = self.read_reform_json(reform_input)
        period_policies = {k: v for k, v in reform['policies'].items() if not
                           k.startswith('_')}
        # for period, policies in reform['policies'].items():
        for period, policies in period_policies.items():
            # need to get rid of underscore prefixed keys
            # policies = {k: v for k, v in json_str.items() if not k.startswith('_')}
            for policy in policies:
                # if policy not in self.VALID_POLICIES:
                if policy not in self.POL_FACTORY.keys():
                    raise ValueError('Invalid policy ' +
                                     'name specified: {}'.format(policy))
                setattr(self,
                        policy,
                        self.POL_FACTORY[policy](pd.Period(period)))
                self.pol_map.update({policy: getattr(self, policy).__class__})




pol1 = Policy()
pol2 = Policy('2013Q3')
pol3 = Policy('2013Q4')
print(pol1.policies)
print(pol2.policies)
print('pol3:', pol3.policies)
z = {'policies': {'2015Q1': ['rent']}}
# pol1.set_policy(z)
pol1.implement_reform(z)
print(pol1.policies)
# pol2.set_policy('reform_params.json')
pol2.implement_reform('reform_params.json')
print(pol2.policies)
print(pol3.current_period)
pol3.set_period('2015Q1')
print(pol3.current_period)
print('pol3:', pol3.policies)
pol3.set_period('2013Q3')
print(pol3.current_period)
print('pol3:', pol3.policies)
