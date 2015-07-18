from urllib.request import urlopen
import json

from abs_base_common_api import AbsBaseCommonApi
from config import Config


class SolrCommonApi(AbsBaseCommonApi):
    _URL = ("http://localhost:8984/solr/newsgroups2/select?"
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

    def __init__(self):
        super().__init__()

    def download_entire_data_set(self):
        return self._download("*", True, True, 0, 1000000, "*")

    def download(self, query, is_to_download_id=True, is_to_download_content=True,
                 offset=0, limit=Config.SEARCH_ENGINE_LIMIT):
        return self._download(query, is_to_download_id, is_to_download_content, offset, limit,
                              SolrCommonApi._FIELD_TO_SEARCH)

    def _download(self, query, is_to_download_id, is_to_download_content, offset, limit, field_to_search):
        url = SolrCommonApi._URL.replace(SolrCommonApi._LIMIT_MASK, str(limit))
        url = url.replace(SolrCommonApi._QUERY_MASK, str(query))
        url = url.replace(SolrCommonApi._FIELD_TO_SEARCH_MASK, field_to_search)
        url = url.replace(SolrCommonApi._OFFSET_MASK, str(offset))
        if is_to_download_id and is_to_download_content:
            url = url.replace(SolrCommonApi._FIELDS_TO_RETURN_MASK,
                              SolrCommonApi._ID_FIELD + "," + SolrCommonApi._FIELD_TO_SEARCH)
        elif is_to_download_content and not is_to_download_id:
            url = url.replace(SolrCommonApi._FIELDS_TO_RETURN_MASK, SolrCommonApi._FIELD_TO_SEARCH)
        else:
            url = url.replace(SolrCommonApi._FIELDS_TO_RETURN_MASK, SolrCommonApi._ID_FIELD)
        response = urlopen(str(url))
        self.inc_download()
        data = response.read().decode(SolrCommonApi._ENCODING)
        dictionary = json.loads(data)
        dictionary = dictionary[SolrCommonApi._RESPONSE_KEY]
        result_list = [
            self.factory.create_data(x.get(SolrCommonApi._ID_FIELD, None), x.get(SolrCommonApi._FIELD_TO_SEARCH, None))
            for x
            in dictionary[SolrCommonApi._DOCUMENT_LIST_KEY]]
        search_result = self.factory.create_search_result(int(dictionary[SolrCommonApi._NUMBER_MATCHES_KEY]),
                                                          result_list)
        return search_result
