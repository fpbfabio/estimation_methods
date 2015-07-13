from abs_executor_factory import AbsExecutorFactory
from logger import Logger
from common_api import CommonApi
# from broder_etal import BroderEtAl
# from sum_est import SumEst
from random_walk import RandomWalk


class ExecutorFactory(AbsExecutorFactory):

    def create_estimator(self):
        return RandomWalk(CommonApi())

    def create_logger(self):
        return Logger()
