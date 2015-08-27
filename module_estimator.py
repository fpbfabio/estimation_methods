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
    DEFAULT_QUERY_POOL_FILE_PATH = "AbsBaseEstimator__DEFAULT_QUERY_POOL_FILE_PATH"
    QUERY_POOL_FILE_PATH_INFORMATION = "Lista de palavras"

    def __init__(self, crawler_api):
        self.__factory = module_factory.EstimatorFactory()
        path_dict = self.factory.create_path_dictionary()
        self.__query_pool_file_path = path_dict.get_path(AbsBaseEstimator.DEFAULT_QUERY_POOL_FILE_PATH)
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

    def report_progress(self, progress, total):
        print("Progress: " + str(progress) + "/" + str(total))

    def read_query_pool(self):
        query_pool = []
        with open(self.query_pool_file_path) as archive:
            for line in archive:
                query_pool.append(line.rstrip("\n").rstrip("\r"))
        return query_pool


class AbsMhr(AbsBaseEstimator, metaclass=abc.ABCMeta):
    MAX_NUMBER_MATCHES_INFORMATION = "Máximo número de resultados"
    MIN_NUMBER_MATCHES_INFORMATION = "Menor número de resultados"
    NUMBER_QUERIES_INFORMATION = "Número de buscas"

    @property
    def experiment_details(self):
        additional_information = {type(self).NUMBER_QUERIES_INFORMATION: type(self).NUMBER_QUERIES,
                                  type(self).MAX_NUMBER_MATCHES_INFORMATION: type(self).MAX_NUMBER_MATCHES,
                                  type(self).MIN_NUMBER_MATCHES_INFORMATION: type(self).MIN_NUMBER_MATCHES,
                                  AbsBaseEstimator.QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.lock_accumulators = threading.Lock()
        self.lock_query_list = threading.Lock()
        self.query_count = 0
        self.total_matches = 0
        self.total_documents_returned = 0
        self.document_id_dict = {}
        self.query_pool = None
        self.query_pool_size = None
        self.progress_count = 0

    def reset(self):
        self.query_count = 0
        self.total_matches = 0
        self.total_documents_returned = 0
        self.document_id_dict = {}
        self.query_pool = self.read_query_pool()
        self.query_pool_size = len(self.query_pool)
        self.progress_count = 0

    def take_query(self):
        query = None
        with self.lock_query_list:
            if self.query_pool_size > 0:
                random_index = random.randrange(self.query_pool_size)
                query = self.query_pool[random_index]
                del (self.query_pool[random_index])
                self.query_pool_size -= 1
                self.progress_count += 1
                self.report_progress(self.progress_count, type(self).NUMBER_QUERIES)
        return query

    def collect_data_for_estimation(self, number, always_download_all=False):
        query = self.take_query()
        if always_download_all:
            search_result = self.crawler_api.download(query, True, False)
        else:
            search_result = self.crawler_api.download_item(query, 0)
        number_matches = search_result.number_results
        if type(self).MIN_NUMBER_MATCHES <= number_matches <= type(self).MAX_NUMBER_MATCHES:
            if not always_download_all:
                search_result = self.crawler_api.download(query, True, False)
            id_list = [x.identifier for x in search_result.results]
            with self.lock_accumulators:
                self.query_count += 1
                self.total_matches += number_matches
                self.total_documents_returned += len(id_list)
                for id_item in id_list:
                    self.document_id_dict[id_item] = self.document_id_dict.get(id_item, 0) + 1
            return True
        return False

    def calculate_estimation(self):
        estimation = -1
        overlapping_rate = -1
        number_unique_documents_returned = len(list(self.document_id_dict.keys()))
        if self.total_documents_returned != 0 and number_unique_documents_returned != 0:
            overflow_rate = self.total_matches / self.total_documents_returned
            overlapping_rate = self.total_documents_returned / number_unique_documents_returned
            if overlapping_rate != 1:
                estimation = overflow_rate * number_unique_documents_returned / (1 - overlapping_rate ** (-1.1))
        if estimation == -1:
            print("total_documents_returned = " + str(self.total_documents_returned))
            print("number_unique_documents_returned = " + str(number_unique_documents_returned))
            print("overlapping_rate = " + str(overlapping_rate))
        return estimation

    def estimate(self):
        super().estimate()
        self.reset()
        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, range(0, type(self).NUMBER_QUERIES),
                                              self.collect_data_for_estimation)
        estimation = self.calculate_estimation()
        return estimation


class Mhr(AbsMhr):
    MAX_NUMBER_MATCHES = 5000000
    MIN_NUMBER_MATCHES = 1
    NUMBER_QUERIES = 100

    def collect_data_for_estimation(self, number, always_download_all=False):
        success = False
        while not success:
            success = super().collect_data_for_estimation(number, True)


class ExactMhr(AbsMhr):
    MAX_NUMBER_MATCHES = 4500
    MIN_NUMBER_MATCHES = 3500
    NUMBER_QUERIES = 5000


class TeacherMhr(AbsBaseEstimator):
    THREAD_LIMIT = 1
    MAX_NUMBER_MATCHES_INFORMATION = "Máximo número de resultados"
    MIN_NUMBER_MATCHES_INFORMATION = "Menor número de resultados"
    NUMBER_QUERIES_INFORMATION = "Número de buscas"
    MAX_NUMBER_MATCHES = 5000000
    MIN_NUMBER_MATCHES = 1
    NUMBER_QUERIES = 100

    @property
    def experiment_details(self):
        additional_information = {type(self).NUMBER_QUERIES_INFORMATION: type(self).NUMBER_QUERIES,
                                  type(self).MAX_NUMBER_MATCHES_INFORMATION: type(self).MAX_NUMBER_MATCHES,
                                  type(self).MIN_NUMBER_MATCHES_INFORMATION: type(self).MIN_NUMBER_MATCHES,
                                  AbsBaseEstimator.QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    def __init__(self, crawler_api):
        super().__init__(crawler_api)
        self.lock_accumulators = threading.Lock()
        self.lock_query_list = threading.Lock()
        self.document_id_list_last_iteration = []
        self.query_count = 0
        self.total_matches = 0
        self.total_documents_returned = 0
        self.query_pool = None
        self.query_pool_size = None
        self.progress_count = 0
        self.total_unique_documents_returned = 0

    def reset(self):
        self.query_count = 0
        self.total_matches = 0
        self.document_id_list_last_iteration = []
        self.total_documents_returned = 0
        self.query_pool = self.read_query_pool()
        self.query_pool_size = len(self.query_pool)
        self.progress_count = 0
        self.total_unique_documents_returned = 0

    def take_query(self):
        query = None
        with self.lock_query_list:
            if self.query_pool_size > 0:
                random_index = random.randrange(self.query_pool_size)
                query = self.query_pool[random_index]
                del (self.query_pool[random_index])
                self.query_pool_size -= 1
        return query

    def collect_data_for_estimation(self, number):
        query = self.take_query()
        search_result = self.crawler_api.download(query, True, False)
        number_matches = search_result.number_results
        if type(self).MIN_NUMBER_MATCHES <= number_matches <= type(self).MAX_NUMBER_MATCHES:
            document_list = search_result.results
            id_list = []
            number_documents_returned = 0
            for document in document_list:
                id_list.append(document.identifier)
                number_documents_returned += 1
            with self.lock_accumulators:
                self.query_count += 1
                self.total_matches += number_matches
                self.total_documents_returned += number_documents_returned
                new_document_list = [x for x in id_list if x not in self.document_id_list_last_iteration]
                self.total_unique_documents_returned += len(new_document_list)
                self.document_id_list_last_iteration = new_document_list
                self.progress_count += 1
                self.report_progress(self.progress_count, type(self).NUMBER_QUERIES)
            return True
        return False

    def calculate_estimation(self):
        estimation = -1
        overlapping_rate = -1
        if self.total_documents_returned != 0 and self.total_unique_documents_returned != 0:
            overflow_rate = self.total_matches / self.total_documents_returned
            overlapping_rate = self.total_documents_returned / self.total_unique_documents_returned
            if overlapping_rate != 1:
                estimation = overflow_rate * self.total_unique_documents_returned / (1 - overlapping_rate ** (-1.1))
        if estimation == -1:
            print("total_documents_returned = " + str(self.total_documents_returned))
            print("total_unique_documents_returned = " + str(self.total_unique_documents_returned))
            print("overlapping_rate = " + str(overlapping_rate))
        return estimation

    def estimate(self):
        super().estimate()
        self.reset()
        self.parallelizer.execute_in_parallel(type(self).THREAD_LIMIT, range(0, type(self).NUMBER_QUERIES),
                                              self.collect_data_for_estimation)
        estimation = self.calculate_estimation()
        return estimation

class RandomWalk(AbsBaseEstimator):
    MIN_NUMBER_MATCHES_FOR_SEED_QUERY_INFORMATION = "Número mínimo de resultados para busca semente"
    MIN_NUMBER_MATCHES_FOR_SEED_QUERY = 2
    MIN_NUMBER_WORDS_INFORMATION = "Número mínimo de palavras em um dcumento sorteado"
    MIN_NUMBER_WORDS = 2
    RANDOM_WALK_SAMPLE_SIZE_INFORMATION = "Número de nós visitados durante um \"random walk\""
    RANDOM_WALK_SAMPLE_SIZE = 5000

    @property
    def experiment_details(self):
        additional_information = {RandomWalk.MIN_NUMBER_WORDS_INFORMATION:
                                  RandomWalk.MIN_NUMBER_WORDS,
                                  RandomWalk.MIN_NUMBER_MATCHES_FOR_SEED_QUERY_INFORMATION:
                                  RandomWalk.MIN_NUMBER_MATCHES_FOR_SEED_QUERY,
                                  RandomWalk.RANDOM_WALK_SAMPLE_SIZE_INFORMATION:
                                  RandomWalk.RANDOM_WALK_SAMPLE_SIZE,
                                  AbsBaseEstimator.QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    def estimate(self):
        super().estimate()
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
        query_pool = self.read_query_pool()
        size = len(query_pool)
        query = query_pool[random.randrange(0, size)]
        number_matches = self.crawler_api.download_item(query, 0).number_results
        while number_matches < RandomWalk.MIN_NUMBER_MATCHES_FOR_SEED_QUERY:
            query = query_pool[random.randrange(0, size)]
            number_matches = self.crawler_api.download_item(query, 0).number_results
        words = []
        count = 0
        number_words = 0
        node_frequency_dict = {}
        while count < RandomWalk.RANDOM_WALK_SAMPLE_SIZE:
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
                if number_words_buffer < RandomWalk.MIN_NUMBER_WORDS:
                    query = words[random.randrange(0, number_words)]
                    number_matches = self.crawler_api.download_item(query, 0).number_results
                    continue
                words = words_buffer
                number_words = number_words_buffer
                document_degree_list.append(number_words)
                node_frequency_dict[document.identifier] = \
                    node_frequency_dict.get(document.identifier, 0) + 1
                count += 1
                self.report_progress(count, RandomWalk.RANDOM_WALK_SAMPLE_SIZE)
            query = words[random.randrange(0, number_words)]
            number_matches = self.crawler_api.download_item(query, 0).number_results
        frequency_node_dict = {}
        for key in node_frequency_dict.keys():
            frequency_node_dict[node_frequency_dict[key]] = frequency_node_dict.get(node_frequency_dict[key], [])
            frequency_node_dict[node_frequency_dict[key]].append(key)
        frequency_number_nodes_dict = {x: len(frequency_node_dict[x]) for x in frequency_node_dict.keys() if x > 1}
        return frequency_number_nodes_dict


class SumEst(AbsBaseEstimator):
    THREAD_LIMIT = 10
    ITERATION_NUMBER = 100
    POOL_SAMPLE_SIZE = 1000
    ITERATION_NUMBER_INFORMATION = "Number of iterations"
    POOL_SAMPLE_SIZE_INFORMATION = "Size of the query pool sample"
    PAIR_QUERY_INDEX = 0
    PAIR_DOCUMENT_INDEX = 1

    @property
    def experiment_details(self):
        additional_information = {SumEst.ITERATION_NUMBER_INFORMATION: SumEst.ITERATION_NUMBER,
                                  SumEst.POOL_SAMPLE_SIZE_INFORMATION: SumEst.POOL_SAMPLE_SIZE,
                                  AbsBaseEstimator.QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    def estimate(self):
        super().estimate()
        estimation_acc = 0
        query_pool = self.read_query_pool()
        pool_size = self.estimate_pool_size(query_pool)
        for i in range(0, SumEst.ITERATION_NUMBER):
            query_document_pair = self.select_query_document_pair(query_pool)
            document = query_document_pair[SumEst.PAIR_DOCUMENT_INDEX]
            query = query_document_pair[SumEst.PAIR_QUERY_INDEX]
            document_inverse_degree = self.calculate_document_inverse_degree(document, query_pool)
            degree_query = self.calculate_degree_query(query)
            partial_estimation = pool_size * degree_query * document_inverse_degree
            estimation_acc += partial_estimation
            self.report_progress(i, SumEst.ITERATION_NUMBER)
        estimation = estimation_acc / SumEst.ITERATION_NUMBER
        return estimation

    def verify_match(self, query, document):
        content = document.content.lower()
        if content.find(query.lower()) != -1:
            return True
        return False

    def select_query_document_pair(self, query_pool):
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
                if self.verify_match(random_query, document):
                    valid_list.append(document)
            if len(valid_list) > 0:
                random_index = random.randrange(len(valid_list))
                random_document = valid_list[random_index]
                return [random_query, random_document]

    def get_matching_query_list(self, document, query_pool):
        lock = threading.Lock()
        matching_query_list = []

        def iteration(query):
            nonlocal document, matching_query_list, lock
            if self.verify_match(query, document):
                with lock:
                    matching_query_list.append(query)

        self.parallelizer.execute_in_parallel(SumEst.THREAD_LIMIT, query_pool, iteration)
        return matching_query_list

    def calculate_degree_query(self, query):
        lock = threading.Lock()
        count = 0

        def iteration(document):
            nonlocal query, count, lock
            if self.verify_match(query, document):
                with lock:
                    count += 1

        document_list = self.crawler_api.download(query).results
        self.parallelizer.execute_in_parallel(SumEst.THREAD_LIMIT, document_list, iteration)
        return count

    def estimate_pool_size(self, query_pool):
        count = 0
        query_pool_size = len(query_pool)
        lock = threading.Lock()

        def iteration(iteration_number):
            nonlocal query_pool, query_pool_size, count, lock
            random_index = random.randrange(0, query_pool_size)
            query = query_pool[random_index]
            document_list = self.crawler_api.download(query).results
            for document in document_list:
                if self.verify_match(query, document):
                    with lock:
                        count += 1
                    return

        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, range(0, SumEst.POOL_SAMPLE_SIZE),
                                              iteration)
        return len(query_pool) * count / SumEst.POOL_SAMPLE_SIZE

    def calculate_document_inverse_degree(self, document, query_pool):
        matching_query_list = self.get_matching_query_list(document, query_pool)
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
    THREAD_LIMIT = 10
    QUERY_RANDOM_SAMPLE_SIZE_INFORMATION = "Size of the random sample of queries"
    DOCUMENT_RANDOM_SAMPLE_SIZE_INFORMATION = "Size of the random sample of documents"
    QUERY_RANDOM_SAMPLE_SIZE = 200
    DOCUMENT_RANDOM_SAMPLE_SIZE = 1000

    @property
    def experiment_details(self):
        additional_information = {BroderEtAl.QUERY_RANDOM_SAMPLE_SIZE_INFORMATION:
                                  BroderEtAl.QUERY_RANDOM_SAMPLE_SIZE,
                                  BroderEtAl.DOCUMENT_RANDOM_SAMPLE_SIZE_INFORMATION:
                                  BroderEtAl.DOCUMENT_RANDOM_SAMPLE_SIZE,
                                  AbsBaseEstimator.QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    def estimate(self):
        super().estimate()
        entire_data_set = self.crawler_api.download_entire_data_set().results
        random_document_sample = random.sample(entire_data_set, BroderEtAl.DOCUMENT_RANDOM_SAMPLE_SIZE)
        self.report_progress(1, 5)
        query_pool = self.read_query_pool()
        self.report_progress(2, 5)
        query_sample = random.sample(query_pool, BroderEtAl.QUERY_RANDOM_SAMPLE_SIZE)
        self.report_progress(3, 5)
        average_weight = self.calculate_average_query_weight(query_sample, query_pool)
        self.report_progress(4, 5)
        number_results_entire_pool = average_weight * len(query_pool)
        number_visible_pool = self.count_matches(random_document_sample, query_pool)
        self.report_progress(5, 5)
        probability_visible_pool = number_visible_pool / len(random_document_sample)
        estimation = number_results_entire_pool / probability_visible_pool
        return estimation

    def verify_match(self, query, document):
        content = document.content.lower()
        if content.find(query.lower()) != -1:
            return True
        return False

    def calculate_average_query_weight(self, query_sample, query_pool):
        weight_sum = 0
        lock = threading.Lock()

        def calc_iteration(query):
            nonlocal weight_sum, query_pool, lock
            results = self.crawler_api.download(query).results
            query_weight = 0
            for document in results:
                count = 0
                for query in query_pool:
                    if self.verify_match(query, document):
                        count += 1
                if count > 0:
                    query_weight += 1 / count
            with lock:
                weight_sum += query_weight

        self.parallelizer.execute_in_parallel(self.crawler_api.thread_limit, query_sample, calc_iteration)
        average_weight = weight_sum / len(query_sample)
        return average_weight

    def count_matches(self, document_sample, query_pool):
        count = 0
        lock = threading.Lock()

        def iteration(document):
            nonlocal count, query_pool, lock
            for query in query_pool:
                if self.verify_match(query, document):
                    with lock:
                        count += 1
                    return

        self.parallelizer.execute_in_parallel(BroderEtAl.THREAD_LIMIT, document_sample, iteration)
        return count


class AbsShokouhi(AbsBaseEstimator, metaclass=abc.ABCMeta):
    MIN_NUMBER_MATCHES = 20
    FACTOR_K = 10
    QUERY_SAMPLE_SIZE = 5000
    MIN_NUMBER_MATCHES_INFORMATION = "Min number of matches for queries to be in the sample"
    FACTOR_K_INFORMATION = "Factor K"
    QUERY_SAMPLE_SIZE_INFORMATION = "QUERY_SAMPLE_SIZE"

    @property
    def experiment_details(self):
        additional_information = {AbsShokouhi.QUERY_SAMPLE_SIZE_INFORMATION: AbsShokouhi.QUERY_SAMPLE_SIZE,
                                  AbsShokouhi.FACTOR_K_INFORMATION: AbsShokouhi.FACTOR_K,
                                  AbsShokouhi.MIN_NUMBER_MATCHES_INFORMATION: AbsShokouhi.MIN_NUMBER_MATCHES,
                                  AbsBaseEstimator.QUERY_POOL_FILE_PATH_INFORMATION: self.query_pool_file_path}
        return additional_information

    @abc.abstractmethod
    def estimate(self):
        super().estimate()
        self.crawler_api.limit_results_per_query = AbsShokouhi.FACTOR_K


class AbsMCR(AbsShokouhi, metaclass=abc.ABCMeta):
    def count_duplicates(self, data_list_1, data_list_2):
        id_list_1 = [x.identifier for x in data_list_1]
        id_list_2 = [x.identifier for x in data_list_2]
        duplicates = [x for x in id_list_1 if x in id_list_2]
        return len(duplicates)

    @abc.abstractmethod
    def estimate(self):
        super().estimate()
        query_pool = self.read_query_pool()
        query_sample =  random.sample(query_pool, AbsShokouhi.QUERY_SAMPLE_SIZE)
        random_sample_list = [self.crawler_api.download(x, True, False) for x in query_sample]
        random_sample_list = [x.results for x in random_sample_list if
                              x.number_results > AbsShokouhi.MIN_NUMBER_MATCHES]
        factor_t = len(random_sample_list)
        factor_d = sum([self.count_duplicates(x, y) for x, y in itertools.combinations(random_sample_list, 2)])
        estimation = factor_t * (factor_t - 1) * AbsShokouhi.FACTOR_K ** 2 / (2 * factor_d)
        return estimation


class AbsCH(AbsShokouhi, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def estimate(self):
        super().estimate()
        query_pool = self.read_query_pool()
        query_sample =  random.sample(query_pool, AbsShokouhi.QUERY_SAMPLE_SIZE)
        random_sample_list = [self.crawler_api.download(x, True, False) for x in query_sample]
        random_sample_list = [x.results for x in random_sample_list if
                              x.number_results > AbsShokouhi.MIN_NUMBER_MATCHES]
        marked_list = []
        numerator = 0
        denominator = 0
        for data_list in random_sample_list:
            numerator += AbsCH.FACTOR_K * len(marked_list) ** 2
            id_list = [x.identifier for x in data_list]
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
        return 10 ** ((math.log10(estimation) - 1.5767) / 0.5911)


class CH(AbsCH):
    def estimate(self):
        return super().estimate()


class CHReg(AbsCH):
    def estimate(self):
        estimation = super().estimate()
        return 10 ** ((math.log10(estimation) - 1.4208) / 0.6429)
