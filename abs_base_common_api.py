from abc import ABCMeta, abstractmethod
from threading import Thread, Lock
import re

from abs_common_api import AbsCommonApi
from common_api_factory import CommonApiFactory
from config import Config


class AbsBaseCommonApi(AbsCommonApi, metaclass=ABCMeta):
    @property
    @abstractmethod
    def query_pool_file_path(self):
        pass

    @property
    @abstractmethod
    def thread_limit(self):
        pass

    @property
    def download_count(self):
        return self.__download_count

    @download_count.setter
    def download_count(self, val):
        self.__download_count = val

    @property
    def factory(self):
        return self.__factory

    @factory.setter
    def factory(self, val):
        self.__factory = val

    def __init__(self):
        self.__download_count = 0
        self.__factory = CommonApiFactory()
        self.__lock = Lock()

    @abstractmethod
    def download(self, query, is_to_download_id=True, is_to_download_content=True,
                 offset=0, limit=Config.SEARCH_ENGINE_LIMIT):
        pass

    @abstractmethod
    def download_entire_data_set(self):
        pass

    def read_query_pool(self):
        query_pool = []
        # noinspection PyTypeChecker
        with open(self.query_pool_file_path) as archive:
            for line in archive:
                query_pool.append(line.rstrip("\n").rstrip("\r"))
        return query_pool

    def retrieve_number_matches(self, query):
        search_result = self.download(query, True, False, 0, 1)
        return search_result.number_results

    def inc_download(self):
        with self.__lock:
            self.download_count += 1

    def execute_in_parallel(self, collection, callback):
        thread_list = []
        for item in collection:
            if len(thread_list) >= self.thread_limit:
                thread_list[0].join()
                del (thread_list[0])
            thread = Thread(target=callback, args=(item,))
            thread_list.append(thread)
            thread.start()
        for thread in thread_list:
            thread.join()

    def report_progress(self, progress, total):
        print("Progress: " + str(progress) + "/" + str(total))

    def extract_words(self, text):
        word = []
        word_dictionary = {}
        count = 0
        letter_or_hyphen_pattern = re.compile(r"[a-z]|[A-Z]|-")
        for character in text:
            if letter_or_hyphen_pattern.match(character) is not None:
                word.append(character)
            else:
                word = str.join("", word)
                word = word.lower().strip("-").strip("-")
                if len(word) > 0 and word not in word_dictionary:
                    word_dictionary[word] = count
                    count += 1
                word = []
        return list(word_dictionary.keys())
