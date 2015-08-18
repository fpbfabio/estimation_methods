import abc
import random
import math
import threading
import itertools

import module_factory


class AbsEstimator(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def query_pool_file_path(self):
        pass

    @query_pool_file_path.setter
    @abc.abstractmethod
    def query_pool_file_path(self, val):
        pass

    @property
    @abc.abstractmethod
    def factory(self):
        pass

    @factory.setter
    @abc.abstractmethod
    def factory(self, val):
        pass

    @property
    @abc.abstractmethod
    def word_extractor(self):
        pass

    @word_extractor.setter
    @abc.abstractmethod
    def word_extractor(self, val):
        pass

    @property
    @abc.abstractmethod
    def parallelizer(self):
        pass

    @parallelizer.setter
    @abc.abstractmethod
    def parallelizer(self, val):
        pass

    @property
    @abc.abstractmethod
    def crawler_api(self):
        pass

    @crawler_api.setter
    @abc.abstractmethod
    def crawler_api(self, val):
        pass

    @abc.abstractmethod
    def estimate(self):
        pass

    @property
    @abc.abstractmethod
    def experiment_details(self):
        pass

    @property
    @abc.abstractmethod
    def download_count(self):
        pass


class AbsBaseEstimator(AbsEstimator, metaclass=abc.ABCMeta):

    _DEFAULT_QUERY_POOL_FILE_PATH = "AbsBaseEstimator__DEFAULT_QUERY_POOL_FILE_PATH"
    _QUERY_POOL_FILE_PATH_INFORMATION = "Lista de palavras"

    def __init__(self, crawler_api):
        self.__factory = module_factory.EstimatorFactory()
        path_dict = self.factory.create_path_dictionary()
        self.__query_pool_file_path = path_dict.get_path(AbsBaseEstimator._DEFAULT_QUERY_POOL_FILE_PATH)
        self.__crawler_api = crawler_api
        self.__word_extractor = self.factory.create_word_extractor()
        self.__parallelizer = self.factory.create_parallelizer()

    @property
    @abc.abstractmethod
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

    @abc.abstractmethod
    def estimate(self):
        self.crawler_api.clean_up_data_folder()
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
                                  Mhr._MIN_NUMBER_MATCHES_INFORMATION: Mhr._MIN_NUMBER_MATCHES,
                                  AbsBaseEstimator._QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.__lock_accumulators = threading.Lock()
        self.__lock_query_list = threading.Lock()
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
            if self.__query_pool_size > 0:
                random_index = random.randrange(self.__query_pool_size)
                query = self.__query_pool[random_index]
                del (self.__query_pool[random_index])
                self.__query_pool_size -= 1
        return query

    def _collect_data_for_estimation(self, number):
        query = self._take_query()
        while query is not None:
            search_result = self.crawler_api.download(query, True, False)
            number_matches = search_result.number_results
            if Mhr._MIN_NUMBER_MATCHES <= number_matches <= Mhr._MAX_NUMBER_MATCHES:
                document_list = search_result.results
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
                    self.__progress_count += 1
                    self._report_progress(self.__progress_count, Mhr._NUMBER_QUERIES)
                return
            query = self._take_query()

    def _calculate_estimation(self):
        estimation = -1
        overlapping_rate = -1
        number_unique_documents_returned = len(list(self.__document_id_dict.keys()))
        if self.__total_documents_returned != 0 and number_unique_documents_returned != 0:
            overflow_rate = self.__total_matches / self.__total_documents_returned
            overlapping_rate = self.__total_documents_returned / number_unique_documents_returned
            if overlapping_rate != 1:
                estimation = overflow_rate * number_unique_documents_returned / (1 - overlapping_rate ** (-1.1))
        if estimation == -1:
            print("total_documents_returned = " + str(self.__total_documents_returned))
            print("number_unique_documents_returned = " + str(number_unique_documents_returned))
            print("overlapping_rate = " + str(overlapping_rate))
        return estimation

    def estimate(self):
        super().estimate()
        self._reset()
        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, range(0, Mhr._NUMBER_QUERIES),
                                              self._collect_data_for_estimation)
        estimation = self._calculate_estimation()
        return estimation


class RandomWalk(AbsBaseEstimator):

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
                                  RandomWalk._RANDOM_WALK_SAMPLE_SIZE,
                                  AbsBaseEstimator._QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

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
        number_matches = self.crawler_api.download_item(query, 0).number_results
        while number_matches < RandomWalk._MIN_NUMBER_MATCHES_FOR_SEED_QUERY:
            query = query_pool[random.randrange(0, size)]
            number_matches = self.crawler_api.download_item(query, 0).number_results
        words = []
        count = 0
        number_words = 0
        node_frequency_dict = {}
        while count < RandomWalk._RANDOM_WALK_SAMPLE_SIZE:
            if number_matches > 0:
                random_index = random.randrange(0, number_matches)
                results = self.crawler_api.download_item(query, random_index).results
                if results is None:
                    query = words[random.randrange(0, number_words)]
                    number_matches = self.crawler_api.download_item(query, 0).number_results
                    continue
                document = results[0]
                words_buffer = self.word_extractor.extract_words(document.content)
                number_words_buffer = len(words_buffer)
                if number_words_buffer < RandomWalk._MIN_NUMBER_WORDS:
                    query = words[random.randrange(0, number_words)]
                    number_matches = self.crawler_api.download_item(query, 0).number_results
                    continue
                words = words_buffer
                number_words = number_words_buffer
                document_degree_list.append(number_words)
                node_frequency_dict[document.identifier] = \
                    node_frequency_dict.get(document.identifier, 0) + 1
                count += 1
                self._report_progress(count, RandomWalk._RANDOM_WALK_SAMPLE_SIZE)
            query = words[random.randrange(0, number_words)]
            number_matches = self.crawler_api.download_item(query, 0).number_results
        frequency_node_dict = {}
        for key in node_frequency_dict.keys():
            frequency_node_dict[node_frequency_dict[key]] = frequency_node_dict.get(node_frequency_dict[key], [])
            frequency_node_dict[node_frequency_dict[key]].append(key)
        frequency_number_nodes_dict = {x: len(frequency_node_dict[x]) for x in frequency_node_dict.keys() if x > 1}
        return frequency_number_nodes_dict


class SumEst(AbsBaseEstimator):

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
                                  SumEst._POOL_SAMPLE_SIZE_INFORMATION: SumEst._POOL_SAMPLE_SIZE,
                                  AbsBaseEstimator._QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

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
        lock = threading.Lock()
        matching_query_list = []

        def iteration(query):
            nonlocal document, matching_query_list, lock
            if self._verify_match(query, document):
                with lock:
                    matching_query_list.append(query)

        self.parallelizer.execute_in_parallel(SumEst._THREAD_LIMIT, query_pool, iteration)
        return matching_query_list

    def _calculate_degree_query(self, query):
        lock = threading.Lock()
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
        lock = threading.Lock()

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
                                  BroderEtAl._DOCUMENT_RANDOM_SAMPLE_SIZE,
                                  AbsBaseEstimator._QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

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
        lock = threading.Lock()

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
        lock = threading.Lock()

        def iteration(document):
            nonlocal count, query_pool, lock
            for query in query_pool:
                if self._verify_match(query, document):
                    with lock:
                        count += 1
                    return

        self.parallelizer.execute_in_parallel(BroderEtAl._THREAD_LIMIT, document_sample, iteration)
        return count


class AbsShokouhi(AbsBaseEstimator, metaclass=abc.ABCMeta):

    _MIN_NUMBER_MATCHES = 20
    FACTOR_N = 10
    _FACTOR_T = 5000
    _MIN_NUMBER_MATCHES_INFORMATION = "Min number of matches for queries to be in the sample"
    _FACTOR_N_INFORMATION = "Factor N"
    _FACTOR_T_INFORMATION = "Factor T"

    @property
    def experiment_details(self):
        additional_information = {AbsShokouhi._FACTOR_T_INFORMATION: AbsShokouhi._FACTOR_T,
                                  AbsShokouhi._FACTOR_N_INFORMATION: AbsShokouhi.FACTOR_N,
                                  AbsShokouhi._MIN_NUMBER_MATCHES_INFORMATION: AbsShokouhi._MIN_NUMBER_MATCHES,
                                  AbsBaseEstimator._QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    @abc.abstractmethod
    def estimate(self):
        super().estimate()
        self.crawler_api.limit_results_per_query = AbsShokouhi.FACTOR_N

    def _build_query_sample(self):
        count = 0
        query_pool = self._read_query_pool()
        size = len(query_pool)
        query_sample = []
        while count < AbsShokouhi._FACTOR_T:
            index = random.randrange(0, size)
            query = random.sample(query_pool, 1)
            del(query_pool[index])
            size -= 1
            if self.crawler_api.download(query, True, False).number_results > AbsShokouhi._MIN_NUMBER_MATCHES:
                query_sample.append(query)
                count += 1
        return query_sample


class AbsMCR(AbsShokouhi, metaclass=abc.ABCMeta):

    def _count_duplicates(self, data_list_1, data_list_2):
        id_list_1 = [x.identifier for x in data_list_1]
        id_list_2 = [x.identifier for x in data_list_2]
        duplicates = [x for x in id_list_1 if x in id_list_2]
        return len(duplicates)

    @abc.abstractmethod
    def estimate(self):
        super().estimate()
        query_sample = self._build_query_sample()
        result_list = [self.crawler_api.download(x, True, False) for x in query_sample]
        factor_d = sum([self._count_duplicates(result_list[x - 1], result_list[x]) for x in range(1, AbsMCR._FACTOR_T)])
        estimation = AbsMCR._FACTOR_T * (AbsMCR._FACTOR_T - 1) * AbsMCR.FACTOR_N ** 2 / factor_d
        return estimation


class AbsCH(AbsShokouhi, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def estimate(self):
        super().estimate()
        query_sample = self._build_query_sample()
        marked_list = []
        numerator = 0
        denominator = 0
        for i in range(0, AbsCH._FACTOR_T):
            result = self.crawler_api.download(query_sample[i], True, False)
            numerator += AbsCH.FACTOR_N * len(marked_list) ** 2
            id_list = [x.identifier for x in result.results]
            denominator += len([x for x in id_list if x in marked_list]) * len(marked_list)
            marked_list = list(itertools.chain(id_list, marked_list))
        estimation = numerator / denominator
        return estimation


class MCR(AbsMCR):

    def estimate(self):
        return super().estimate()


class MCRReg(AbsMCR):

    def estimate(self):
        estimation = super().estimate()
        return 10 ** (math.log10(estimation) - 1.5767) / 0.5911


class CH(AbsCH):

    def estimate(self):
        return super().estimate()


class CHReg(AbsCH):

    def estimate(self):
        estimation = super().estimate()
        return 10 ** (math.log10(estimation) - 1.4208) / 0.6429
