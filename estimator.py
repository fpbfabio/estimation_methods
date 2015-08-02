""""
This is the module that provides an abstract interface for a class used to obtain
estimations of the size of a data set.
"""

from abc import ABCMeta, abstractmethod
import random
import math
from threading import Lock

from estimator_factory import EstimatorFactory


class AbsEstimator(metaclass=ABCMeta):
    """
    Class used to estimate the size of a data set.
    """

    @property
    @abstractmethod
    def query_pool_file_path(self):
        """
        Returns the path to the query pool file.
        """
        pass

    @query_pool_file_path.setter
    @abstractmethod
    def query_pool_file_path(self, val):
        """
        Sets the path to the query pool file.
        """
        pass

    @property
    @abstractmethod
    def factory(self):
        """
        Returns the instance of an AbsEstimatorFactory object.
        """
        pass

    @factory.setter
    @abstractmethod
    def factory(self, val):
        """
        Sets the instance of an AbsEstimatorFactory object.
        """
        pass

    @property
    @abstractmethod
    def word_extractor(self):
        """
        Returns the instance of an AbsWordExtractor object.
        """
        pass

    @word_extractor.setter
    @abstractmethod
    def word_extractor(self, val):
        """
        Sets the instance of an AbsWordExtractor object.
        """
        pass

    @property
    @abstractmethod
    def parallelizer(self):
        """
        Returns the instance of an AbsParallelizer object.
        """
        pass

    @parallelizer.setter
    @abstractmethod
    def parallelizer(self, val):
        """
        Sets the instance of an AbsParallelizer object.
        """
        pass

    @property
    @abstractmethod
    def crawler_api(self):
        """
        Returns the instance of an AbsCrawlerApi object.
        """
        pass

    @crawler_api.setter
    @abstractmethod
    def crawler_api(self, val):
        """
        Sets the instance of an AbsCrawlerApi object.
        """
        pass

    @abstractmethod
    def estimate(self):
        """
        Returns the estimation of the size of the data set.
        """
        pass

    @property
    @abstractmethod
    def experiment_details(self):
        """
        Returns the parameters used in the experiment.
        """
        pass

    @property
    @abstractmethod
    def download_count(self):
        """
        Returns the number of downloads in the estimation.
        """
        pass


class AbsBaseEstimator(AbsEstimator, metaclass=ABCMeta):

    def __init__(self, crawler_api):
        self.__query_pool_file_path = None
        self.__crawler_api = crawler_api
        self.__factory = EstimatorFactory()
        self.__word_extractor = self.factory.create_word_extractor()
        self.__parallelizer = self.factory.create_parallelizer()

    @property
    @abstractmethod
    def experiment_details(self):
        pass

    @property
    def query_pool_file_path(self):
        return self.__query_pool_file_path

    @query_pool_file_path.setter
    def query_pool_file_path(self, val):
        self.__query_pool_file_path = val

    @property
    def download_count(self):
        return self.crawler_api.download_count

    @property
    def factory(self):
        return self.__factory

    @factory.setter
    def factory(self, val):
        self.__factory = val

    @property
    def word_extractor(self):
        return self.__word_extractor

    @word_extractor.setter
    def word_extractor(self, val):
        self.__word_extractor = val

    @property
    def parallelizer(self):
        return self.__parallelizer

    @parallelizer.setter
    def parallelizer(self, val):
        self.__parallelizer = val

    @property
    def crawler_api(self):
        return self.__crawler_api

    @crawler_api.setter
    def crawler_api(self, val):
        self.__crawler_api = val

    @abstractmethod
    def estimate(self):
        self.crawler_api.download_count = 0

    def _report_progress(self, progress, total):
        print("Progress: " + str(progress) + "/" + str(total))

    def _read_query_pool(self):
        query_pool = []
        with open(self.query_pool_file_path) as archive:
            for line in archive:
                query_pool.append(line.rstrip("\n").rstrip("\r"))
        return query_pool


class Mhr(AbsBaseEstimator):

    _DEFAULT_QUERY_POOL_FILE_PATH = "/home/fabio/SolrFiles/Cores/WordLists/new_shine.txt"
    _MAX_NUMBER_MATCHES_INFORMATION = "Máximo número de resultados"
    _MIN_NUMBER_MATCHES_INFORMATION = "Menor número de resultados"
    _NUMBER_QUERIES_INFORMATION = "Número de buscas"
    _MAX_NUMBER_MATCHES = 5000000
    _MIN_NUMBER_MATCHES = 1
    _NUMBER_QUERIES = 100

    @property
    def experiment_details(self):
        additional_information = {Mhr._NUMBER_QUERIES_INFORMATION: Mhr._NUMBER_QUERIES,
                                  Mhr._MAX_NUMBER_MATCHES_INFORMATION: Mhr._MAX_NUMBER_MATCHES,
                                  Mhr._MIN_NUMBER_MATCHES_INFORMATION: Mhr._MIN_NUMBER_MATCHES}
        return additional_information

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.query_pool_file_path = Mhr._DEFAULT_QUERY_POOL_FILE_PATH
        self.__lock_accumulators = Lock()
        self.__lock_query_list = Lock()
        self.__query_count = 0
        self.__total_matches = 0
        self.__total_documents_returned = 0
        self.__document_id_dict = {}
        self.__query_pool = None
        self.__query_pool_size = None
        self.__progress_count = 0

    def _reset(self):
        self.__query_count = 0
        self.__total_matches = 0
        self.__total_documents_returned = 0
        self.__document_id_dict = {}
        self.__query_pool = self._read_query_pool()
        self.__query_pool_size = len(self.__query_pool)
        self.__progress_count = 0

    def _take_query(self):
        query = None
        with self.__lock_query_list:
            self.__progress_count += 1
            self._report_progress(self.__progress_count, Mhr._NUMBER_QUERIES)
            if self.__query_pool_size > 0:
                random_index = random.randrange(self.__query_pool_size)
                query = self.__query_pool[random_index]
                del (self.__query_pool[random_index])
                self.__query_pool_size -= 1
        return query

    def _collect_data_for_estimation(self, number):
        query = self._take_query()
        number_matches = self.crawler_api.retrieve_number_matches(query)
        if Mhr._MIN_NUMBER_MATCHES <= number_matches <= Mhr._MAX_NUMBER_MATCHES:
            document_list = self.crawler_api.download(query, True, False).results
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
        super().estimate()
        self._reset()
        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, range(0, Mhr._NUMBER_QUERIES),
                                              self._collect_data_for_estimation)
        estimation = self._calculate_estimation()
        return estimation


class RandomWalk(AbsBaseEstimator):

    _DEFAULT_QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    _MIN_NUMBER_MATCHES_FOR_SEED_QUERY_INFORMATION = "Número mínimo de resultados para busca semente"
    _MIN_NUMBER_MATCHES_FOR_SEED_QUERY = 2
    _MIN_NUMBER_WORDS_INFORMATION = "Número mínimo de palavras em um dcumento sorteado"
    _MIN_NUMBER_WORDS = 2
    _RANDOM_WALK_SAMPLE_SIZE_INFORMATION = "Número de nós visitados durante um \"random walk\""
    _RANDOM_WALK_SAMPLE_SIZE = 5000

    @property
    def experiment_details(self):
        additional_information = {RandomWalk._MIN_NUMBER_WORDS_INFORMATION:
                                  RandomWalk._MIN_NUMBER_WORDS,
                                  RandomWalk._MIN_NUMBER_MATCHES_FOR_SEED_QUERY_INFORMATION:
                                  RandomWalk._MIN_NUMBER_MATCHES_FOR_SEED_QUERY,
                                  RandomWalk._RANDOM_WALK_SAMPLE_SIZE_INFORMATION:
                                  RandomWalk._RANDOM_WALK_SAMPLE_SIZE}
        return additional_information

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.query_pool_file_path = RandomWalk._DEFAULT_QUERY_POOL_FILE_PATH

    def estimate(self):
        super().estimate()
        document_degree_list = []
        frequency_number_nodes_dict = self._random_walk(document_degree_list)
        n = len(document_degree_list)
        dw = sum(document_degree_list) / n
        dh = n / sum([1 / x for x in document_degree_list])
        binomy_n_2 = math.factorial(n) / (math.factorial(n - 2) * 2)
        c = sum([((math.factorial(x) / (math.factorial(x - 2) * 2)) * frequency_number_nodes_dict[x]) for x in
                 frequency_number_nodes_dict.keys()])
        estimation = (dw / dh) * binomy_n_2 * (1 / c)
        return estimation

    def _random_walk(self, document_degree_list):
        query_pool = self._read_query_pool()
        size = len(query_pool)
        query = query_pool[random.randrange(0, size)]
        number_matches = self.crawler_api.retrieve_number_matches(query)
        while number_matches < RandomWalk._MIN_NUMBER_MATCHES_FOR_SEED_QUERY:
            query = query_pool[random.randrange(0, size)]
            number_matches = self.crawler_api.retrieve_number_matches(query)
        words = []
        count = 0
        number_words = 0
        node_frequency_dict = {}
        while count < RandomWalk._RANDOM_WALK_SAMPLE_SIZE:
            if number_matches > 0:
                random_index = random.randrange(0, number_matches)
                try:
                    results = self.crawler_api.download(query, True, True, random_index, 1).results
                except:
                    query = words[random.randrange(0, number_words)]
                    number_matches = self.crawler_api.retrieve_number_matches(query)
                    continue
                document = results[0]
                words_buffer = self.word_extractor.extract_words(document.content)
                number_words_buffer = len(words_buffer)
                if number_words_buffer < RandomWalk._MIN_NUMBER_WORDS:
                    query = words[random.randrange(0, number_words)]
                    number_matches = self.crawler_api.retrieve_number_matches(query)
                    continue
                words = words_buffer
                number_words = number_words_buffer
                document_degree_list.append(number_words)
                node_frequency_dict[document.identifier] = \
                    node_frequency_dict.get(document.identifier, 0) + 1
                count += 1
                self._report_progress(count, RandomWalk._RANDOM_WALK_SAMPLE_SIZE)
            query = words[random.randrange(0, number_words)]
            number_matches = self.crawler_api.retrieve_number_matches(query)
        frequency_node_dict = {}
        for key in node_frequency_dict.keys():
            frequency_node_dict[node_frequency_dict[key]] = frequency_node_dict.get(node_frequency_dict[key], [])
            frequency_node_dict[node_frequency_dict[key]].append(key)
        frequency_number_nodes_dict = {x: len(frequency_node_dict[x]) for x in frequency_node_dict.keys() if x > 1}
        return frequency_number_nodes_dict


class SumEst(AbsBaseEstimator):

    _DEFAULT_QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    _THREAD_LIMIT = 10
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

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.query_pool_file_path = SumEst._DEFAULT_QUERY_POOL_FILE_PATH

    def estimate(self):
        super().estimate()
        estimation_acc = 0
        query_pool = self._read_query_pool()
        pool_size = self._estimate_pool_size(query_pool)
        for i in range(0, SumEst._ITERATION_NUMBER):
            query_document_pair = self._select_query_document_pair(query_pool)
            document = query_document_pair[SumEst._PAIR_DOCUMENT_INDEX]
            query = query_document_pair[SumEst._PAIR_QUERY_INDEX]
            document_inverse_degree = self._calculate_document_inverse_degree(document, query_pool)
            degree_query = self._calculate_degree_query(query)
            partial_estimation = pool_size * degree_query * document_inverse_degree
            estimation_acc += partial_estimation
            self._report_progress(i, SumEst._ITERATION_NUMBER)
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
                document_list = self.crawler_api.download(random_query).results
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

        self.parallelizer.execute_in_parallel(SumEst._THREAD_LIMIT, query_pool, iteration)
        return matching_query_list

    def _calculate_degree_query(self, query):
        lock = Lock()
        count = 0

        def iteration(document):
            nonlocal query, count, lock
            if self._verify_match(query, document):
                with lock:
                    count += 1

        document_list = self.crawler_api.download(query).results
        self.parallelizer.execute_in_parallel(SumEst._THREAD_LIMIT, document_list, iteration)
        return count

    def _estimate_pool_size(self, query_pool):
        count = 0
        query_pool_size = len(query_pool)
        lock = Lock()

        def iteration(iteration_number):
            nonlocal query_pool, query_pool_size, count, lock
            random_index = random.randrange(0, query_pool_size)
            query = query_pool[random_index]
            document_list = self.crawler_api.download(query).results
            for document in document_list:
                if self._verify_match(query, document):
                    with lock:
                        count += 1
                    return

        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, range(0, SumEst._POOL_SAMPLE_SIZE),
                                              iteration)
        return len(query_pool) * count / SumEst._POOL_SAMPLE_SIZE

    def _calculate_document_inverse_degree(self, document, query_pool):
        matching_query_list = self._get_matching_query_list(document, query_pool)
        i = 1
        while True:
            random_index = random.randrange(0, len(matching_query_list))
            query = matching_query_list[random_index]
            try:
                document_list = self.crawler_api.download(query).results
            except:
                continue
            for item in document_list:
                if item.identifier == document.identifier:
                    return i / len(matching_query_list)
            i += 1


class BroderEtAl(AbsBaseEstimator):

    _DEFAULT_QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    _THREAD_LIMIT = 10
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

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.query_pool_file_path = BroderEtAl._DEFAULT_QUERY_POOL_FILE_PATH

    def estimate(self):
        super().estimate()
        entire_data_set = self.crawler_api.download_entire_data_set().results
        random_document_sample = random.sample(entire_data_set, BroderEtAl._DOCUMENT_RANDOM_SAMPLE_SIZE)
        self._report_progress(1, 5)
        query_pool = self._read_query_pool()
        self._report_progress(2, 5)
        query_sample = random.sample(query_pool, BroderEtAl._QUERY_RANDOM_SAMPLE_SIZE)
        self._report_progress(3, 5)
        average_weight = self._calculate_average_query_weight(query_sample, query_pool)
        self._report_progress(4, 5)
        number_results_entire_pool = average_weight * len(query_pool)
        number_visible_pool = self._count_matches(random_document_sample, query_pool)
        self._report_progress(5, 5)
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
            results = self.crawler_api.download(query).results
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

        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, query_sample, calc_iteration)
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

        self.parallelizer.execute_in_parallel(BroderEtAl._THREAD_LIMIT, document_sample, iteration)
        return count
