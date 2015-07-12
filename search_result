""""
Module with an abstract class that represents the result of a search.
"""

from abc import ABCMeta, abstractmethod


class AbsSearchResult(metaclass=ABCMeta):
    """"
    Class that represents the result of a search.
    """

    @property
    @abstractmethod
    def number_results(self):
        """
        The number os results.
        """
        pass

    @property
    @abstractmethod
    def results(self):
        """
        A list with the search result data .
        """
        pass
