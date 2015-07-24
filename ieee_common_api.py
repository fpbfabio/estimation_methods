import os
import signal

from abs_website_common_api import AbsWebsiteCommonApi


class IEEECommonApi(AbsWebsiteCommonApi):
    _WEB_DOMAIN = "http://ieeexplore.ieee.org"
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
    _MAX_RESULTS_PER_PAGE = 100
    _ELEMENT_WITH_NUMBER_MATCHES_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE = "class"
    _ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE_VALUE = "ng-binding ng-scope"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_TAG = "span"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE = "ng-if"
    _ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE_VALUE = "records.length === 1"
    _DOWNLOAD_TRY_NUMBER = 5
    _BASE_URL = ("http://ieeexplore.ieee.org/search/searchresult.jsp?"
                 + "queryText=<<query>>&rowsPerPage=100&pageNumber=<<offset>>&resultAction=ROWS_PER_PAGE")
    _DATA_FOLDER_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs"

    def __init__(self):
        super().__init__()

    @property
    def max_results_per_page(self):
        return IEEECommonApi._MAX_RESULTS_PER_PAGE

    @property
    def base_url(self):
        return IEEECommonApi._BASE_URL

    @property
    def data_folder_path(self):
        return IEEECommonApi._DATA_FOLDER_PATH

    def _calculate_real_offset(self, offset):
        return (offset + self.max_results_per_page) / self.max_results_per_page

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
        html_element = soup.find(IEEECommonApi._ELEMENT_WITH_NUMBER_MATCHES_TAG, dictionary)
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
