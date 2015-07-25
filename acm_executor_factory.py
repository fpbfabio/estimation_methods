from abs_executor_factory import AbsExecutorFactory
from acm_common_api import ACMCommonApi
from logger import Logger
from mhr import Mhr


class ACMExecutorFactory(AbsExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACM/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ACM/Log.txt"

    def create_estimator(self):
        return Mhr(ACMCommonApi())

    def create_logger(self):
        return Logger(ACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      ACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      ACMCommonApi.DATA_SET_SIZE,
                      ACMCommonApi.QUERY_POOL_FILE_PATH)
