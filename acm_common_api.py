import os
from abs_website_common_api import AbsWebsiteCommonApi


class ACMCommonApi(AbsWebsiteCommonApi):
    DATA_SET_SIZE = 445543
    _THREAD_LIMIT = 1
    QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "b"
    _NO_RESULTS_TAG = "font"
    _NO_RESULTS_TAG_ATTRIBUTE_VALUE = "+1"
    _NO_RESULTS_TAG_ATTRIBUTE = "size"
    _BASE_URL = "http://dl.acm.org/results.cfm?query=<<query>>&start=<<offset>>1&dlr=ACM"
    _DATA_FOLDER_PATH = "/media/fabio/FABIO/acm"
    _MAX_RESULTS_PER_PAGE = 20
    _WEB_DOMAIN = "http://dl.acm.org/"
    _TITLE_TAG_ID_ATTRIBUTE = "href"
    _TITLE_TAG = "a"
    _TITLE_TAG_ATTRIBUTE_VALUE = "medium-text"
    _TITLE_TAG_ATTRIBUTE = "class"

    @property
    def thread_limit(self):
        return ACMCommonApi._THREAD_LIMIT

    @property
    def query_pool_file_path(self):
        return ACMCommonApi.QUERY_POOL_FILE_PATH

    @property
    def max_results_per_page(self):
        return ACMCommonApi._MAX_RESULTS_PER_PAGE

    @property
    def data_folder_path(self):
        return ACMCommonApi._DATA_FOLDER_PATH

    @property
    def base_url(self):
        return ACMCommonApi._BASE_URL

    def _calculate_real_offset(self, offset):
        return 2 * offset / self.max_results_per_page

    def _extract_data_list_from_soup(self, soup):
        dictionary = {ACMCommonApi._TITLE_TAG_ATTRIBUTE: ACMCommonApi._TITLE_TAG_ATTRIBUTE_VALUE}
        title_tag_list = soup.find_all(ACMCommonApi._TITLE_TAG, dictionary)
        abstract_list = [x.parent.parent.parent.find("div", {"class": "abstract2"}) for x in title_tag_list]
        data_list = [self._create_data(x[ACMCommonApi._TITLE_TAG_ID_ATTRIBUTE], x.text, y.text)
                     for x, y in zip(title_tag_list, abstract_list)]
        return data_list

    def _extract_number_matches_from_soup(self, soup):
        dictionary = {ACMCommonApi._NO_RESULTS_TAG_ATTRIBUTE: ACMCommonApi._NO_RESULTS_TAG_ATTRIBUTE_VALUE}
        no_results_element = soup.find(ACMCommonApi._NO_RESULTS_TAG, dictionary)
        if no_results_element is not None:
            return 0
        html_element = soup.find(ACMCommonApi._ELEMENT_WITH_NUMBER_MATCHES_TAG)
        if html_element is not None:
            try:
                number_matches = int(str(html_element.text.replace(",", "")))
            except:
                return -1
        else:
            return -1
        return number_matches

    def _create_data(self, href, text, abstract):
        identifier = self._format_data_id(str(href))
        content = self._format_data_content(text, abstract)
        data = self.factory.create_data(identifier, content)
        return data

    def _format_data_id(self, href):
        href = str(href[0:href.find("&")])
        return ACMCommonApi._WEB_DOMAIN + href

    def _format_data_content(self, text, abstract):
        if abstract is not None:
            return str(text) + os.linesep + str(abstract)
        else:
            return str(text)
