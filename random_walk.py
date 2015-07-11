from datetime import datetime
import random
import math

from abs_estimator import AbsEstimator
from config import Config


class RandomWalk(AbsEstimator):
    RANDOM_WALK_SAMPLE_SIZE_INFORMATION = "Number of nodes visited during the random walk"
    RANDOM_WALK_SAMPLE_SIZE = 2000

    @property
    def common_api(self):
        return self.__common_api

    @common_api.setter
    def common_api(self, val):
        self.__common_api = val

    def __init__(self, common_api):
        self.__common_api = common_api

    def estimate(self):
        start = datetime.now()
        document_degree_list = []
        frequency_number_nodes_dict = self.random_walk(document_degree_list)
        n = len(document_degree_list)
        d_w = sum(document_degree_list) / n
        d_h = n / sum([1 / x for x in document_degree_list])
        gama = (d_w / d_h - 1) ** 0.5
        binomy_n_2 = math.factorial(n) / (math.factorial(n - 2) * 2)
        c = sum([((math.factorial(x) / (math.factorial(x - 2) * 2)) * frequency_number_nodes_dict[x]) for x in
                 frequency_number_nodes_dict.keys()])
        estimation = (gama ** 2 + 1) * binomy_n_2 * 1 / (c + 1)
        end = datetime.now()
        additional_info = {RandomWalk.RANDOM_WALK_SAMPLE_SIZE_INFORMATION: RandomWalk.RANDOM_WALK_SAMPLE_SIZE}
        self.common_api.log_result_experiment(estimation, end - start, additional_info)

    def random_walk(self, document_degree_list):
        query_pool = self.common_api.read_query_pool()
        size = len(query_pool)
        query = query_pool[random.randrange(0, size)]
        while self.common_api.retrieve_number_matches(query) == 0:
            query = query_pool[random.randrange(0, size)]
        words = []
        count = 0
        number_words = 0
        node_frequency_dict = {}
        while count < RandomWalk.RANDOM_WALK_SAMPLE_SIZE:
            number_matches = self.common_api.retrieve_number_matches(query)
            if number_matches > 0:
                try:
                    results = self.common_api.download(query)
                except:
                    query = words[random.randrange(0, number_words)]
                    continue
                document = results[random.randrange(0, number_matches)]
                words = self.common_api.extract_words(document[Config.FIELD_TO_SEARCH])
                number_words = len(words)
                document_degree_list.append(number_words)
                node_frequency_dict[document[Config.ID_FIELD]] = node_frequency_dict.get(document[Config.ID_FIELD],
                                                                                         0) + 1
                count += 1
                self.common_api.report_progress(count, RandomWalk.RANDOM_WALK_SAMPLE_SIZE)
            query = words[random.randrange(0, number_words)]
        frequency_node_dict = {}
        for key in node_frequency_dict.keys():
            frequency_node_dict[node_frequency_dict[key]] = frequency_node_dict.get(node_frequency_dict[key], [])
            frequency_node_dict[node_frequency_dict[key]].append(key)
        frequency_number_nodes_dict = {x: len(frequency_node_dict[x]) for x in frequency_node_dict.keys() if x > 1}
        return frequency_number_nodes_dict
