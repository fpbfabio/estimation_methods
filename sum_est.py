from threading import Lock
import random

from abs_estimator import AbsEstimator


class SumEst(AbsEstimator):
    _ITERATION_NUMBER = 100
    _POOL_SAMPLE_SIZE = 1000
    _ITERATION_NUMBER_INFORMATION = "Number of iterations"
    _POOL_SAMPLE_SIZE_INFORMATION = "Size of the query pool sample"
    _PAIR_QUERY_INDEX = 0
    _PAIR_DOCUMENT_INDEX = 1

    @property
    def experiment_details(self):
        additional_information = {SumEst._ITERATION_NUMBER_INFORMATION: SumEst._ITERATION_NUMBER,
                                  SumEst._POOL_SAMPLE_SIZE_INFORMATION: SumEst._POOL_SAMPLE_SIZE}
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
        estimation_acc = 0
        query_pool = self.common_api.read_query_pool()
        pool_size = self._estimate_pool_size(query_pool)
        for i in range(0, SumEst._ITERATION_NUMBER):
            query_document_pair = self._select_query_document_pair(query_pool)
            document = query_document_pair[SumEst._PAIR_DOCUMENT_INDEX]
            query = query_document_pair[SumEst._PAIR_QUERY_INDEX]
            document_inverse_degree = self._calculate_document_inverse_degree(document, query_pool)
            degree_query = self._calculate_degree_query(query)
            partial_estimation = pool_size * degree_query * document_inverse_degree
            estimation_acc += partial_estimation
            self.common_api.report_progress(i, SumEst._ITERATION_NUMBER)
        estimation = estimation_acc / SumEst._ITERATION_NUMBER
        return estimation

    def _verify_match(self, query, document):
        content = document.content.lower()
        if content.find(query.lower()) != -1:
            return True
        return False

    def _select_query_document_pair(self, query_pool):
        list_size = len(query_pool)
        while True:
            random_index = random.randrange(list_size)
            random_query = query_pool[random_index]
            try:
                document_list = self.common_api.download(random_query).results
            except:
                continue
            valid_list = []
            for document in document_list:
                if self._verify_match(random_query, document):
                    valid_list.append(document)
            if len(valid_list) > 0:
                random_index = random.randrange(len(valid_list))
                random_document = valid_list[random_index]
                return [random_query, random_document]

    def _get_matching_query_list(self, document, query_pool):
        lock = Lock()
        matching_query_list = []

        def iteration(query):
            nonlocal document, matching_query_list, lock
            if self._verify_match(query, document):
                with lock:
                    matching_query_list.append(query)

        self.common_api.execute_in_parallel(query_pool, iteration)
        return matching_query_list

    def _calculate_degree_query(self, query):
        lock = Lock()
        count = 0

        def iteration(document):
            nonlocal query, count, lock
            if self._verify_match(query, document):
                with lock:
                    count += 1

        document_list = self.common_api.download(query).results
        self.common_api.execute_in_parallel(document_list, iteration)
        return count

    def _estimate_pool_size(self, query_pool):
        count = 0
        query_pool_size = len(query_pool)
        lock = Lock()

        def iteration(iteration_number):
            nonlocal query_pool, query_pool_size, count, lock
            random_index = random.randrange(0, query_pool_size)
            query = query_pool[random_index]
            document_list = self.common_api.download(query).results
            for document in document_list:
                if self._verify_match(query, document):
                    with lock:
                        count += 1
                    return

        self.common_api.execute_in_parallel(range(0, SumEst._POOL_SAMPLE_SIZE), iteration)
        return len(query_pool) * count / SumEst._POOL_SAMPLE_SIZE

    def _calculate_document_inverse_degree(self, document, query_pool):
        matching_query_list = self._get_matching_query_list(document, query_pool)
        i = 1
        while True:
            random_index = random.randrange(0, len(matching_query_list))
            query = matching_query_list[random_index]
            try:
                document_list = self.common_api.download(query).results
            except:
                continue
            for item in document_list:
                if item.identifier == document.identifier:
                    return i / len(matching_query_list)
            i += 1
