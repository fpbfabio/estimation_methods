""""
This is the module that provides an abstract interface for a class
with the functions used in common in all estimators.
"""

from abc import ABCMeta, abstractmethod

from config import Config


class AbsCommonApi(metaclass=ABCMeta):
    """
    Contains common methods that are needed by all estimation algorithm classes.
    """

    @property
    @abstractmethod
    def download_count(self):
        """
        Returns the number of downloads.
        """
        pass

    @download_count.setter
    @abstractmethod
    def download_count(self, val):
        """
        Sets the number of downloads.
        """
        pass

    @property
    @abstractmethod
    def factory(self):
        """
        Returns the instance of an AbsCommonApiFactory class.
        """
        pass

    @factory.setter
    @abstractmethod
    def factory(self, val):
        """
        Sets the instance of an AbsCommonApiFactory class.
        """
        pass

    @abstractmethod
    def read_query_pool(self):
        """
        Returns a list with the queries specified in the query pool file,
        whose path is set in the Config class.
        """
        pass

    @abstractmethod
    def download_entire_data_set(self):
        """
        Returns a list with all the documents from the data set.
        """
        pass

    @abstractmethod
    def retrieve_number_matches(self, query):
        """
        Returns the number of matches in the search engine for the given query.
        """
        pass

    @abstractmethod
    def download(self, query, is_to_download_id=True, is_to_download_content=True, limit=Config.SEARCH_ENGINE_LIMIT):
        """
        Returns the a list with documents retrieved by the given query with
        the max size set by the given limit.
        """
        pass

    @abstractmethod
    def execute_in_parallel(self, collection, callback):
        """
        Executes a function in multiple threads, for each thread
        the callback receives an item from the collection.
        """
        pass

    @abstractmethod
    def report_progress(self, progress, total):
        """
        Gives a feedback about the progress of the estimation.
        """
        pass

    @abstractmethod
    def extract_words(self, text):
        """
        Returns the words in the text as keys of a dictionary.
        """
        pass
