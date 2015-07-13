import random
import math

from abs_estimator import AbsEstimator


class RandomWalk(AbsEstimator):
    RANDOM_WALK_SAMPLE_SIZE_INFORMATION = "Número de nós visitados durante um \"random walk\""
    RANDOM_WALK_SAMPLE_SIZE = 5000

    @property
    def experiment_details(self):
        additional_information = {RandomWalk.RANDOM_WALK_SAMPLE_SIZE_INFORMATION: RandomWalk.RANDOM_WALK_SAMPLE_SIZE}
        return additional_information

    @property
    def common_api(self):
        return self.__common_api

    @common_api.setter
    def common_api(self, val):
        self.__common_api = val

    def __init__(self, common_api):
        self.__common_api = common_api

    def estimate(self):
        document_degree_list = []
        frequency_number_nodes_dict = self.random_walk(document_degree_list)
        n = len(document_degree_list)
        dw = sum(document_degree_list) / n
        dh = n / sum([1 / x for x in document_degree_list])
        binomy_n_2 = math.factorial(n) / (math.factorial(n - 2) * 2)
        c = sum([((math.factorial(x) / (math.factorial(x - 2) * 2)) * frequency_number_nodes_dict[x]) for x in
                 frequency_number_nodes_dict.keys()])
        estimation = (dw / dh) * binomy_n_2 * (1 / c)
        return estimation

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
                random_index = random.randrange(0, number_matches)
                try:
                    results = self.common_api.download(query, True, True, random_index, 1).results
                except:
                    query = words[random.randrange(0, number_words)]
                    continue
                document = results[0]
                words = self.common_api.extract_words(document.content)
                number_words = len(words)
                document_degree_list.append(number_words)
                node_frequency_dict[document.identifier] = \
                    node_frequency_dict.get(document.identifier, 0) + 1
                count += 1
                self.common_api.report_progress(count, RandomWalk.RANDOM_WALK_SAMPLE_SIZE)
            query = words[random.randrange(0, number_words)]
        frequency_node_dict = {}
        for key in node_frequency_dict.keys():
            frequency_node_dict[node_frequency_dict[key]] = frequency_node_dict.get(node_frequency_dict[key], [])
            frequency_node_dict[node_frequency_dict[key]].append(key)
        frequency_number_nodes_dict = {x: len(frequency_node_dict[x]) for x in frequency_node_dict.keys() if x > 1}
        return frequency_number_nodes_dict
