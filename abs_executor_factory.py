""""
Module with an abstract factory class.
"""

from abc import ABCMeta, abstractmethod


class AbsExecutorFactory(metaclass=ABCMeta):
    """"
    Factory class.
    """

    @abstractmethod
    def create_estimator(self):
        """
        Instantiates an object derived from the AbsEstimator class.
        """
        pass

    @abstractmethod
    def create_logger(self):
        """
        Instantiates an object derived from the AbsLogger class.
        """
        pass
