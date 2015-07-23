import os
import signal

from abs_website_common_api import AbsWebsiteCommonApi


class IEEEAbstractCommonApi(AbsWebsiteCommonApi):
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
    _DOWNLOAD_TRY_NUMBER = 5
    _BASE_URL = ("http://ieeexplore.ieee.org/search/searchresult.jsp?"
                 + "queryText=<<query>>&rowsPerPage=100&pageNumber=<<offset>>&resultAction=ROWS_PER_PAGE")
    _DATA_FOLDER_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs"

    def __init__(self):
        super().__init__()

    @property
    def max_results_per_page(self):
        return IEEEAbstractCommonApi._MAX_RESULTS_PER_PAGE

    @property
    def base_url(self):
        return IEEEAbstractCommonApi._BASE_URL

    @property
    def data_folder_path(self):
        return IEEEAbstractCommonApi._DATA_FOLDER_PATH

    def _extract_number_matches_from_soup(self, soup):
        dictionary = {IEEEAbstractCommonApi._NO_RESULTS_TAG_ATTRIBUTE: IEEEAbstractCommonApi._NO_RESULTS_TAG_ATTRIBUTE_VALUE}
        no_results_element = soup.find(IEEEAbstractCommonApi._NO_RESULTS_TAG, dictionary)
        if no_results_element is not None:
            return 0
        dictionary = {IEEEAbstractCommonApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE:
                      IEEEAbstractCommonApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_ATTRIBUTE_VALUE}
        one_result_element = soup.find(IEEEAbstractCommonApi._ELEMENT_WITH_NUMBER_MATCHES_WHEN_ONE_RESULT_TAG, dictionary)
        if one_result_element is not None:
            return 1
        dictionary = {IEEEAbstractCommonApi._ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE:
                      IEEEAbstractCommonApi._ELEMENT_WITH_NUMBER_MATCHES_ATTRIBUTE_VALUE}
        html_element = soup.find(IEEEAbstractCommonApi._ELEMENT_WITH_NUMBER_MATCHES_TAG, dictionary)
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
        dictionary = {IEEEAbstractCommonApi._ITEM_TAG_ATTRIBUTE: IEEEAbstractCommonApi._ITEM_TAG_ATTRIBUTE_VALUE}
        item_tag_list = soup.find_all(IEEEAbstractCommonApi._ITEM_TAG, dictionary)

        def extract_data(item):
            dictio = {IEEEAbstractCommonApi._ID_TAG_ATTRIBUTE: IEEEAbstractCommonApi._ID_TAG_ATTRIBUTE_VALUE}
            identifier_tag = item.find(IEEEAbstractCommonApi._ID_TAG, dictio)
            dictio = {IEEEAbstractCommonApi._TITLE_TAG_ATTRIBUTE: IEEEAbstractCommonApi._TITLE_TAG_ATTRIBUTE_VALUE}
            title_tag = item.find(IEEEAbstractCommonApi._TITLE_TAG, dictio)
            dictio = {IEEEAbstractCommonApi._ABSTRACT_TAG_ATTRIBUTE:
                      IEEEAbstractCommonApi._ABSTRACT_TAG_ATTRIBUTE_VALUE}
            abstract_tag = item.find(IEEEAbstractCommonApi._ABSTRACT_TAG, dictio)
            if identifier_tag is None or title_tag is None:
                print("ERROR - Data extraction failure")
                os.kill(os.getpid(), signal.SIGUSR1)
                return
            if abstract_tag is not None:
                data = self._create_data(identifier_tag[IEEEAbstractCommonApi._HREF], title_tag.text, abstract_tag.text)
            else:
                data = self._create_data(identifier_tag[IEEEAbstractCommonApi._HREF], title_tag.text)
            return data

        data_list = [extract_data(x) for x in item_tag_list]
        return data_list

    def _create_data(self, href, title, abstract=None):
        identifier = self._format_data_id(str(href))
        content = self._format_data_content(title, abstract)
        data = self.factory.create_data(identifier, content)
        return data

    def _format_data_id(self, href):
        return IEEEAbstractCommonApi._WEB_DOMAIN + href

    def _format_data_content(self, title, abstract):
        if abstract is not None:
            return str(title) + os.linesep + os.linesep + str(abstract)
        else:
            return str(title)
