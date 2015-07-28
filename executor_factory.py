""""
Module with an abstract factory class.
"""

from abc import ABCMeta, abstractmethod

from crawler_api import ACMCrawlerApi, IEEECrawlerApi, SolrCrawlerApi
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

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/Log.txt"

    def create_estimator(self):
        return Mhr(SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(SolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      SolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      SolrCrawlerApi.DATA_SET_SIZE,
                      SolrCrawlerApi.LIMIT_RESULTS,
                      query_pool_file_path)


class IEEEExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/Log.txt"

    def create_estimator(self):
        return Mhr(IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(IEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      IEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      IEEECrawlerApi.DATA_SET_SIZE,
                      IEEECrawlerApi.LIMIT_RESULTS,
                      query_pool_file_path)


class ACMExecutorFactory(AbsExecutorFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACM/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACM/Log.txt"

    def create_estimator(self):
        return Mhr(ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        return Logger(ACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      ACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      ACMCrawlerApi.DATA_SET_SIZE,
                      ACMCrawlerApi.LIMIT_RESULTS,
                      query_pool_file_path)
