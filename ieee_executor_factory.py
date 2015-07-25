from abs_executor_factory import AbsExecutorFactory
from ieee_abstract_common_api import IEEEAbstractCommonApi
from logger import Logger
from mhr import Mhr


class IEEEExecutorFactory(AbsExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/ExperimentResults.csv"
    _EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/IEEE/Log.txt"

    def create_estimator(self):
        return Mhr(IEEEAbstractCommonApi())

    def create_logger(self):
        return Logger(IEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH,
                      IEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH,
                      IEEEAbstractCommonApi.DATA_SET_SIZE,
                      IEEEAbstractCommonApi.QUERY_POOL_FILE_PATH)
