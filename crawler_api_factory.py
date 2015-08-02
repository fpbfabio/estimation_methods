""""
Module with an abstract factory class.
"""

from abc import ABCMeta, abstractmethod

from data import Data
from search_result import SearchResult
from terminator import Terminator


class AbsCrawlerApiFactory(metaclass=ABCMeta):
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

    @abstractmethod
    def create_terminator(self):
        """
        Instantiates an object derived from the AbsTerminator class.
        """
        pass


class CrawlerApiFactory(AbsCrawlerApiFactory):

    def create_search_result(self, number_results, results):
        return SearchResult(number_results, results)

    def create_data(self, identifier, content):
        return Data(identifier, content)

    def create_terminator(self):
        return Terminator()
