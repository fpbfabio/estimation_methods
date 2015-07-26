""""
Module with an abstract factory class.
"""

from abc import ABCMeta, abstractmethod


class AbsCommonApiFactory(metaclass=ABCMeta):
    """"
    Factory class.
    """

    @abstractmethod
    def create_search_result(self, number_results, results):
        """
        Instantiates an object derived from the AbsSearchResult class.
        """
        pass

    @abstractmethod
    def create_data(self, identifier, content):
        """
        Instantiates an object derived from the AbsData class.
        """
        pass
