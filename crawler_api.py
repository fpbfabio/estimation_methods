""""
This is the module that provides an abstract interface for a class
with the functions used in common in all estimators.
"""

from abc import ABCMeta, abstractmethod
import json
import os
import re
from threading import Lock
import itertools
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pickle
import math
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time

from crawler_api_factory import CrawlerApiFactory


class AbsCrawlerApi(metaclass=ABCMeta):
    """
    Contains common methods that are needed by all estimation algorithm classes.
    """

    @property
    @abstractmethod
    def thread_limit(self):
        pass

    @property
    @abstractmethod
    def download_count(self):
        """
        Returns the number of downloads.
        """
        pass

    @download_count.setter
    @abstractmethod
    def download_count(self, val):
        """
        Sets the number of downloads.
        """
        pass

    @property
    @abstractmethod
    def factory(self):
        """
        Returns the instance of an AbsCommonApiFactory class.
        """
        pass

    @factory.setter
    @abstractmethod
    def factory(self, val):
        """
        Sets the instance of an AbsCommonApiFactory class.
        """
        pass

    @property
    @abstractmethod
    def terminator(self):
        """
        Returns the instance of an AbsTerminator class.
        """
        pass

    @terminator.setter
    @abstractmethod
    def terminator(self, val):
        """
        Sets the instance of an AbsTerminator class.
        """
        pass

    @abstractmethod
    def download_entire_data_set(self):
        """
        Returns a list with all the documents from the data set.
        """
        pass

    @abstractmethod
    def retrieve_number_matches(self, query):
        """
        Returns the number of matches in the search engine for the given query.
        """
        pass

    @abstractmethod
    def download(self, query, is_to_download_id=True, is_to_download_content=True, offset=0, limit=None):
        """
        Returns the a list with documents retrieved by the given query with
        the max size set by the given limit.
        """
        pass


class AbsBaseCrawlerApi(AbsCrawlerApi, metaclass=ABCMeta):

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

    @property
    def terminator(self):
        return self.__terminator

    @terminator.setter
    def terminator(self, val):
        self.__terminator = val

    def __init__(self):
        self.__download_count = 0
        self.__factory = CrawlerApiFactory()
        self.__lock = Lock()
        self.__terminator = self.__factory.create_terminator()

    @abstractmethod
    def download(self, query, is_to_download_id=True, is_to_download_content=True, offset=0, limit=None):
        pass

    @abstractmethod
    def download_entire_data_set(self):
        pass

    def retrieve_number_matches(self, query):
        search_result = self.download(query, True, False, 0, 1)
        return search_result.number_results

    def inc_download(self):
        with self.__lock:
            self.download_count += 1

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


class AbsWebsiteCrawlerApi(AbsBaseCrawlerApi, metaclass=ABCMeta):

    _NUMBER_ATTEMPTS_GET_EXPECTED_AMOUNT_OF_DATA = 5
    _DATA_FILE_EXTENSION = ".pkl"
    _PAGE_LOAD_TIMEOUT = 30
    _CRAWL_DELAY = 1
    _DOWNLOAD_TRY_NUMBER = 10000
    _OFFSET_MASK = "<<offset>>"
    _QUERY_MASK = "<<query>>"
    _HTML_PARSER = "lxml"
    _JAVASCRIPT_GET_PAGE_SOURCE_CODE = "return document.getElementsByTagName('html')[0].innerHTML"

    @property
    @abstractmethod
    def _limit_results(self):
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
    def _calculate_offset(self, offset):
        pass

    @abstractmethod
    def _handle_inconsistent_page(self, page_data_list):
        pass

    @abstractmethod
    def __init__(self):
        super().__init__()
        self._clean_up_data_folder()

    def download_entire_data_set(self):
        self.terminator.terminate("ERROR - INVALID OPERATION")

    def download(self, query, is_to_download_id=True, is_to_download_content=True, offset=0, limit=None):
        file_path = self._build_file_path(query)
        search_result = self._download_based_on_stored_file(query, file_path)
        if search_result is None:
            search_result = self._download_completely_from_web(query, file_path)
        search_result = self._filter_result_content(search_result, is_to_download_id,
                                                    is_to_download_content, offset, limit)
        return search_result

    def _clean_up_data_folder(self):
        for the_file in os.listdir(self.data_folder_path):
            file_path = os.path.join(self.data_folder_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except:
                pass

    def _download_more_results_if_needed(self, query, number_matches, data_list):
        number_downloaded_results = len(data_list)
        if number_downloaded_results > number_matches:
            return self.factory.create_search_result(number_matches, data_list)
        number_additional_downloads = self._calculate_number_additional_downloads(number_matches,
                                                                                  number_downloaded_results)
        if number_additional_downloads > 0:
            additional_data_list = self._do_additional_downloads(query, number_downloaded_results,
                                                                 number_additional_downloads, number_matches)
            data_list = list(itertools.chain(data_list, additional_data_list))
        search_result = self.factory.create_search_result(number_matches, data_list)
        return search_result

    def _download_based_on_stored_file(self, query, file_path):
        if not os.path.exists(file_path):
            return None
        search_result = self._get_saved_result(file_path)
        return search_result

    def _download_completely_from_web(self, query, file_path):
        web_page = self._attempt_download(query, 0)
        soup = BeautifulSoup(web_page, AbsWebsiteCrawlerApi._HTML_PARSER)
        number_matches = self._extract_number_matches_from_soup(soup)
        if number_matches == 0:
            search_result = self.factory.create_search_result(0, [])
            self._save_result(file_path, search_result)
            return search_result
        data_list = self._extract_data_list_from_soup(soup)
        if not self._is_expected_amount_of_data(data_list, number_matches, 0):
            data_list = self._download_until_expected_amount_of_data_is_extracted(query, number_matches, 0)
        search_result = self._download_more_results_if_needed(query, number_matches, data_list)
        if len(search_result.results) != number_matches:
            print("ERROR - NUMBER OF DATA ITEMS != NUMBER OF MATCHES IN QUERY =  " + query)
            print("ERROR IGNORED")
        self._save_result(file_path, search_result)
        return search_result

    def _do_additional_downloads(self, query, starting_number_downloaded_results,
                                 number_additional_downloads, number_matches):
        data_list = []
        for i in range(0, number_additional_downloads):
            number_downloaded_results = starting_number_downloaded_results + i * self.max_results_per_page
            list_from_soup = self._download_until_expected_amount_of_data_is_extracted(query, number_matches,
                                                                                       number_downloaded_results)
            data_list = itertools.chain(data_list, list_from_soup)
        data_list = list(data_list)
        return data_list

    def _is_expected_amount_of_data(self, data_list, number_matches, number_previously_downloaded_results):
        if number_matches - number_previously_downloaded_results >= self.max_results_per_page:
            return len(data_list) == self.max_results_per_page
        else:
            return len(data_list) == number_matches % self.max_results_per_page

    def _download_until_expected_amount_of_data_is_extracted(self, query, number_matches, number_downloaded_results):
        list_from_soup = []
        for i in range(0, AbsWebsiteCrawlerApi._NUMBER_ATTEMPTS_GET_EXPECTED_AMOUNT_OF_DATA):
            web_page = self._attempt_download(query, number_downloaded_results)
            soup = BeautifulSoup(web_page, AbsWebsiteCrawlerApi._HTML_PARSER)
            list_from_soup = self._extract_data_list_from_soup(soup)
            if self._is_expected_amount_of_data(list_from_soup, number_matches, number_downloaded_results):
                return list_from_soup
            else:
                print("DETECTED INCONSISTENCY")
                print("NUMBER OF ITEMS IN THE PAGE = " + str(len(list_from_soup)))
                print("NUMBER OF DOWNLOADED RESULTS = " + str(number_downloaded_results))
                print("NUMBER OF MATCHES = " + str(number_matches))
                print("NUMBER OF RESULTS PER PAGE = " + str(self.max_results_per_page))
                print("QUERY = " + str(query))
        print("INCONSISTENCY COULD NOT BE SOLVED")
        list_from_soup = self._handle_inconsistent_page(list_from_soup)
        return list_from_soup

    def _build_file_path(self, query):
        return self.data_folder_path + os.path.sep + query + AbsWebsiteCrawlerApi._DATA_FILE_EXTENSION

    def _get_saved_result(self, file_path):
        try:
            with open(file_path, "rb") as archive:
                search_result = pickle.load(archive)
        except:
            search_result = None
        return search_result

    def _test_page_loaded(self, web_page):
        page_source = web_page.execute_script(AbsWebsiteCrawlerApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
        soup = BeautifulSoup(page_source, AbsWebsiteCrawlerApi._HTML_PARSER)
        return self._extract_number_matches_from_soup(soup) >= 0

    def _attempt_download(self, query, number_items_already_downloaded):
        offset = self._calculate_offset(number_items_already_downloaded)
        dictionary = {AbsWebsiteCrawlerApi._QUERY_MASK: query, AbsWebsiteCrawlerApi._OFFSET_MASK: str(offset)}
        url = self._multiple_replace(dictionary, self.base_url)
        page_source = None
        for i in range(0, AbsWebsiteCrawlerApi._DOWNLOAD_TRY_NUMBER):
            time.sleep(AbsWebsiteCrawlerApi._CRAWL_DELAY)
            web_page = None
            try:
                web_page = webdriver.PhantomJS()
                web_page.get(url)
                wait = WebDriverWait(web_page, AbsWebsiteCrawlerApi._PAGE_LOAD_TIMEOUT)
                wait.until(self._test_page_loaded)
                page_source = web_page.execute_script(AbsWebsiteCrawlerApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
            except Exception as exception:
                if web_page is not None:
                    web_page.close()
                    web_page.quit()
                page_source = None
                continue
            web_page.close()
            web_page.quit()
            self.inc_download()
            break
        if page_source is None:
            self.terminator.terminate("ERROR - INTERNET CONNECTION FAILURE")
        return page_source

    def _multiple_replace(self, dictionary, string):
        dictionary = dict((re.escape(k), v) for k, v in dictionary.items())
        pattern = re.compile("|".join(dictionary.keys()))
        return pattern.sub(lambda m: dictionary[re.escape(m.group(0))], string)

    def _calculate_number_additional_downloads(self, number_matches, number_downloaded_results):
        if number_matches <= self.max_results_per_page or number_downloaded_results == number_matches:
            return 0
        else:
            return math.ceil((number_matches - number_downloaded_results) / self.max_results_per_page)

    def _save_result(self, file_path, search_result):
        with open(file_path, "wb") as archive:
            pickle.dump(search_result, archive)

    def _filter_result_content(self, search_result, is_to_have_id, is_to_have_content, offset=None, limit=None):
        if is_to_have_content and not is_to_have_id:
            data_list = [self.factory.create_data(None, x.content) for x in search_result.results]
        elif is_to_have_id and not is_to_have_content:
            data_list = [self.factory.create_data(x.identifier, None) for x in search_result.results]
        else:
            data_list = search_result.results
        if search_result.number_results != 0:
            if limit is not None and limit >= search_result.number_results:
                limit = None
            if offset is not None and limit is not None:
                data_list = data_list[offset:limit]
            elif offset is not None and limit is None:
                data_list = data_list[offset:]
            elif offset is None and limit is not None:
                data_list = data_list[0:limit]
        return self.factory.create_search_result(search_result.number_results, data_list)


class SolrCrawlerApi(AbsBaseCrawlerApi):

    DATA_SET_SIZE = 19994
    LIMIT_RESULTS = 5000000
    _QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    _THREAD_LIMIT = 5
    _URL = ("http://localhost:8984/solr/experiment/select?"
            + "q=::FIELD:::::QUERY::&start=::OFFSET::&rows=::LIMIT::&fl=::FIELDS_TO_RETURN::&wt=json")
    _ID_FIELD = "id"
    _FIELD_TO_SEARCH = "text"
    _DOCUMENT_LIST_KEY = "docs"
    _NUMBER_MATCHES_KEY = "numFound"
    _OFFSET_MASK = "::OFFSET::"
    _LIMIT_MASK = "::LIMIT::"
    _FIELD_TO_SEARCH_MASK = "::FIELD::"
    _FIELDS_TO_RETURN_MASK = "::FIELDS_TO_RETURN::"
    _QUERY_MASK = "::QUERY::"
    _RESPONSE_KEY = "response"
    _ENCODING = "utf-8"

    @property
    def thread_limit(self):
        return SolrCrawlerApi._THREAD_LIMIT

    @property
    def query_pool_file_path(self):
        return SolrCrawlerApi._QUERY_POOL_FILE_PATH

    def __init__(self):
        super().__init__()

    def download_entire_data_set(self):
        return self._download("*", True, True, 0, 1000000, "*")

    def download(self, query, is_to_download_id=True, is_to_download_content=True,
                 offset=0, limit=None):
        if limit is not None:
            result = self._download(query, is_to_download_id, is_to_download_content, offset, limit,
                                    SolrCrawlerApi._FIELD_TO_SEARCH)
        else:
            result = self._download(query, is_to_download_id, is_to_download_content, offset,
                                    SolrCrawlerApi.LIMIT_RESULTS, SolrCrawlerApi._FIELD_TO_SEARCH)
        return result

    def _download(self, query, is_to_download_id, is_to_download_content, offset, limit, field_to_search):
        url = SolrCrawlerApi._URL.replace(SolrCrawlerApi._LIMIT_MASK, str(limit))
        url = url.replace(SolrCrawlerApi._QUERY_MASK, str(query))
        url = url.replace(SolrCrawlerApi._FIELD_TO_SEARCH_MASK, field_to_search)
        url = url.replace(SolrCrawlerApi._OFFSET_MASK, str(offset))
        if is_to_download_id and is_to_download_content:
            url = url.replace(SolrCrawlerApi._FIELDS_TO_RETURN_MASK,
                              SolrCrawlerApi._ID_FIELD + "," + SolrCrawlerApi._FIELD_TO_SEARCH)
        elif is_to_download_content and not is_to_download_id:
            url = url.replace(SolrCrawlerApi._FIELDS_TO_RETURN_MASK, SolrCrawlerApi._FIELD_TO_SEARCH)
        else:
            url = url.replace(SolrCrawlerApi._FIELDS_TO_RETURN_MASK, SolrCrawlerApi._ID_FIELD)
        response = urlopen(str(url))
        self.inc_download()
        data = response.read().decode(SolrCrawlerApi._ENCODING)
        dictionary = json.loads(data)
        dictionary = dictionary[SolrCrawlerApi._RESPONSE_KEY]
        result_list = [
            self.factory.create_data(x.get(SolrCrawlerApi._ID_FIELD, None),
                                     x.get(SolrCrawlerApi._FIELD_TO_SEARCH, None))
            for x
            in dictionary[SolrCrawlerApi._DOCUMENT_LIST_KEY]]
        search_result = self.factory.create_search_result(int(dictionary[SolrCrawlerApi._NUMBER_MATCHES_KEY]),
                                                          result_list)
        return search_result


class AbsIEEECrawlerApi(AbsWebsiteCrawlerApi, metaclass=ABCMeta):

    _DATA_SET_SIZE_TAG = "a"
    _DATA_SET_SIZE_TAG_ATTRIBUTE = "href"
    _DATA_SET_SIZE_TAG_ATTRIBUTE_VALUE = "/search/searchresult.jsp?sortType=desc_p_Publication_Year&newsearch=true"
    DATA_SET_SIZE = 3707749
    LIMIT_RESULTS = 5000000
    _THREAD_LIMIT = 1
    _WEB_DOMAIN = "http://ieeexplore.ieee.org"
    _NO_RESULTS_TAG = "li"
    _NO_RESULTS_TAG_ATTRIBUTE = "class"
    _NO_RESULTS_TAG_ATTRIBUTE_VALUE = "article-list-item no-results ng-scope"
    _ITEM_TAG = "li"
    _ITEM_TAG_ATTRIBUTE = "class"
    _ITEM_TAG_ATTRIBUTE_VALUE = "article-list-item ng-scope"
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
    _MAX_RESULTS_PER_PAGE = 100
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE = "class"
    _ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE_VALUE = "ng-binding ng-scope"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE = "ng-if"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE_VALUE = "records.length === 1"
    _DATA_FOLDER_PATH = "/media/fabio/FABIO/ieee"

    def __init__(self):
        super().__init__()

    @property
    @abstractmethod
    def base_url(self):
        pass

    @property
    def _limit_results(self):
        return AbsIEEECrawlerApi.LIMIT_RESULTS

    @property
    def thread_limit(self):
        return AbsIEEECrawlerApi._THREAD_LIMIT

    @property
    def max_results_per_page(self):
        return AbsIEEECrawlerApi._MAX_RESULTS_PER_PAGE

    @property
    def data_folder_path(self):
        return AbsIEEECrawlerApi._DATA_FOLDER_PATH

    @staticmethod
    def _extract_data_set_size(soup):
        dictionary = {AbsIEEECrawlerApi._DATA_SET_SIZE_TAG_ATTRIBUTE:
                      AbsIEEECrawlerApi._DATA_SET_SIZE_TAG_ATTRIBUTE_VALUE}
        soup = soup.find(AbsIEEECrawlerApi._DATA_SET_SIZE_TAG, dictionary)
        if soup is None:
            return -1
        data_set_size = int(str(soup.next).replace(",", ""))
        return data_set_size

    @staticmethod
    def _test_if_page_with_data_set_size_loaded(web_driver):
        page_source = web_driver.execute_script(AbsWebsiteCrawlerApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
        soup = BeautifulSoup(page_source, AbsWebsiteCrawlerApi._HTML_PARSER)
        return AbsIEEECrawlerApi._extract_data_set_size(soup) != -1

    @staticmethod
    def get_data_set_size():
        web_driver = webdriver.PhantomJS()
        web_driver.get(AbsIEEECrawlerApi._WEB_DOMAIN)
        wait = WebDriverWait(web_driver, AbsWebsiteCrawlerApi._PAGE_LOAD_TIMEOUT)
        wait.until(AbsIEEECrawlerApi._test_if_page_with_data_set_size_loaded)
        page_source = web_driver.execute_script(AbsWebsiteCrawlerApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
        soup = BeautifulSoup(page_source, AbsWebsiteCrawlerApi._HTML_PARSER)
        return AbsIEEECrawlerApi._extract_data_set_size(soup)

    def _calculate_offset(self, offset):
        return int((offset + self.max_results_per_page) / self.max_results_per_page)

    def _handle_inconsistent_page(self, page_data_list):
        return []

    def _extract_number_matches_from_soup(self, soup):
        dictionary = {AbsIEEECrawlerApi._NO_RESULTS_TAG_ATTRIBUTE:
                      AbsIEEECrawlerApi._NO_RESULTS_TAG_ATTRIBUTE_VALUE}
        no_results_element = soup.find(AbsIEEECrawlerApi._NO_RESULTS_TAG, dictionary)
        if no_results_element is not None:
            return 0
        dictionary = {AbsIEEECrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE:
                      AbsIEEECrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE_VALUE}
        one_result_element = soup.find(AbsIEEECrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_TAG,
                                       dictionary)
        if one_result_element is not None:
            return 1
        dictionary = {AbsIEEECrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE:
                      AbsIEEECrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE_VALUE}
        html_element = soup.find(AbsIEEECrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_TAG, dictionary)
        if html_element is not None:
            try:
                contents = html_element.next.strip().split()
                number_matches = int(str(contents[4].replace(",", "")))
            except:
                return -1
        else:
            return -1
        return number_matches

    def _extract_data_list_from_soup(self, soup):
        dictionary = {AbsIEEECrawlerApi._ITEM_TAG_ATTRIBUTE: AbsIEEECrawlerApi._ITEM_TAG_ATTRIBUTE_VALUE}
        item_tag_list = soup.find_all(AbsIEEECrawlerApi._ITEM_TAG, dictionary)

        def extract_data(item):
            dictio = {AbsIEEECrawlerApi._ID_TAG_ATTRIBUTE: AbsIEEECrawlerApi._ID_TAG_ATTRIBUTE_VALUE}
            identifier_tag = item.find(AbsIEEECrawlerApi._ID_TAG, dictio)
            dictio = {AbsIEEECrawlerApi._TITLE_TAG_ATTRIBUTE: AbsIEEECrawlerApi._TITLE_TAG_ATTRIBUTE_VALUE}
            title_tag = item.find(AbsIEEECrawlerApi._TITLE_TAG, dictio)
            dictio = {AbsIEEECrawlerApi._ABSTRACT_TAG_ATTRIBUTE:
                      AbsIEEECrawlerApi._ABSTRACT_TAG_ATTRIBUTE_VALUE}
            abstract_tag = item.find(AbsIEEECrawlerApi._ABSTRACT_TAG, dictio)
            if identifier_tag is not None and title_tag is not None:
                if abstract_tag is not None:
                    data = self._create_data(identifier_tag[AbsIEEECrawlerApi._HREF], title_tag.text,
                                             abstract_tag.text)
                else:
                    data = self._create_data(identifier_tag[AbsIEEECrawlerApi._HREF], title_tag.text)
                return data
            elif identifier_tag is None and title_tag is not None:
                ampersand_index = title_tag[AbsIEEECrawlerApi._HREF].find("&")
                if abstract_tag is not None:
                    data = self._create_data(title_tag[AbsIEEECrawlerApi._HREF][0:ampersand_index],
                                             title_tag.text, abstract_tag.text)
                else:
                    data = self._create_data(title_tag[AbsIEEECrawlerApi._HREF][0:ampersand_index],
                                             title_tag.text)
                return data
            else:
                self.terminator.terminate("ERROR - Data extraction failure - " + str(item))

        data_list = [extract_data(x) for x in item_tag_list]
        return data_list

    def _create_data(self, href, title, abstract=None):
        identifier = self._format_data_id(str(href))
        content = self._format_data_content(title, abstract)
        data = self.factory.create_data(identifier, content)
        return data

    def _format_data_id(self, href):
        return AbsIEEECrawlerApi._WEB_DOMAIN + href

    def _format_data_content(self, title, abstract):
        if abstract is not None:
            return str(title) + os.linesep + os.linesep + str(abstract)
        else:
            return str(title)


class IEEECrawlerApi(AbsIEEECrawlerApi):

    _BASE_URL = ("http://ieeexplore.ieee.org/search/searchresult.jsp?"
                 + "queryText=<<query>>&rowsPerPage=100&pageNumber=<<offset>>&resultAction=ROWS_PER_PAGE")

    def __init__(self):
        super().__init__()

    @property
    def base_url(self):
        return IEEECrawlerApi._BASE_URL


class IEEEOnlyTitleCrawlerApi(AbsIEEECrawlerApi):

    _BASE_URL = ("http://ieeexplore.ieee.org/search/searchresult.jsp?"
                 + "queryText=(\"Document%20Title\":<<query>>)&"
                 + "rowsPerPage=100&pageNumber=<<offset>>&resultAction=ROWS_PER_PAGE")

    def __init__(self):
        super().__init__()

    @property
    def base_url(self):
        return IEEEOnlyTitleCrawlerApi._BASE_URL


class AbsACMCrawlerApi(AbsWebsiteCrawlerApi):

    DATA_SET_SIZE = 446154
    LIMIT_RESULTS = 5000000
    _THREAD_LIMIT = 1
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "b"
    _DATA_FOLDER_PATH = "/media/fabio/FABIO/acm"
    _MAX_RESULTS_PER_PAGE = 20
    _WEB_DOMAIN = "http://dl.acm.org/"
    _NO_RESULTS_TAG = "font"
    _NO_RESULTS_TAG_ATTRIBUTE = "size"
    _NO_RESULTS_TAG_ATTRIBUTE_VALUE = "+1"
    _TITLE_TAG_ID_ATTRIBUTE = "href"
    _TITLE_TAG = "a"
    _TITLE_TAG_ATTRIBUTE = "class"
    _TITLE_TAG_ATTRIBUTE_VALUE = "medium-text"
    _ABSTRACT_TAG = "div"
    _ABSTRACT_TAG_ATTRIBUTE = "class"
    _ABSTRACT_TAG_ATTRIBUTE_VALUE = "abstract2"

    def __init__(self):
        super().__init__()

    @property
    def _limit_results(self):
        return AbsACMCrawlerApi.LIMIT_RESULTS

    @property
    def thread_limit(self):
        return AbsACMCrawlerApi._THREAD_LIMIT

    @property
    def max_results_per_page(self):
        return AbsACMCrawlerApi._MAX_RESULTS_PER_PAGE

    @property
    def data_folder_path(self):
        return AbsACMCrawlerApi._DATA_FOLDER_PATH

    @abstractmethod
    @property
    def base_url(self):
        pass

    def _handle_inconsistent_page(self, page_data_list):
        return page_data_list

    def _calculate_offset(self, offset):
        return int(2 * offset / self.max_results_per_page)

    def _extract_data_list_from_soup(self, soup):
        dictionary = {AbsACMCrawlerApi._TITLE_TAG_ATTRIBUTE: AbsACMCrawlerApi._TITLE_TAG_ATTRIBUTE_VALUE}
        title_tag_list = soup.find_all(AbsACMCrawlerApi._TITLE_TAG, dictionary)
        dictionary = {AbsACMCrawlerApi._ABSTRACT_TAG_ATTRIBUTE: AbsACMCrawlerApi._ABSTRACT_TAG_ATTRIBUTE_VALUE}
        abstract_list = [x.parent.parent.parent.find(AbsACMCrawlerApi._ABSTRACT_TAG, dictionary) for x in
                         title_tag_list]
        data_list = [self._create_data(x[AbsACMCrawlerApi._TITLE_TAG_ID_ATTRIBUTE], x.text, y)
                     for x, y in zip(title_tag_list, abstract_list)]
        return data_list

    def _extract_number_matches_from_soup(self, soup):
        dictionary = {AbsACMCrawlerApi._NO_RESULTS_TAG_ATTRIBUTE: AbsACMCrawlerApi._NO_RESULTS_TAG_ATTRIBUTE_VALUE}
        no_results_element = soup.find(AbsACMCrawlerApi._NO_RESULTS_TAG, dictionary)
        if no_results_element is not None:
            return 0
        html_element = soup.find(AbsACMCrawlerApi._ELEMENT_WITH_NUMBER_MATCHES_TAG)
        if html_element is not None:
            try:
                number_matches = int(str(html_element.text.replace(",", "")))
            except:
                return -1
        else:
            return -1
        return number_matches

    def _create_data(self, href, title, abstract_tag):
        identifier = AbsACMCrawlerApi._WEB_DOMAIN + href[0:href.find("&")]
        if abstract_tag is not None:
            content = str(title) + os.linesep + str(abstract_tag.text)
        else:
            content = str(title)
        data = self.factory.create_data(identifier, content)
        return data


class ACMCrawlerApi(AbsACMCrawlerApi):

    _BASE_URL = "http://dl.acm.org/results.cfm?query=<<query>>&start=<<offset>>1&dlr=ACM"

    @property
    def base_url(self):
        return ACMCrawlerApi._BASE_URL


class ACMOnlyTitleCrawlerApi(AbsACMCrawlerApi):

    _BASE_URL = ("http://dl.acm.org/results.cfm?within=<<query>>&adv=1&termzone=Title&" +
                 "allofem=<<query>>&start=<<offset>>&dlr=ACM")

    @property
    def base_url(self):
        return ACMOnlyTitleCrawlerApi._BASE_URL
