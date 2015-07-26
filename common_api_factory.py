from data import Data
from abs_common_api_factory import AbsCommonApiFactory
from search_result import SearchResult


class CommonApiFactory(AbsCommonApiFactory):

    def create_search_result(self, number_results, results):
        return SearchResult(number_results, results)

    def create_data(self, identifier, content):
        return Data(identifier, content)
