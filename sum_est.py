from datetime import datetime
from threading import Lock
import random

from abs_estimator import AbsEstimator
from config import Config


class SumEst(AbsEstimator):

	ITERATION_NUMBER = 100
	POOL_SAMPLE_SIZE = 1000
	ITERATION_NUMBER_INFORMATION = "Number of iterations"
	POOL_SAMPLE_SIZE_INFORMATION = "Size of the query pool sample"
	PAIR_QUERY_INDEX = 0
	PAIR_DOCUMENT_INDEX = 1

	@property
	def commom_api(self):
		return self.__commom_api

	@commom_api.setter
	def commom_api(self, val):
		self.__commom_api = val

	def __init__(self, commom_api):
		self.commom_api = commom_api

	def estimate(self):
		sum = 0
		start = datetime.now()
		query_pool = self.commom_api.read_query_pool()
		pool_size = self.estimate_pool_size(query_pool)
		for i in range(0, SumEst.ITERATION_NUMBER):
			query_document_pair = self.select_query_document_pair(query_pool)
			document = query_document_pair[SumEst.PAIR_DOCUMENT_INDEX]
			query = query_document_pair[SumEst.PAIR_QUERY_INDEX]
			document_inverse_degree = self.calculate_document_inverse_degree(document, query_pool)
			degree_query = self.calculate_degree_query(query)
			parcial_estimation = pool_size * degree_query * document_inverse_degree
			sum += parcial_estimation
			self.commom_api.report_progress(i, SumEst.ITERATION_NUMBER);
		end = datetime.now()
		estimation = sum / SumEst.ITERATION_NUMBER
		additional_info = {SumEst.ITERATION_NUMBER_INFORMATION : SumEst.ITERATION_NUMBER, SumEst.POOL_SAMPLE_SIZE_INFORMATION : SumEst.POOL_SAMPLE_SIZE}
		self.commom_api.log_result_experiment(estimation, end - start, additional_info)

	def verify_match(self, query, document):
		content = document[Config.FIELD_TO_SEARCH].lower()
		if (content.find(query.lower()) != -1):
			return True
		return False

	def select_query_document_pair(self, query_pool):
		list_size = len(query_pool)
		while (True):
			random_index = random.randrange(list_size)
			random_query = query_pool[random_index]
			document_list = []
			try:
				document_list = self.commom_api.download(random_query)
			except Exception as exception:
				continue
			valid_list = []
			for document in document_list:
				if (self.verify_match(random_query, document)):
					valid_list.append(document)
			if (len(valid_list) > 0):
				random_index = random.randrange(len(valid_list))
				random_document = valid_list[random_index]
				return [random_query, random_document]

	def get_matching_query_list(self, document, query_pool):
		lock = Lock()
		matching_query_list = []
		def iteration(query):
			nonlocal document, matching_query_list, lock
			if (self.verify_match(query, document)):
				with lock:
					matching_query_list.append(query)
		self.commom_api.execute_in_parallel(query_pool, iteration)
		return matching_query_list

	def calculate_degree_query(self, query):
		lock = Lock()
		count = 0
		def iteration(document):
			nonlocal query, count, lock
			if (self.verify_match(query, document)):
				with lock:
					count += 1
		document_list = self.commom_api.download(query)
		self.commom_api.execute_in_parallel(document_list, iteration)
		return count

	def estimate_pool_size(self, query_pool):
		count = 0
		query_pool_size = len(query_pool)
		lock = Lock()
		def iteration(iteration_number):
			nonlocal query_pool, query_pool_size, count, lock
			random_index = random.randrange(0, query_pool_size)
			query = query_pool[random_index]
			document_list = self.commom_api.download(query)
			for document in document_list:
				if (self.verify_match(query, document)):
					with lock:
						count += 1
					return
		self.commom_api.execute_in_parallel(range(0, SumEst.POOL_SAMPLE_SIZE), iteration)
		return len(query_pool) * count / SumEst.POOL_SAMPLE_SIZE

	def calculate_document_inverse_degree(self, document, query_pool):
		matching_query_list = self.get_matching_query_list(document, query_pool)
		i = 1
		while (True):
			random_index = random.randrange(0, len(matching_query_list))
			query = matching_query_list[random_index]
			document_list = []
			try:
				document_list = self.commom_api.download(query)
			except Exception as exception:
				continue
			for item in document_list:
				if (item[Config.ID_FIELD] == document[Config.ID_FIELD]):
					return i / len(matching_query_list)
			i += 1