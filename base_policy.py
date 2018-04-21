"""
BasePolicy Class
"""

import abc
import json
import pandas as pd



class BaseClass(object, metaclass=abc.ABCMeta):

    DEFAULT_PERIODS = ["2013Q3", "2013Q4",
                       "2014Q1", "2014Q2", "2014Q3", "2014Q4",
                       "2015Q1", "2015Q2", "2015Q3", "2015Q4",
                       "2016Q1", "2016Q2", "2016Q3", "2016Q4",
                       "2017Q1", "2017Q2", "2017Q3", "2017Q4"]
    DEFAULT_PERIODS_PD = [pd.Period(x) for x in DEFAULT_PERIODS]

    DEFAULT_FILENAME = None

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
            # rfm = {k: v for k, v in json_str.items() if not k.startswith('_')}
            # return rfm
            return json_str


    # TODO: period properties

    # TODO: set_period abstract method



class BasePolicy(BaseClass, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def factory(period):
        """
        Construct an instance of the policy
        """

# z = BaseClass()
# print(z.DEFAULT_PERIODS_PD)

# class TestPolicy(BasePolicy):
# 
# 
#     @staticmethod
#     def factory(arg):
#         print('this is the factory method!')
#         if arg == 'a':
#             return PolicyA()
#         if arg == 'b':
#             return PolicyB()
#         if arg == 'c':
#             return PolicyC()
#         assert 0, 'bad arg'
# 
# 
# class PolicyA(TestPolicy): pass
# class PolicyB(TestPolicy): pass
# class PolicyC(TestPolicy): pass
# 
# 
# print(BasePolicy.DEFAULT_PERIODS)
# 
# def create_policy(period, **kwargs):
#     rasst_pol = rasst.RentAssistance.factory(kwargs.get('ra_period', period))
#     return rasst_pol
# 

# y = create_policy('a', tp_period='c')
# print(y)
# z = TestPolicy.factory('a')
# print(z.__class__.__name__)

# def create_policy(period, tp_period=None):
