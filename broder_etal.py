from threading import Lock
import random

from abs_estimator import AbsEstimator


class BroderEtAl(AbsEstimator):
    _QUERY_RANDOM_SAMPLE_SIZE_INFORMATION = "Size of the random sample of queries"
    _DOCUMENT_RANDOM_SAMPLE_SIZE_INFORMATION = "Size of the random sample of documents"
    _QUERY_RANDOM_SAMPLE_SIZE = 200
    _DOCUMENT_RANDOM_SAMPLE_SIZE = 1000

    @property
    def experiment_details(self):
        additional_information = {BroderEtAl._QUERY_RANDOM_SAMPLE_SIZE_INFORMATION:
                                  BroderEtAl._QUERY_RANDOM_SAMPLE_SIZE,
                                  BroderEtAl._DOCUMENT_RANDOM_SAMPLE_SIZE_INFORMATION:
                                  BroderEtAl._DOCUMENT_RANDOM_SAMPLE_SIZE}
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
        entire_data_set = self.common_api.download_entire_data_set().results
        random_document_sample = random.sample(entire_data_set, BroderEtAl._DOCUMENT_RANDOM_SAMPLE_SIZE)
        self.common_api.report_progress(1, 5)
        query_pool = self.common_api.read_query_pool()
        self.common_api.report_progress(2, 5)
        query_sample = random.sample(query_pool, BroderEtAl._QUERY_RANDOM_SAMPLE_SIZE)
        self.common_api.report_progress(3, 5)
        average_weight = self._calculate_average_query_weight(query_sample, query_pool)
        self.common_api.report_progress(4, 5)
        number_results_entire_pool = average_weight * len(query_pool)
        number_visible_pool = self._count_matches(random_document_sample, query_pool)
        self.common_api.report_progress(5, 5)
        probability_visible_pool = number_visible_pool / len(random_document_sample)
        estimation = number_results_entire_pool / probability_visible_pool
        return estimation

    def _verify_match(self, query, document):
        content = document.content.lower()
        if content.find(query.lower()) != -1:
            return True
        return False

    def _calculate_average_query_weight(self, query_sample, query_pool):
        weight_sum = 0
        lock = Lock()

        def calc_iteration(query):
            nonlocal weight_sum, query_pool, lock
            results = self.common_api.download(query).results
            query_weight = 0
            for document in results:
                count = 0
                for query in query_pool:
                    if self._verify_match(query, document):
                        count += 1
                if count > 0:
                    query_weight += 1 / count
            with lock:
                weight_sum += query_weight

        self.common_api.execute_in_parallel(query_sample, calc_iteration)
        average_weight = weight_sum / len(query_sample)
        return average_weight

    def _count_matches(self, document_sample, query_pool):
        count = 0
        lock = Lock()

        def iteration(document):
            nonlocal count, query_pool, lock
            for query in query_pool:
                if self._verify_match(query, document):
                    with lock:
                        count += 1
                    return

        self.common_api.execute_in_parallel(document_sample, iteration)
        return count
