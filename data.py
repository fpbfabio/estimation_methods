""""
Module with an abstract class that represents the data taken from a search engine.
"""

from abc import ABCMeta, abstractmethod


class AbsData(metaclass=ABCMeta):
    """"
    Class that represents the data taken from a search engine.
    """

    @property
    @abstractmethod
    def identifier(self):
        """
        A unique identifier for the data in the scope of the search engine.
        """
        pass

    @property
    @abstractmethod
    def content(self):
        """
        Text content of the data.
        """
        pass


class Data(AbsData):

    def __init__(self, identifier, content):
        self.__identifier = identifier
        self.__content = content

    @property
    def identifier(self):
        return self.__identifier

    @property
    def content(self):
        return self.__content
