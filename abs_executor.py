""""
This is the module that provides an abstract interface for a
class used to obtain estimations of the size of a data set.
"""

from abc import ABCMeta, abstractmethod


class AbsExecutor(metaclass=ABCMeta):
    """
    Class used to execute the program.
    """

    @property
    @abstractmethod
    def logger(self):
        """
        Returns the instance of an AbsLogger class.
        """
        pass

    @logger.setter
    @abstractmethod
    def logger(self, val):
        """
        Sets the instance of an AbsLogger class.
        """
        pass

    @property
    @abstractmethod
    def factory(self):
        """
        Returns the instance of an AbsFactory class.
        """
        pass

    @factory.setter
    @abstractmethod
    def factory(self, val):
        """
        Sets the instance of an AbsFactory class.
        """
        pass

    @property
    @abstractmethod
    def estimator(self):
        """
        Returns the instance of an AbsEstimator class.
        """
        pass

    @estimator.setter
    @abstractmethod
    def estimator(self, val):
        """
        Sets the instance of an AbsEstimator class.
        """
        pass

    @abstractmethod
    def execute(self):
        """
        Executes the code.
        """
        pass
