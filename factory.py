from abs_factory import AbsFactory
from commom_api import CommomApi
from broder_etal import BroderEtAl
from sum_est import SumEst
from random_walk import RandomWalk


class Factory(AbsFactory):

	def create_commom_api(self):
		return CommomApi()

	def create_estimator(self, commom_api):
		return BroderEtAl(commom_api)