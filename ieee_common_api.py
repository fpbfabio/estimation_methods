import os
import pickle
import re
import time
import itertools
import math
import signal
from bs4 import BeautifulSoup
from selenium import webdriver

from abs_search_result import AbsSearchResult
from abs_base_common_api import AbsBaseCommonApi
from config import Config


class IEEECommonApi(AbsBaseCommonApi):
    _PAGE_LOAD_TIMEOUT = 300
    _ID_QUERY_STRING_VARIABLE = "arnumber"
    _WEB_DOMAIN = "http://ieeexplore.ieee.org"
    _HTML_PARSER = "lxml"
    _NO_RESULTS_TAG = "li"
    _NO_RESULTS_TAG_ATTRIBUTE = "class"
    _NO_RESULTS_TAG_ATTRIBUTE_VALUE = "article-list-item no-results ng-scope"
    _TITLE_TAG = True
    _TITLE_TAG_ATTRIBUTE = "ng-bind-html"
    _TITLE_TAG_ATTRIBUTE_VALUE = "::record.title"
    _ABSTRACT_TAG = "span"
    _ABSTRACT_TAG_ATTRIBUTE = "ng-bind-html"
    _ABSTRACT_TAG_ATTRIBUTE_VALUE = "::record.abstract"
    _ID_TAG = "a"
    _ID_TAG_ATTRIBUTE = "class"
    _ID_TAG_ATTRIBUTE_VALUE = "icon-pdf ng-scope"
    _HREF = "href"
    _CRAWL_DELAY = 1
    _MAX_RESULTS_PER_PAGE = 100
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE = "class"
    _ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE_VALUE = "ng-binding ng-scope"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE = "ng-if"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE_VALUE = "records.length === 1"
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
        soup = BeautifulSoup(web_page, IEEECommonApi._HTML_PARSER)
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
        dictionary = {IEEECommonApi._NO_RESULTS_TAG_ATTRIBUTE: IEEECommonApi._NO_RESULTS_TAG_ATTRIBUTE_VALUE}
        no_results_element = soup.find(IEEECommonApi._NO_RESULTS_TAG, dictionary)
        if no_results_element is not None:
            return 0
        dictionary = {IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE:
                      IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE_VALUE}
        one_result_element = soup.find(IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_TAG, dictionary)
        if one_result_element is not None:
            return 1
        dictionary = {IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE:
                      IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE_VALUE}
        try:
            html_element = soup.find(IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_TAG, dictionary)
            contents = html_element.next.strip().split()
            number_matches = int(str(contents[4].replace(",", "")))
        except:
            print("ERROR - Could not obtain number matches")
            os.kill(os.getpid(), signal.SIGUSR1)
            return 0
        return number_matches

    def _extract_data_list_from_soup(self, soup):
        dictionary = {IEEECommonApi._ID_TAG_ATTRIBUTE:
                      IEEECommonApi._ID_TAG_ATTRIBUTE_VALUE}
        id_tag_list = soup.find_all(IEEECommonApi._ID_TAG, dictionary)
        dictionary = {IEEECommonApi._TITLE_TAG_ATTRIBUTE:
                      IEEECommonApi._TITLE_TAG_ATTRIBUTE_VALUE}
        title_tag_list = soup.find_all(IEEECommonApi._TITLE_TAG, dictionary)
        data_list = [self._create_data(x[IEEECommonApi._HREF], y.text)
                     for x, y in zip(id_tag_list, title_tag_list)]
        size_id_tag_list = len(id_tag_list)
        size_data_list = len(data_list)
        if size_id_tag_list == 0:
            print("ERROR - Data extraction failure")
            os.kill(os.getpid(), signal.SIGUSR1)
        elif size_id_tag_list != size_data_list:
            print("ERROR - Inconsistent data extraction")
            os.kill(os.getpid(), signal.SIGUSR1)
        return data_list

    def _create_data(self, href, title):
        identifier = self._format_data_id(str(href))
        content = str(title)
        data = self.factory.create_data(identifier, content)
        return data

    def _format_data_id(self, href):
        return IEEECommonApi._WEB_DOMAIN + href

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
            return math.ceil((limit - number_downloaded_results) / IEEECommonApi._MAX_RESULTS_PER_PAGE)
        else:
            return math.ceil((number_matches - number_downloaded_results) / IEEECommonApi._MAX_RESULTS_PER_PAGE)

    def _attempt_download(self, query, offset):
        offset = (offset + IEEECommonApi._MAX_RESULTS_PER_PAGE) / IEEECommonApi._MAX_RESULTS_PER_PAGE
        offset = int(offset)
        dictionary = {IEEECommonApi._QUERY_MASK: query, IEEECommonApi._OFFSET_MASK: str(offset)}
        url = self._multiple_replace(dictionary, IEEECommonApi._BASE_URL)
        page_source = None
        for i in range(0, IEEECommonApi._DOWNLOAD_TRY_NUMBER):
            time.sleep(IEEECommonApi._CRAWL_DELAY)
            try:
                web_page = webdriver.Firefox()
                web_page.get(url)
                page_source = web_page.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
                web_page.close()
                self.inc_download()
                break
            except Exception as exception:
                page_source = None
                print(str(exception))
        if page_source is None:
            print("ERROR - Internet connection failure")
            os.kill(os.getpid(), signal.SIGUSR1)
        return page_source

    def _save_result(self, file_path, search_result):
        with open(file_path, "wb") as archive:
            pickle.dump(search_result, archive)

    def _do_additional_downloads(self, query, number_downloaded_results, number_additional_downloads):
        data_list = []
        for i in range(0, number_additional_downloads):
            offset = number_downloaded_results + i * IEEECommonApi._MAX_RESULTS_PER_PAGE
            web_page = self._attempt_download(query, offset)
            soup = BeautifulSoup(web_page, IEEECommonApi._HTML_PARSER)
            list_from_soup = self._extract_data_list_from_soup(soup)
            data_list = itertools.chain(data_list, list_from_soup)
        data_list = list(data_list)
        return data_list
