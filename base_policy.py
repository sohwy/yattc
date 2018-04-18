"""
BasePolicy Class
"""

import abc



class BaseClass(object, metaclass=abc.ABCMeta):

    DEFAULT_PERIODS = ["2013Q3", "2013Q4",
                       "2014Q1", "2014Q2", "2014Q3", "2014Q4",
                       "2015Q1", "2015Q2", "2015Q3", "2015Q4",
                       "2016Q1", "2016Q2", "2016Q3", "2016Q4",
                       "2017Q1", "2017Q2", "2017Q3", "2017Q4"]

    DEFAULT_FILENAME = None


class BasePolicy(BaseClass, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def factory(period):
        """
        Construct an instance of the policy
        """


class TestPolicy(BasePolicy):


    @staticmethod
    def factory(arg):
        print('this is the factory method!')
        if arg == 'a':
            return PolicyA()
        if arg == 'b':
            return PolicyB()
        if arg == 'c':
            return PolicyC()
        assert 0, 'bad arg'


class PolicyA(TestPolicy): pass
class PolicyB(TestPolicy): pass
class PolicyC(TestPolicy): pass


print(BasePolicy.DEFAULT_PERIODS)
# z = TestPolicy.factory('a')
# print(z.__class__.__name__)

# def create_policy(period, tp_period=None):
def create_policy(period, **kwargs):
    # if tp_period is None:
        # tp_period = period
    testpolicy1 = TestPolicy.factory(kwargs.get('tp_period', period))
    testpolicy2 = TestPolicy.factory(kwargs.get('tp_period2', period))
    return testpolicy1, testpolicy2

# x, y = create_policy('a', tp_period='c')
# print(x)
# print(y)


