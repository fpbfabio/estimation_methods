from abs_executer import AbsExecuter
from factory import Factory


class Executer(AbsExecuter):

	def __init__(self):
		self.factory = Factory()
		self.estimator = None

	@property
	def factory(self):
		return self.__factory

	@factory.setter
	def factory(self, val):
		self.__factory = val

	@property
	def estimator(self):
		return self.__estimator

	@estimator.setter
	def estimator(self, val):
		self.__estimator = val

	def execute(self):
		commom_api = self.factory.create_commom_api()
		self.estimator = self.factory.create_estimator(commom_api)
		self.estimator.estimate()


if __name__ == "__main__":
	executer = Executer()
	for i in range(0, 20):
		executer.execute()