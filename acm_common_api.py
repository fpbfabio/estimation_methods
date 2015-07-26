import os
from abs_website_common_api import AbsWebsiteCommonApi


class ACMCommonApi(AbsWebsiteCommonApi):
    DATA_SET_SIZE = 445543
    QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    _THREAD_LIMIT = 1
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "b"
    _BASE_URL = "http://dl.acm.org/results.cfm?query=<<query>>&start=<<offset>>1&dlr=ACM"
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
        dictionary = {ACMCommonApi._ABSTRACT_TAG_ATTRIBUTE: ACMCommonApi._ABSTRACT_TAG_ATTRIBUTE_VALUE}
        abstract_list = [x.parent.parent.parent.find(ACMCommonApi._ABSTRACT_TAG, dictionary) for x in title_tag_list]
        data_list = [self._create_data(x[ACMCommonApi._TITLE_TAG_ID_ATTRIBUTE], x.text, y)
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

    def _create_data(self, href, title, abstract_tag):
        identifier = ACMCommonApi._WEB_DOMAIN + href[0:href.find("&")]
        if abstract_tag is not None:
            content = str(title) + os.linesep + str(abstract_tag.text)
        else:
            content = str(title)
        data = self.factory.create_data(identifier, content)
        return data
