""""This is the module that provides an abstract interface for a class used to obtain estimations of the size of a dataset."""

from abc import ABCMeta, abstractmethod


class AbsEstimator(metaclass=ABCMeta):
	"""Class used to estimate the size of a dataset."""

	@property
	@abstractmethod
	def commom_api(self):
		"""Returns the instance of an AbsCommom object."""
		pass

	@commom_api.setter
	@abstractmethod
	def commom_api(self, val):
		"""Sets the instance of an AbsCommom object."""
		pass

	@abstractmethod
	def estimate(self):
		"""Returns the estimation of the size of the dataset."""
		pass