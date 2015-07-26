""""
This is the module that provides an abstract interface for a class used to obtain
estimations of the size of a data set.
"""

from abc import ABCMeta, abstractmethod


class AbsEstimator(metaclass=ABCMeta):
    """
    Class used to estimate the size of a data set.
    """

    @property
    @abstractmethod
    def common_api(self):
        """
        Returns the instance of an AbsCommon object.
        """
        pass

    @common_api.setter
    @abstractmethod
    def common_api(self, val):
        """
        Sets the instance of an AbsCommon object.
        """
        pass

    @abstractmethod
    def estimate(self):
        """
        Returns the estimation of the size of the data set.
        """
        self.common_api.download_count = 0

    @property
    @abstractmethod
    def experiment_details(self):
        """
        Returns the parameters used in the experiment.
        """
        pass

    @property
    def download_count(self):
        return self.common_api.download_count
