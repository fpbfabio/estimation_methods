from abs_search_result import AbsSearchResult


class SearchResult(AbsSearchResult):

    def __init__(self, number_results, results):
        self.__number_results = number_results
        self.__results = results

    @property
    def number_results(self):
        return self.__number_results

    @property
    def results(self):
        return self.__results
