""""Module with an abstract factory class."""

from abc import ABCMeta, abstractmethod


class AbsFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_estimator(self):
        """Instantiates an object derived from the AbsEstimator class."""
        pass
