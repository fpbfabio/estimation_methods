from urllib.request import urlopen
from threading import Thread, Lock
import json
import re

from abs_common_api import AbsCommonApi
from common_api_factory import CommonApiFactory
from config import Config


class CommonApi(AbsCommonApi):
    DOCUMENT_LIST_KEY = "docs"
    NUMBER_MATCHES_KEY = "numFound"
    RESPONSE_KEY = "response"
    LOG_FILE_PERMISSION = "a+"
    ENCODING = "utf-8"

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
        self.lock = Lock()

    def read_query_pool(self):
        query_pool = []
        with open(Config.QUERY_POOL_FILE_PATH) as archive:
            for line in archive:
                query_pool.append(line.rstrip("\n").rstrip("\r"))
        return query_pool

    def download_entire_data_set(self):
        return self.download("*", True, True, 0, 1000000, "*")

    def retrieve_number_matches(self, query):
        search_result = self.download(query, True, False, 0, 1)
        return search_result.number_results

    def download(self, query, is_to_download_id=True, is_to_download_content=True, offset=0,
                 limit=Config.SEARCH_ENGINE_LIMIT, field_to_search=Config.FIELD_TO_SEARCH):
        url = Config.URL.replace(Config.LIMIT_MASK, str(limit))
        url = url.replace(Config.QUERY_MASK, str(query))
        url = url.replace(Config.FIELD_TO_SEARCH_MASK, field_to_search)
        url = url.replace(Config.OFFSET_MASK, str(offset))
        if is_to_download_id and is_to_download_content:
            url = url.replace(Config.FIELDS_TO_RETURN_MASK, Config.ID_FIELD + "," + Config.FIELD_TO_SEARCH)
        elif is_to_download_content and not is_to_download_id:
            url = url.replace(Config.FIELDS_TO_RETURN_MASK, Config.FIELD_TO_SEARCH)
        else:
            url = url.replace(Config.FIELDS_TO_RETURN_MASK, Config.ID_FIELD)
        response = urlopen(str(url))
        with self.lock:
            self.download_count += 1
        data = response.read().decode(CommonApi.ENCODING)
        dictionary = json.loads(data)
        dictionary = dictionary[CommonApi.RESPONSE_KEY]
        result_list = [self.factory.create_data(x.get(Config.ID_FIELD, None), x.get(Config.FIELD_TO_SEARCH, None)) for x
                       in dictionary[CommonApi.DOCUMENT_LIST_KEY]]
        search_result = self.factory.create_search_result(dictionary[CommonApi.NUMBER_MATCHES_KEY], result_list)
        return search_result

    def execute_in_parallel(self, collection, callback):
        thread_list = []
        for item in collection:
            if len(thread_list) > Config.THREAD_LIMIT:
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
