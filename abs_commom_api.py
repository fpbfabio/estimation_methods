""""This is the module that provides an abstract interface for a class with the functions used in commom in all estimators."""

from abc import ABCMeta, abstractmethod
from config import Config


class AbsCommomApi(metaclass=ABCMeta):
	"""Contains commom methods that are needed by all estimation algorithm classes."""

	@property
	@abstractmethod
	def download_count(self):
		"""Returns the number of downloads."""
		pass

	@download_count.setter
	@abstractmethod
	def download_count(self, val):
		"""Sets the number of downloads."""
		pass

	@abstractmethod
	def read_query_pool(self):
		"""Returns a list with the queries specified in the query pool file, whose path is set in the Config class."""
		pass

	@abstractmethod		
	def log(self, tag, content = ""):
		"""Used to write logs in the log file specified in the Config class."""
		pass

	@abstractmethod		
	def download_entire_data_set(self):
		"""Returns a list with all the documents from the dataset."""
		pass

	@abstractmethod		
	def retrieve_number_matches(self, query):
		"""Returns the number of matches in the search engine for the given query."""
		pass

	@abstractmethod		
	def download(self, query, limit = Config.SEARCH_ENGINE_LIMIT):
		"""Returns the a list with documents retrieved by the given query with the max size set by the given limit."""
		pass

	@abstractmethod
	def execute_in_parallel(self, collection, callback):
		"""Executes a function in multiple threads, for each thread the callback receives an item from the collection."""
		pass

	@abstractmethod
	def report_progress(self, progress, total):
		"""Gives a feedback about the progress of the estimation."""
		pass

	@abstractmethod
	def log_result_experiment(self, estimation, duration, additional_information = {}):
		"""Registers the experiment result data"""
		pass
