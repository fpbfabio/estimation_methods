from abc import ABCMeta, abstractmethod

from crawler_api import SolrCrawlerApi, ACMOnlyAbstractCrawlerApi, AbsACMCrawlerApi, ACMOnlyTitleCrawlerApi, \
    ACMCrawlerApi, IEEEOnlyAbstractCrawlerApi, AbsIEEECrawlerApi, IEEEOnlyTitleCrawlerApi, IEEECrawlerApi
from data import Data
from estimator import Mhr
from logger import Logger
from parallelizer import Parallelizer
from path_dictionary import WindowsPathDictionary
from search_result import SearchResult
from terminator import Terminator
from word_extractor import WordExtractor


class AbsFactory(metaclass=ABCMeta):

    @abstractmethod
    def create_search_result(self, number_results, results):
        pass

    @abstractmethod
    def create_data(self, identifier, content):
        pass

    @abstractmethod
    def create_terminator(self):
        pass

    @abstractmethod
    def create_parallelizer(self):
        pass

    @abstractmethod
    def create_word_extractor(self):
        pass

    @abstractmethod
    def create_estimator(self):
        pass

    @abstractmethod
    def create_logger(self, query_pool_file_path):
        pass

    @abstractmethod
    def create_path_dictionary(self):
        pass


class AbsExceptionFactory(AbsFactory, metaclass=ABCMeta):

    def create_search_result(self, number_results, results):
        raise NotImplementedError()

    def create_data(self, identifier, content):
        raise NotImplementedError()

    def create_terminator(self):
        raise NotImplementedError()

    def create_parallelizer(self):
        raise NotImplementedError()

    def create_word_extractor(self):
        raise NotImplementedError()

    def create_estimator(self):
        raise NotImplementedError()

    def create_logger(self, query_pool_file_path):
        raise NotImplementedError()

    def create_path_dictionary(self):
        raise NotImplementedError()


class AbsBaseFactory(AbsExceptionFactory, metaclass=ABCMeta):

    def create_search_result(self, number_results, results):
        return super().create_search_result(number_results, results)

    def create_data(self, identifier, content):
        return super().create_data(identifier, content)

    def create_terminator(self):
        return super().create_terminator()

    def create_parallelizer(self):
        return super().create_parallelizer()

    def create_word_extractor(self):
        return super().create_word_extractor()

    def create_estimator(self):
        return super().create_estimator()

    def create_logger(self, query_pool_file_path):
        return super().create_logger(query_pool_file_path)

    def create_path_dictionary(self):
        return WindowsPathDictionary()


class SolrExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "SolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(SolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(SolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      SolrCrawlerApi.get_data_set_size(),
                      SolrCrawlerApi.LIMIT_RESULTS)


class IEEEExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "IEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "IEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(IEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(IEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      AbsIEEECrawlerApi.get_data_set_size(),
                      AbsIEEECrawlerApi.LIMIT_RESULTS)


class IEEEOnlyTitleExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "IEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "IEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(IEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(IEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      AbsIEEECrawlerApi.get_data_set_size(),
                      AbsIEEECrawlerApi.LIMIT_RESULTS)


class IEEEOnlyAbstractExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(IEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(IEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      AbsIEEECrawlerApi.get_data_set_size(),
                      AbsIEEECrawlerApi.LIMIT_RESULTS)


class ACMExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "ACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(ACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(ACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      AbsACMCrawlerApi.get_data_set_size(),
                      AbsACMCrawlerApi.LIMIT_RESULTS)


class ACMOnlyTitleExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "ACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(ACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(ACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      AbsACMCrawlerApi.get_data_set_size(),
                      AbsACMCrawlerApi.LIMIT_RESULTS)


class ACMOnlyAbstractExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "ACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return Mhr(ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dictionary = self.create_path_dictionary()
        return Logger(path_dictionary.get_path(ACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                      path_dictionary.get_path(ACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                      AbsACMCrawlerApi.get_data_set_size(),
                      AbsACMCrawlerApi.LIMIT_RESULTS)


class EstimatorFactory(AbsBaseFactory):

    def create_parallelizer(self):
        return Parallelizer()

    def create_word_extractor(self):
        return WordExtractor()


class CrawlerApiFactory(AbsBaseFactory):

    def create_search_result(self, number_results, results):
        return SearchResult(number_results, results)

    def create_data(self, identifier, content):
        return Data(identifier, content)

    def create_terminator(self):
        return Terminator()
