from abs_factory import AbsFactory
from commom_api import CommomApi
from sum_est import SumEst


class Factory(AbsFactory):

	def create_commom_api(self):
		return CommomApi()

	def create_estimator(self, commom_api):
		return SumEst(commom_api)