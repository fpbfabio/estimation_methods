import abc
import json
import os
import re
import threading
import itertools
import urllib.request
import bs4
import pickle
import math
import selenium
import time
from selenium.webdriver.support.wait import WebDriverWait

import module_factory


class AbsCrawlerApi(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def thread_limit(self):
        pass

    @property
    @abc.abstractmethod
    def download_count(self):
        pass

    @download_count.setter
    @abc.abstractmethod
    def download_count(self, val):
        pass

    @property
    @abc.abstractmethod
    def limit_results_per_query(self):
        pass

    @limit_results_per_query.setter
    @abc.abstractmethod
    def limit_results_per_query(self, val):
        pass

    @property
    @abc.abstractmethod
    def factory(self):
        pass

    @factory.setter
    @abc.abstractmethod
    def factory(self, val):
        pass

    @abc.abstractmethod
    def download_entire_data_set(self):
        pass

    @classmethod
    @abc.abstractmethod
    def get_data_set_size(cls):
        pass

    @abc.abstractmethod
    def download_item(self, query, index):
        pass

    @abc.abstractmethod
    def download(self, query, is_to_download_id=True, is_to_download_content=True):
        pass

    @abc.abstractmethod
    def clean_up_data_folder(self):
        pass


class AbsBaseCrawlerApi(AbsCrawlerApi, metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
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
    def limit_results_per_query(self):
        return self.__limit_results_per_query

    @limit_results_per_query.setter
    def limit_results_per_query(self, val):
        self.__limit_results_per_query = val

    @property
    def _terminator(self):
        return self.__terminator

    @_terminator.setter
    def _terminator(self, val):
        self.__terminator = val

    def __init__(self, limit_results_per_query):
        self.__download_count = 0
        self.__factory = module_factory.CrawlerApiFactory()
        self.__lock = threading.Lock()
        self.__terminator = self.__factory.create_terminator()
        self.__limit_results_per_query = limit_results_per_query

    @classmethod
    @abc.abstractmethod
    def get_data_set_size(cls):
        pass

    @abc.abstractmethod
    def download_item(self, query, index):
        pass

    @abc.abstractmethod
    def download(self, query, is_to_download_id=True, is_to_download_content=True):
        pass

    @abc.abstractmethod
    def clean_up_data_folder(self):
        pass

    @abc.abstractmethod
    def download_entire_data_set(self):
        pass

    def inc_download(self):
        with self.__lock:
            self.download_count += 1


class AbsWebsiteCrawlerApi(AbsBaseCrawlerApi, metaclass=abc.ABCMeta):

    _NUMBER_ATTEMPTS_GET_EXPECTED_AMOUNT_OF_DATA = 5
    _DATA_FILE_EXTENSION = ".pkl"
    _PAGE_LOAD_TIMEOUT = 30
    _CRAWL_DELAY = 1
    _DOWNLOAD_TRY_NUMBER = 10000
    _OFFSET_MASK = "<<offset>>"
    _QUERY_MASK = "<<query>>"
    _HTML_PARSER = "html5lib"
    _JAVASCRIPT_GET_PAGE_SOURCE_CODE = "return document.getElementsByTagName('html')[0].innerHTML"

    @property
    @abc.abstractmethod
    def _limit_results(self):
        pass

    @property
    @abc.abstractmethod
    def thread_limit(self):
        pass

    @property
    @abc.abstractmethod
    def base_url(self):
        pass

    @property
    @abc.abstractmethod
    def max_results_per_page(self):
        pass

    @property
    @abc.abstractmethod
    def data_folder_path(self):
        pass

    @abc.abstractmethod
    def _extract_data_list_from_soup(self, soup):
        pass

    @abc.abstractmethod
    def _extract_number_matches_from_soup(self, soup):
        pass

    @abc.abstractmethod
    def _calculate_offset(self, offset):
        pass

    @abc.abstractmethod
    def _handle_inconsistent_page(self, page_data_list):
        pass

    @classmethod
    @abc.abstractmethod
    def _get_url_with_data_set_size(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def _extract_data_set_size(cls, soup):
        pass

    @abc.abstractmethod
    def __init__(self, limit_number_results):
        super().__init__(limit_number_results)
        self.clean_up_data_folder()

    @classmethod
    def _test_if_page_with_data_set_size_loaded(cls, web_driver):
        page_source = web_driver.execute_script(AbsWebsiteCrawlerApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
        soup = bs4.BeautifulSoup(page_source, AbsWebsiteCrawlerApi._HTML_PARSER)
        return cls._extract_data_set_size(soup) != -1

    @classmethod
    def get_data_set_size(cls):
        web_driver = selenium.webdriver.PhantomJS()
        web_driver.get(cls._get_url_with_data_set_size())
        wait = WebDriverWait(web_driver, AbsWebsiteCrawlerApi._PAGE_LOAD_TIMEOUT)
        wait.until(cls._test_if_page_with_data_set_size_loaded)
        page_source = web_driver.execute_script(AbsWebsiteCrawlerApi._JAVASCRIPT_GET_PAGE_SOURCE_CODE)
        soup = bs4.BeautifulSoup(page_source, AbsWebsiteCrawlerApi._HTML_PARSER)
        return cls._extract_data_set_size(soup)

    def download_entire_data_set(self):
        self._terminator.terminate("ERROR - INVALID OPERATION")

    def download_item(self, query, index):
        web_page = self._attempt_download(query, index)
        soup = bs4.BeautifulSoup(web_page, AbsWebsiteCrawlerApi._HTML_PARSER)
        number_matches = self._extract_number_matches_from_soup(soup)
        if number_matches > 0:
            if index >= number_matches:
                self._terminator.terminate("ERROR - INDEX OUT OF RANGE")
            data_list = self._extract_data_list_from_soup(soup)
            list_index = index % self.max_results_per_page
            if list_index >= len(data_list):
                return None
            data = data_list[list_index]
            search_result = self.factory.create_search_result(number_matches, [data])
        else:
            search_result = self.factory.create_search_result(number_matches, [])
        return search_result

    def download(self, query, is_to_download_id=True, is_to_download_content=True):
        file_path = self._build_file_path(query)
        search_result = self._download_based_on_stored_file(query, file_path)
        if search_result is None:
            search_result = self._download_completely_from_web(query, file_path)
        search_result = self._filter_result_content(search_result, is_to_download_id,
                                                    is_to_download_content)
        return search_result

    def clean_up_data_folder(self):
        for the_file in os.listdir(self.data_folder_path):
            file_path = os.path.join(self.data_folder_path, the_file)
            if ".gitignore" not in file_path:
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except:
                    pass

    def _download_more_results_if_needed(self, query, number_matches, data_list):
        number_downloaded_results = len(data_list)
        if number_downloaded_results > number_matches:
            return self.factory.create_search_result(number_matches, data_list)
        if self.limit_results_per_query < number_matches:
            number_additional_downloads = self._calculate_number_additional_downloads(self.limit_results_per_query,
                                                                                      number_downloaded_results)
        else:
            number_additional_downloads = self._calculate_number_additional_downloads(number_matches,
                                                                                      number_downloaded_results)
        if number_additional_downloads > 0:
            additional_data_list = self._do_additional_downloads(query, number_downloaded_results,
                                                                 number_additional_downloads, number_matches)
            data_list = list(itertools.chain(data_list, additional_data_list))
        data_list_size = len(data_list)
        if self.limit_results_per_query < number_matches and data_list_size > self.limit_results_per_query:
            if data_list_size - self.limit_results_per_query >= self.max_results_per_page:
                print("DOWNLOADED UNECESSARY PAGES, TOTAL OF " + str(data_list_size - self.limit_results_per_query) +
                      " MORE ITEMS")
            data_list = data_list[0:self.limit_results_per_query]
        search_result = self.factory.create_search_result(number_matches, data_list)
        return search_result

    def _download_based_on_stored_file(self, query, file_path):
        if not os.path.exists(file_path):
            return None
        search_result = self._get_saved_result(file_path)
        return search_result

    def _download_completely_from_web(self, query, file_path):
        web_page = self._attempt_download(query, 0)
        soup = bs4.BeautifulSoup(web_page, AbsWebsiteCrawlerApi._HTML_PARSER)
        number_matches = self._extract_number_matches_from_soup(soup)
        if number_matches == 0:
            search_result = self.factory.create_search_result(0, [])
            self._save_result(file_path, search_result)
            return search_result
        data_list = self._extract_data_list_from_soup(soup)
        if not self._is_expected_amount_of_data(data_list, number_matches, 0):
            data_list = self._download_until_expected_amount_of_data_is_extracted(query, number_matches, 0)
        search_result = self._download_more_results_if_needed(query, number_matches, data_list)
        number_results = len(search_result.results)
        if self.limit_results_per_query < number_matches:
            if number_results != self.limit_results_per_query:
                print("ERROR - NUMBER OF DATA ITEMS != LIMIT OF RESULTS =  " + query)
                print("ERROR IGNORED")
        else:
            if number_results != number_matches:
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
            soup = bs4.BeautifulSoup(web_page, AbsWebsiteCrawlerApi._HTML_PARSER)
            list_from_soup = self._extract_data_list_from_soup(soup)
            if self._is_expected_amount_of_data(list_from_soup, number_matches, number_downloaded_results):
                return list_from_soup
        print("INCONSISTENCY COULD NOT BE SOLVED")
        print("NUMBER OF ITEMS IN THE PAGE = " + str(len(list_from_soup)))
        print("NUMBER OF DOWNLOADED RESULTS = " + str(number_downloaded_results))
        print("NUMBER OF MATCHES = " + str(number_matches))
        print("NUMBER OF RESULTS PER PAGE = " + str(self.max_results_per_page))
        print("QUERY = " + str(query))
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
        soup = bs4.BeautifulSoup(page_source, AbsWebsiteCrawlerApi._HTML_PARSER)
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
                web_page = selenium.webdriver.PhantomJS()
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
            self._terminator.terminate("ERROR - INTERNET CONNECTION FAILURE")
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

    def _filter_result_content(self, search_result, is_to_have_id, is_to_have_content):
        if is_to_have_content and not is_to_have_id:
            data_list = [self.factory.create_data(None, x.content) for x in search_result.results]
        elif is_to_have_id and not is_to_have_content:
            data_list = [self.factory.create_data(x.identifier, None) for x in search_result.results]
        else:
            data_list = search_result.results
        return self.factory.create_search_result(search_result.number_results, data_list)


class AbsIEEECrawlerApi(AbsWebsiteCrawlerApi, metaclass=abc.ABCMeta):

    DEFAULT_LIMIT_RESULTS = 5000000
    _DATA_SET_SIZE_TAG = "a"
    _DATA_SET_SIZE_TAG_ATTRIBUTE = "href"
    _DATA_SET_SIZE_TAG_ATTRIBUTE_VALUE = "/search/searchresult.jsp?sortType=desc_p_Publication_Year&newsearch=true"
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
    _DATA_FOLDER_PATH = "AbsIEEECrawlerApi__DATA_FOLDER_PATH"

    def __init__(self, limit_number_results=None):
        if limit_number_results is None:
            limit_number_results = AbsIEEECrawlerApi.DEFAULT_LIMIT_RESULTS
        super().__init__(limit_number_results)

    @property
    @abc.abstractmethod
    def base_url(self):
        pass

    @property
    def _limit_results(self):
        return AbsIEEECrawlerApi.DEFAULT_LIMIT_RESULTS

    @property
    def thread_limit(self):
        return AbsIEEECrawlerApi._THREAD_LIMIT

    @property
    def max_results_per_page(self):
        return AbsIEEECrawlerApi._MAX_RESULTS_PER_PAGE

    @property
    def data_folder_path(self):
        path_dictionary = self.factory.create_path_dictionary()
        return path_dictionary.get_path(AbsIEEECrawlerApi._DATA_FOLDER_PATH)

    @classmethod
    def _get_url_with_data_set_size(cls):
        return AbsIEEECrawlerApi._WEB_DOMAIN

    @classmethod
    def _extract_data_set_size(cls, soup):
        dictionary = {AbsIEEECrawlerApi._DATA_SET_SIZE_TAG_ATTRIBUTE:
                      AbsIEEECrawlerApi._DATA_SET_SIZE_TAG_ATTRIBUTE_VALUE}
        soup = soup.find(AbsIEEECrawlerApi._DATA_SET_SIZE_TAG, dictionary)
        if soup is None:
            return -1
        data_set_size = int(str(soup.next).replace(".", ""))
        return data_set_size

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
                self._terminator.terminate("ERROR - Data extraction failure - " + str(item))

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
            return str(title) + "\n" + "\n" + str(abstract)
        else:
            return str(title)


class AbsACMCrawlerApi(AbsWebsiteCrawlerApi, metaclass=abc.ABCMeta):

    DEFAULT_LIMIT_RESULTS = 5000000
    _URL_WITH_DATA_SET_SIZE = "http://dl.acm.org/results.cfm?h=1&query=test&dlr=GUIDE"
    _THREAD_LIMIT = 1
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "b"
    _DATA_FOLDER_PATH = "AbsACMCrawlerApi__DATA_FOLDER_PATH"
    _MAX_RESULTS_PER_PAGE = 20
    _WEB_DOMAIN = "http://dl.acm.org/"
    _DATA_SET_SIZE_TAG_PARENT = "span"
    _DATA_SET_SIZE_TAG_PARENT_ATTRIBUTE = "class"
    _DATA_SET_SIZE_TAG_PARENT_ATTRIBUTE_VALUE = "text10"
    _DATA_SET_SIZE_TAG = "strong"
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

    def __init__(self, limit_number_results=None):
        if limit_number_results is None:
            limit_number_results = AbsACMCrawlerApi.DEFAULT_LIMIT_RESULTS
        super().__init__(limit_number_results)

    @property
    def _limit_results(self):
        return AbsACMCrawlerApi.DEFAULT_LIMIT_RESULTS

    @property
    def thread_limit(self):
        return AbsACMCrawlerApi._THREAD_LIMIT

    @property
    def max_results_per_page(self):
        return AbsACMCrawlerApi._MAX_RESULTS_PER_PAGE

    @property
    def data_folder_path(self):
        path_dictionary = self.factory.create_path_dictionary()
        return path_dictionary.get_path(AbsACMCrawlerApi._DATA_FOLDER_PATH)

    @property
    @abc.abstractmethod
    def base_url(self):
        pass

    @classmethod
    def _get_url_with_data_set_size(cls):
        return AbsACMCrawlerApi._URL_WITH_DATA_SET_SIZE

    @classmethod
    def _extract_data_set_size(cls, soup):
        dictionary = {AbsACMCrawlerApi._DATA_SET_SIZE_TAG_PARENT_ATTRIBUTE:
                      AbsACMCrawlerApi._DATA_SET_SIZE_TAG_PARENT_ATTRIBUTE_VALUE}
        soup = soup.find_all(AbsACMCrawlerApi._DATA_SET_SIZE_TAG_PARENT, dictionary)
        if soup is None or len(soup) < 2:
            return -1
        soup = soup[1].find(AbsACMCrawlerApi._DATA_SET_SIZE_TAG)
        if soup is None:
            return -1
        data_set_size = int(str(soup.next).replace(",", ""))
        return data_set_size

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
            content = str(title) + "\n" + str(abstract_tag.text)
        else:
            content = str(title)
        data = self.factory.create_data(identifier, content)
        return data


class SolrCrawlerApi(AbsBaseCrawlerApi):

    DEFAULT_LIMIT_RESULTS = 5000000
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

    def __init__(self, limit_number_results=None):
        if limit_number_results is None:
            limit_number_results = SolrCrawlerApi.DEFAULT_LIMIT_RESULTS
        super().__init__(limit_number_results)

    def clean_up_data_folder(self):
        pass

    @classmethod
    def get_data_set_size(cls):
        url = SolrCrawlerApi._URL.replace(SolrCrawlerApi._LIMIT_MASK, str(1))
        url = url.replace(SolrCrawlerApi._QUERY_MASK, str("*"))
        url = url.replace(SolrCrawlerApi._FIELD_TO_SEARCH_MASK, "*")
        url = url.replace(SolrCrawlerApi._FIELDS_TO_RETURN_MASK, SolrCrawlerApi._ID_FIELD)
        url = url.replace(SolrCrawlerApi._OFFSET_MASK, str(0))
        response = urllib.request.urlopen(url)
        data = response.read().decode(SolrCrawlerApi._ENCODING)
        dictionary = json.loads(data)
        data_set_size = int(dictionary[SolrCrawlerApi._RESPONSE_KEY][SolrCrawlerApi._NUMBER_MATCHES_KEY])
        return data_set_size

    def download_item(self, query, index):
        return self._download(query, True, True, index, 1, SolrCrawlerApi._FIELD_TO_SEARCH)

    def download_entire_data_set(self):
        return self._download("*", True, True, 0, 1000000, "*")

    def download(self, query, is_to_download_id=True, is_to_download_content=True):
        result = self._download(query, is_to_download_id, is_to_download_content, 0,
                                self.limit_results_per_query, SolrCrawlerApi._FIELD_TO_SEARCH)
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
        response = urllib.request.urlopen(str(url))
        self.inc_download()
        data = response.read().decode(SolrCrawlerApi._ENCODING)
        dictionary = json.loads(data)
        dictionary = dictionary[SolrCrawlerApi._RESPONSE_KEY]
        result_list = [
            self.factory.create_data(x.get(SolrCrawlerApi._ID_FIELD, None),
                                     x.get(SolrCrawlerApi._FIELD_TO_SEARCH, None))
            for x in dictionary[SolrCrawlerApi._DOCUMENT_LIST_KEY]]
        search_result = self.factory.create_search_result(int(dictionary[SolrCrawlerApi._NUMBER_MATCHES_KEY]),
                                                          result_list)
        return search_result


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
                 + "action=search&sortType=&searchField=Search_All&matchBoolean=true&"
                 + "queryText=(\"Document%20Title\":<<query>>)&"
                 + "rowsPerPage=100&pageNumber=<<offset>>&resultAction=ROWS_PER_PAGE")

    def __init__(self):
        super().__init__()

    @property
    def base_url(self):
        return IEEEOnlyTitleCrawlerApi._BASE_URL


class IEEEOnlyAbstractCrawlerApi(AbsIEEECrawlerApi):

    _BASE_URL = ("http://ieeexplore.ieee.org/search/searchresult.jsp?"
                 + "action=search&sortType=&searchField=Search_All&matchBoolean=true&"
                 + "queryText=(\"Abstract\":<<query>>)&"
                 + "rowsPerPage=100&pageNumber=<<offset>>&resultAction=ROWS_PER_PAGE")

    def __init__(self):
        super().__init__()

    @property
    def base_url(self):
        return IEEEOnlyAbstractCrawlerApi._BASE_URL


class ACMCrawlerApi(AbsACMCrawlerApi):

    _BASE_URL = "http://dl.acm.org/results.cfm?query=<<query>>&start=<<offset>>1&dlr=ACM"

    @property
    def base_url(self):
        return ACMCrawlerApi._BASE_URL


class ACMOnlyTitleCrawlerApi(AbsACMCrawlerApi):

    _BASE_URL = ("http://dl.acm.org/results.cfm?query=%28Title%3A<<query>>%29&"
                 + "querydisp=%28Title%3A<<query>>%29&source_query=Owner%3AACM&"
                 + "start=<<offset>>1&srt=score%20dsc&short=0&source_disp=&since_month=&"
                 + "since_year=&before_month=&before_year=&coll=DL&dl=ACM&termshow=matchboolean&"
                 + "range_query=&zadv=1")

    @property
    def base_url(self):
        return ACMOnlyTitleCrawlerApi._BASE_URL


class ACMOnlyAbstractCrawlerApi(AbsACMCrawlerApi):

    _BASE_URL = ("http://dl.acm.org/results.cfm?query=%28Abstract%3A<<query>>%29&"
                 + "querydisp=%28Abstract%3A<<query>>%29&source_query=Owner%3AACM&"
                 + "start=<<offset>>1&srt=score%20dsc&short=0&source_disp=&since_month=&"
                 + "since_year=&before_month=&before_year=&coll=DL&dl=ACM&termshow=matchboolean&"
                 + "range_query=&zadv=1")

    @property
    def base_url(self):
        return ACMOnlyAbstractCrawlerApi._BASE_URL