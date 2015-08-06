""""
Module with an abstract factory class.
"""

from abc import ABCMeta, abstractmethod

from crawler_api import ACMCrawlerApi, AbsIEEECrawlerApi, IEEECrawlerApi, SolrCrawlerApi, IEEEOnlyTitleCrawlerApi, \
    AbsACMCrawlerApi, ACMOnlyTitleCrawlerApi
from estimator import Mhr
from logger import Logger


class AbsExecutorFactory(metaclass=ABCMeta):
    """"
    Factory class.
    """

    @abstractmethod
    def create_estimator(self):
        """
        Instantiates an object derived from the AbsEstimator class.
        """
        pass

    @abstractmethod
    def create_logger(self, query_pool_file_path):
        """
        Instantiates an object derived from the AbsLogger class.
        """
        pass


class SolrExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/Solr/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/Solr/Log.txt"

    def create_estimator(self):
        return Mhr(SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(SolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      SolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      SolrCrawlerApi.DATA_SET_SIZE,
                      SolrCrawlerApi.LIMIT_RESULTS)


class IEEEExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/Log.txt"

    def create_estimator(self):
        return Mhr(IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(IEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      IEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      AbsIEEECrawlerApi.get_data_set_size(),
                      AbsIEEECrawlerApi.LIMIT_RESULTS)


class IEEEOnlyTitleExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEEOnlyTitle/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEEOnlyTitle/Log.txt"

    def create_estimator(self):
        return Mhr(IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(IEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      IEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      AbsIEEECrawlerApi.get_data_set_size(),
                      AbsIEEECrawlerApi.LIMIT_RESULTS)


class ACMExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACM/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACM/Log.txt"

    def create_estimator(self):
        return Mhr(ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(ACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      ACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      AbsACMCrawlerApi.DATA_SET_SIZE,
                      AbsACMCrawlerApi.LIMIT_RESULTS)


class ACMOnlyTitleExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACMOnlyTitle/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACMOnlyTitle/Log.txt"

    def create_estimator(self):
        return Mhr(ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(ACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      ACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      AbsACMCrawlerApi.DATA_SET_SIZE,
                      AbsACMCrawlerApi.LIMIT_RESULTS)
