"""
BasePolicy Class
"""

import abc


class BasePolicy(object, metaclass=abc.ABCMeta):

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


# z = TestPolicy.factory('a')
# print(z.__class__.__name__)

# def create_policy(period, tp_period=None):
def create_policy(period, **kwargs):
    # if tp_period is None:
        # tp_period = period
    testpolicy1 = TestPolicy.factory(kwargs.get('tp_period', period))
    testpolicy2 = TestPolicy.factory(kwargs.get('tp_period2', period))
    return testpolicy1, testpolicy2

x, y = create_policy('a', tp_period='c')
print(x)
print(y)


