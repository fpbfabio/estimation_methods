from datetime import datetime
from threading import Lock
from random import randrange

from abs_estimator import AbsEstimator
from config import Config


class Mhr(AbsEstimator):
    MAX_NUMBER_MATCHES = 4500
    MIN_NUMBER_MATCHES = 3500
    NUMBER_QUERIES = 5000

    @property
    def common_api(self):
        return self.__common_api

    @common_api.setter
    def common_api(self, val):
        self.__common_api = val

    @property
    def experiment_details(self):
        additional_information = {"Número de buscas": Mhr.NUMBER_QUERIES,
                                  "Máximo número de resultados": Mhr.MAX_NUMBER_MATCHES,
                                  "Menor número de resultados": Mhr.MIN_NUMBER_MATCHES}
        return additional_information

    def __init__(self, common_api):
        self.__common_api = common_api
        self.lock_accumulators = Lock()
        self.lock_query_list = Lock()
        self.query_count = 0
        self.total_matches = 0
        self.total_documents_returned = 0
        self.document_id_dict = {}
        self.query_list = []
        self.query_pool_size = 0
        self.progress_count = 0

    def init_accumulators(self):
        self.query_count = 0
        self.total_matches = 0
        self.total_documents_returned = 0
        self.document_id_dict = {}
        self.progress_count = 0

    def init_query_list(self):
        self.query_list = self.common_api.read_query_pool()
        self.query_pool_size = len(self.query_list)

    def take_query(self):
        query = None
        with self.lock_query_list:
            self.progress_count += 1
            self.common_api.report_progress(self.progress_count, Mhr.NUMBER_QUERIES)
            if self.query_pool_size > 0:
                random_index = randrange(self.query_pool_size)
                query = self.query_list[random_index]
                del (self.query_list[random_index])
        return query

    def collect_data_for_estimation(self):
        query = self.take_query()
        number_matches = self.common_api.retrieve_number_matches(query)
        if Mhr.MIN_NUMBER_MATCHES <= number_matches <= Mhr.MAX_NUMBER_MATCHES:
            document_list = self.common_api.download(query)
            id_list = []
            number_documents_returned = 0
            for document in document_list:
                id_list.append(document[Config.ID_FIELD])
                number_documents_returned += 1
            with self.lock_accumulators:
                self.query_count += 1
                self.total_matches += number_matches
                self.total_documents_returned += number_documents_returned
                for id_item in id_list:
                    self.document_id_dict[id_item] = self.document_id_dict.get(id_item, 0) + 1

    def calculate_estimation(self):
        estimation = -1
        number_unique_documents_returned = len(list(self.document_id_dict.keys()))
        if self.total_documents_returned != 0 and number_unique_documents_returned != 0:
            overflow_rate = self.total_matches / self.total_documents_returned
            overlapping_rate = self.total_documents_returned / number_unique_documents_returned
            if overlapping_rate != 1:
                estimation = overflow_rate * number_unique_documents_returned / (1 - overlapping_rate ** (-1.1))
        return estimation

    def estimate(self):
        self.init_accumulators()
        self.init_query_list()
        self.common_api.execute_in_parallel(range(0, Mhr.NUMBER_QUERIES), self.collect_data_for_estimation)
        estimation = self.calculate_estimation()
        return estimation
