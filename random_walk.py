from datetime import datetime
import random
import math

from abs_estimator import AbsEstimator
from config import Config


class RandomWalk(AbsEstimator):

	RANDOM_WALK_SAMPLE_SIZE_INFORMATION = "Number of nodes visited during the random walk"
	RANDOM_WALK_SAMPLE_SIZE = 2000

	@property
	def commom_api(self):
		return self.__commom_api

	@commom_api.setter
	def commom_api(self, val):
		self.__commom_api = val

	def __init__(self, commom_api):
		self.commom_api = commom_api

	def estimate(self):
		start = datetime.now()
		document_degree_list = []
		frequency_number_nodes_dict = self.random_walk(document_degree_list)
		n = len(document_degree_list)
		dW = sum(document_degree_list) / n
		dH = n / sum([ 1 / x for x in document_degree_list])
		gama = (dW / dH - 1) ** 0.5
		binomy_n_2 = math.factorial(n) / (math.factorial(n - 2) * 2)
		c = sum([((math.factorial(x) / (math.factorial(x - 2) * 2)) * frequency_number_nodes_dict[x]) for x in frequency_number_nodes_dict.keys()])
		estimation = (gama ** 2 + 1) * binomy_n_2 * 1 / (c + 1)
		end = datetime.now()
		additional_info = {RandomWalk.RANDOM_WALK_SAMPLE_SIZE_INFORMATION : RandomWalk.RANDOM_WALK_SAMPLE_SIZE}
		self.commom_api.log_result_experiment(estimation, end - start, additional_info)
		
	def random_walk(self, document_degree_list):
		query_pool = self.commom_api.read_query_pool()
		size = len(query_pool)
		query = query_pool[random.randrange(0, size)]
		while(self.commom_api.retrieve_number_matches(query) == 0):
			query = query_pool[random.randrange(0, size)]
		words = []
		count = 0
		number_words = 0
		node_frequency_dict = {}
		while(count < RandomWalk.RANDOM_WALK_SAMPLE_SIZE):
			number_matches = self.commom_api.retrieve_number_matches(query)
			if(number_matches > 0):
				results = None
				try:
					results = self.commom_api.download(query)
				except Exception as exception:
					query = words[random.randrange(0, number_words)]
					continue
				document = results[random.randrange(0, number_matches)]
				words = self.commom_api.extract_words(document[Config.FIELD_TO_SEARCH])
				number_words = len(words)
				document_degree_list.append(number_words)
				node_frequency_dict[document[Config.ID_FIELD]] = node_frequency_dict.get(document[Config.ID_FIELD], 0) + 1
				count += 1
				self.commom_api.report_progress(count, RandomWalk.RANDOM_WALK_SAMPLE_SIZE)
			query = words[random.randrange(0, number_words)]
		frequency_node_dict = {}
		for key in node_frequency_dict.keys():
			frequency_node_dict[node_frequency_dict[key]] = frequency_node_dict.get(node_frequency_dict[key], [])
			frequency_node_dict[node_frequency_dict[key]].append(key)
		frequency_number_nodes_dict = {x:len(frequency_node_dict[x]) for x in frequency_node_dict.keys() if x > 1}
		return frequency_number_nodes_dict