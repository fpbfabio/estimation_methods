from threading import Lock
from random import randrange

from abs_estimator import AbsEstimator


class Mhr(AbsEstimator):
    _MAX_NUMBER_MATCHES_INFORMATION = "Máximo número de resultados"
    _MIN_NUMBER_MATCHES_INFORMATION = "Menor número de resultados"
    _NUMBER_QUERIES_INFORMATION = "Número de buscas"
    _MAX_NUMBER_MATCHES = 4500
    _MIN_NUMBER_MATCHES = 0
    _NUMBER_QUERIES = 5000

    @property
    def common_api(self):
        return self.__common_api

    @common_api.setter
    def common_api(self, val):
        self.__common_api = val

    @property
    def experiment_details(self):
        additional_information = {Mhr._NUMBER_QUERIES_INFORMATION: Mhr._NUMBER_QUERIES,
                                  Mhr._MAX_NUMBER_MATCHES_INFORMATION: Mhr._MAX_NUMBER_MATCHES,
                                  Mhr._MIN_NUMBER_MATCHES_INFORMATION: Mhr._MIN_NUMBER_MATCHES}
        return additional_information

    def __init__(self, common_api):
        self.__common_api = common_api
        self.__lock_accumulators = Lock()
        self.__lock_query_list = Lock()
        self.__query_count = 0
        self.__total_matches = 0
        self.__total_documents_returned = 0
        self.__document_id_dict = {}
        self.__query_list = []
        self.__query_pool_size = 0
        self.__progress_count = 0

    def _init_accumulators(self):
        self.__query_count = 0
        self.__total_matches = 0
        self.__total_documents_returned = 0
        self.__document_id_dict = {}
        self.__progress_count = 0

    def _init_query_list(self):
        self.__query_list = self.common_api.read_query_pool()
        self.__query_pool_size = len(self.__query_list)

    def _take_query(self):
        query = None
        with self.__lock_query_list:
            self.__progress_count += 1
            self.common_api.report_progress(self.__progress_count, Mhr._NUMBER_QUERIES)
            if self.__query_pool_size > 0:
                random_index = randrange(self.__query_pool_size)
                query = self.__query_list[random_index]
                del (self.__query_list[random_index])
        return query

    def _collect_data_for_estimation(self, number):
        query = self._take_query()
        number_matches = self.common_api.retrieve_number_matches(query)
        if Mhr._MIN_NUMBER_MATCHES <= number_matches <= Mhr._MAX_NUMBER_MATCHES:
            document_list = self.common_api.download(query, True, False).results
            id_list = []
            number_documents_returned = 0
            for document in document_list:
                id_list.append(document.identifier)
                number_documents_returned += 1
            with self.__lock_accumulators:
                self.__query_count += 1
                self.__total_matches += number_matches
                self.__total_documents_returned += number_documents_returned
                for id_item in id_list:
                    self.__document_id_dict[id_item] = self.__document_id_dict.get(id_item, 0) + 1

    def _calculate_estimation(self):
        estimation = -1
        number_unique_documents_returned = len(list(self.__document_id_dict.keys()))
        if self.__total_documents_returned != 0 and number_unique_documents_returned != 0:
            overflow_rate = self.__total_matches / self.__total_documents_returned
            overlapping_rate = self.__total_documents_returned / number_unique_documents_returned
            if overlapping_rate != 1:
                estimation = overflow_rate * number_unique_documents_returned / (1 - overlapping_rate ** (-1.1))
        return estimation

    def estimate(self):
        self._init_accumulators()
        self._init_query_list()
        self.common_api.execute_in_parallel(range(0, Mhr._NUMBER_QUERIES), self._collect_data_for_estimation)
        estimation = self._calculate_estimation()
        return estimation
