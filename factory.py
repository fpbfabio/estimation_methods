from abs_factory import AbsFactory
from logger import Logger
from common_api import CommonApi
from broder_etal import BroderEtAl
# from sum_est import SumEst
# from random_walk import RandomWalk


class Factory(AbsFactory):

    def create_estimator(self):
        return BroderEtAl(CommonApi())

    def create_logger(self):
        return Logger()
