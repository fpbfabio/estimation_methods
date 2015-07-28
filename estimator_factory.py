""""
Module with an abstract factory class.
"""

from abc import ABCMeta, abstractmethod

from parallelizer import Parallelizer
from word_extractor import WordExtractor


class AbsEstimatorFactory(metaclass=ABCMeta):
    """"
    Factory class.
    """

    @abstractmethod
    def create_parallelizer(self):
        """
        Instantiates an object derived from the AbsParallelizer class.
        """
        pass

    @abstractmethod
    def create_word_extractor(self):
        """
        Instantiates an object derived from the AbsWordExtractor class.
        """
        pass


class EstimatorFactory(AbsEstimatorFactory):

    def create_parallelizer(self):
        return Parallelizer()

    def create_word_extractor(self):
        return WordExtractor()
