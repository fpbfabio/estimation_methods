import os
import pickle
import signal
import itertools
import re
import time
import math
from abc import ABCMeta, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from config import Config
from abs_base_common_api import AbsBaseCommonApi
from abs_search_result import AbsSearchResult


class AbsWebsiteCommonApi(AbsBaseCommonApi, metaclass=ABCMeta):
    _DATA_FILE_EXTENSION = ".pkl"
    _PAGE_LOAD_TIMEOUT = 30
    _CRAWL_DELAY = 1
    _DOWNLOAD_TRY_NUMBER = 5
    _OFFSET_MASK = "<<offset>>"
    _QUERY_MASK = "<<query>>"
    _HTML_PARSER = "lxml"
    _JAVASCRIPT_GET_PAGE_SOURCE_CODE = "return document.getElementsByTagName('html')[0].innerHTML"

    @property
    @abstractmethod
    def query_pool_file_path(self):
        pass

    @property
    @abstractmethod
    def thread_limit(self):
        pass

    @property
    @abstractmethod
    def base_url(self):
        pass

    @property
    @abstractmethod
    def max_results_per_page(self):
        pass

    @property
    @abstractmethod
    def data_folder_path(self):
        pass

    @abstractmethod
    def _extract_data_list_from_soup(self, soup):
        pass

    @abstractmethod
    def _extract_number_matches_from_soup(self, soup):
        pass

    @abstractmethod
    def _calculate_real_offset(self, offset):
        pass

    def download_entire_data_set(self):
        print("ERROR - Invalid operation")
        os.kill(os.getpid(), signal.SIGUSR1)
        return

    def download(self, query, is_to_download_id=True, is_to_download_content=True, offset=0,
                 limit=Config.SEARCH_ENGINE_LIMIT):
        file_path = self._build_file_path(query)
        if os.path.exists(file_path):
            search_result = self._get_saved_result(file_path)
            if search_result.number_results == 0:
                return search_result
            number_downloaded_results = len(search_result.results)
            number_additional_downloads = self._calculate_number_additional_downloads(search_result.number_results,
                                                                                      number_downloaded_results, limit)
            if number_additional_downloads > 0:
                data_list = self._do_additional_downloads(query, number_downloaded_results, number_additional_downloads)
                data_list = list(itertools.chain(search_result.results, data_list))
                search_result = self.factory.create_search_result(search_result.number_results, data_list)
                self._save_result(file_path, search_result)
            search_result = self._filter_result_content(search_result, is_to_download_id, is_to_download_content)
            return search_result
        web_page = self._attempt_download(query, offset)
        soup = BeautifulSoup(web_page, AbsWebsiteCommonApi._HTML_PARSER)
        number_matches = self._extract_number_matches_from_soup(soup)
        if number_matches == 0:
            search_result = self.factory.create_search_result(0, [])
            self._save_result(file_path, search_result)
            return search_result
        data_list = self._extract_data_list_from_soup(soup)
        # noinspection PyTypeChecker
        number_downloaded_results = len(data_list)
        # noinspection PyTypeChecker
        number_additional_downloads = self._calculate_number_additional_downloads(number_matches,
                                                                                  number_downloaded_results, limit)
        if number_additional_downloads > 0:
            additional_data_list = self._do_additional_downloads(query, number_downloaded_results,
                                                                 number_additional_downloads)
            data_list = list(itertools.chain(data_list, additional_data_list))
        search_result = self.factory.create_search_result(number_matches, data_list)
        self._save_result(file_path, search_result)
        search_result = self._filter_result_content(search_result, is_to_download_id, is_to_download_content)
        return search_result

    def _build_file_path(self, query):
        return self.data_folder_path + os.path.sep + query + AbsWebsiteCommonApi._DATA_FILE_EXTENSION

    def _get_saved_result(self, file_path):
        with open(file_path, "rb") as archive:
            search_result = pickle.load(archive)
            assert (isinstance(search_result, AbsSearchResult))
            return search_result

    def _do_additional_downloads(self, query, number_downloaded_results, number_additional_downloads):
        data_list = []
        for i in range(0, number_additional_downloads):
            # noinspection PyTypeChecker
            offset = number_downloaded_results + i * self.max_results_per_page
            web_page = self._attempt_download(query, offset)
            soup = BeautifulSoup(web_page, AbsWebsiteCommonApi._HTML_PARSER)
            list_from_soup = self._extract_data_list_from_soup(soup)
            data_list = itertools.chain(data_list, list_from_soup)
        data_list = list(data_list)
        return data_list

    def test_page_loaded(self, web_page):
        page_source = web_page.execute_script(AbsWebsiteCommonApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
        soup = BeautifulSoup(page_source, AbsWebsiteCommonApi._HTML_PARSER)
        return self._extract_number_matches_from_soup(soup) >= 0

    def _attempt_download(self, query, offset):
        real_offset = self._calculate_real_offset(offset)
        real_offset = int(real_offset)
        dictionary = {AbsWebsiteCommonApi._QUERY_MASK: query, AbsWebsiteCommonApi._OFFSET_MASK: str(real_offset)}
        url = self._multiple_replace(dictionary, self.base_url)
        page_source = None
        for i in range(0, AbsWebsiteCommonApi._DOWNLOAD_TRY_NUMBER):
            time.sleep(AbsWebsiteCommonApi._CRAWL_DELAY)
            web_page = webdriver.PhantomJS()
            web_page.get(url)
            wait = WebDriverWait(web_page, AbsWebsiteCommonApi._PAGE_LOAD_TIMEOUT)
            try:
                wait.until(self.test_page_loaded)
            except Exception as exception:
                print(str(exception))
                web_page.close()
                page_source = None
                continue
            page_source = web_page.execute_script(AbsWebsiteCommonApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
            web_page.close()
            self.inc_download()
            break
        if page_source is None:
            print("ERROR - Internet connection failure")
            os.kill(os.getpid(), signal.SIGUSR1)
        return page_source

    def _multiple_replace(self, dictionary, string):
        dictionary = dict((re.escape(k), v) for k, v in dictionary.items())
        pattern = re.compile("|".join(dictionary.keys()))
        return pattern.sub(lambda m: dictionary[re.escape(m.group(0))], string)

    def _calculate_number_additional_downloads(self, number_matches, number_downloaded_results, limit):
        if (number_matches <= self.max_results_per_page or
                number_downloaded_results == number_matches or
                number_downloaded_results >= limit):
            return 0
        elif number_matches > limit:
            return math.ceil((limit - number_downloaded_results) / self.max_results_per_page)
        else:
            return math.ceil((number_matches - number_downloaded_results) / self.max_results_per_page)

    def _save_result(self, file_path, search_result):
        if search_result.number_results < len(search_result.results):
            print("ERROR - Search result corrupted - " + file_path)
            os.kill(os.getpid(), signal.SIGUSR1)
            return
        with open(file_path, "wb") as archive:
            pickle.dump(search_result, archive)

    def _filter_result_content(self, search_result, is_to_have_id, is_to_have_content):
        if is_to_have_content and not is_to_have_id:
            data_list = [self.factory.create_data(None, x.content) for x in search_result.results]
        elif is_to_have_id and not is_to_have_content:
            data_list = [self.factory.create_data(x.identifier, None) for x in search_result.results]
        else:
            return search_result
        return self.factory.create_search_result(search_result.number_results, data_list)
