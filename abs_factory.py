""""Module with an abstract factory class."""

from abc import ABCMeta, abstractmethod

class AbsFactory(metaclass=ABCMeta):

	@abstractmethod
	def create_commom_api(self):
		"""Instantiates an object derived from the AbsCommomApi class."""
		pass

	@abstractmethod
	def create_estimator(self, commom_api):
		"""Instantiates an object derived from the AbsEstimator class."""
		pass