from abs_executor_factory import AbsExecutorFactory
from logger import Logger
# from ieee_abstract_common_api import IEEEAbstractCommonApi
from acm_common_api import ACMCommonApi
# from ieee_common_api import IEEECommonApi
from mhr import Mhr
# from solr_common_api import SolrCommonApi
# from broder_etal import BroderEtAl
# from sum_est import SumEst
# from random_walk import RandomWalk


class ExecutorFactory(AbsExecutorFactory):

    def create_estimator(self):
        return Mhr(ACMCommonApi())

    def create_logger(self):
        return Logger()
