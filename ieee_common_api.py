import os
import pickle
import re
import time
import itertools
from bs4 import BeautifulSoup
from selenium import webdriver
from abs_search_result import AbsSearchResult
from abs_base_common_api import AbsBaseCommonApi
from config import Config


class IEEECommonApi(AbsBaseCommonApi):
    _TITLE_TAG_ATTRIBUTE = "ng-bind-html"
    _TITLE_TAG_ATTRIBUTE_VALUE = "::record.title"
    _ABSTRACT_TAG_ATTRIBUTE = "ng-bind-html"
    _ABSTRACT_TAG_ATTRIBUTE_VALUE = "::record.abstract"
    _HREF = "href"
    _CLASS = "class"
    _A_TAG = "a"
    _CRAWL_DELAY = 1
    _MAX_RESULTS_PER_PAGE = 100
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_CLASS = "ng-binding ng-scope"
    _DOWNLOAD_TRY_NUMBER = 5
    _BASE_URL = ("http://ieeexplore.ieee.org/search/searchresult.jsp?"
                 + "queryText=<<query>>&rowsPerPage=100&pageNumber=<<page_number>>&resultAction=ROWS_PER_PAGE")
    _QUERY_MASK = "<<query>>"
    _OFFSET_MASK = "<<page_number>>"
    _FILE_EXTENSION = ".pickle"
    _DATA_FOLDER_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs"

    def __init__(self):
        super().__init__()

    def download_entire_data_set(self):
        raise NotImplementedError("Invalid operation")

    def download(self, query, is_to_download_id=True, is_to_download_content=True,
                 offset=0, limit=Config.SEARCH_ENGINE_LIMIT):
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
        soup = BeautifulSoup(web_page)
        number_matches = self._extract_number_matches_from_soup(soup)
        if number_matches == 0:
            search_result = self.factory.create_search_result(0, [])
            self._save_result(file_path, search_result)
            return search_result
        data_list = self._extract_data_list_from_soup(soup)
        number_downloaded_results = len(data_list)
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

    def _filter_result_content(self, search_result, is_to_have_id, is_to_have_content):
        if is_to_have_content and not is_to_have_id:
            data_list = [self.factory.create_data(None, x.content) for x in search_result.results]
        elif is_to_have_id and not is_to_have_content:
            data_list = [self.factory.create_data(x.identifier, None) for x in search_result.results]
        else:
            return search_result
        return self.factory.create_search_result(search_result.number_results, data_list)

    def _extract_number_matches_from_soup(self, soup):
        dictionary = {IEEECommonApi._CLASS: IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_CLASS}
        try:
            html_element = soup.find(IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_TAG, dictionary)
            number_matches = int(str(html_element.next.strip().split()[4].replace(",", "")))
        except:
            number_matches = 0
        return number_matches

    def _extract_data_list_from_soup(self, soup):
        dictionary = {IEEECommonApi._TITLE_TAG_ATTRIBUTE:
                      IEEECommonApi._TITLE_TAG_ATTRIBUTE_VALUE}
        a_tag_list = soup.find_all(IEEECommonApi._A_TAG, dictionary)
        data_list = [self.factory.create_data(x[IEEECommonApi._HREF], str(x.text)) for x in a_tag_list]
        return data_list

    def _build_file_path(self, query):
        return IEEECommonApi._DATA_FOLDER_PATH + os.path.sep + query + IEEECommonApi._FILE_EXTENSION

    def _multiple_replace(self, dictionary, string):
        dictionary = dict((re.escape(k), v) for k, v in dictionary.items())
        pattern = re.compile("|".join(dictionary.keys()))
        return pattern.sub(lambda m: dictionary[re.escape(m.group(0))], string)

    def _get_saved_result(self, file_path):
        with open(file_path, "rb") as archive:
            search_result = pickle.load(archive)
            assert (isinstance(search_result, AbsSearchResult))
            return search_result

    def _calculate_number_additional_downloads(self, number_matches, number_downloaded_results, limit):
        if (number_matches <= IEEECommonApi._MAX_RESULTS_PER_PAGE or
                number_downloaded_results == number_matches or
                number_downloaded_results >= limit):
            return 0
        elif number_matches > limit:
            return int((limit - number_downloaded_results) / IEEECommonApi._MAX_RESULTS_PER_PAGE)
        else:
            return int((number_matches - number_downloaded_results) / IEEECommonApi._MAX_RESULTS_PER_PAGE)

    def _attempt_download(self, query, offset):
        offset = (offset + IEEECommonApi._MAX_RESULTS_PER_PAGE) / IEEECommonApi._MAX_RESULTS_PER_PAGE
        offset = int(offset)
        dictionary = {IEEECommonApi._QUERY_MASK: query, IEEECommonApi._OFFSET_MASK: str(offset)}
        url = self._multiple_replace(dictionary, IEEECommonApi._BASE_URL)
        print(url)
        web_page = None
        for i in range(0, IEEECommonApi._DOWNLOAD_TRY_NUMBER):
            time.sleep(IEEECommonApi._CRAWL_DELAY)
            try:
                web_page = webdriver.Firefox()
                web_page.get(url)
                web_page = web_page.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                self.inc_download()
                break
            except Exception as exception:
                web_page = None
                print(str(exception))
        return web_page

    def _save_result(self, file_path, search_result):
        with open(file_path, "wb") as archive:
            pickle.dump(search_result, archive)

    def _do_additional_downloads(self, query, number_downloaded_results, number_additional_downloads):
        data_list = []
        for i in range(0, number_additional_downloads):
            web_page = self._attempt_download(query, number_downloaded_results
                                              + i * IEEECommonApi._MAX_RESULTS_PER_PAGE)
            soup = BeautifulSoup(web_page)
            data_list = itertools.chain(data_list, self._extract_data_list_from_soup(soup))
        data_list = list(data_list)
        return data_list
