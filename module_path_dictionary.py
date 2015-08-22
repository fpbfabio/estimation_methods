import abc
import re


class AbsPathDictionary(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_path(self, key):
        pass


class WindowsPathDictionary(AbsPathDictionary):
    _RESULTS_FILE_PATH_REGEX = re.compile("([a-zA-z]+)ExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH")
    _DETAILS_FILE_PATH_REGEX = re.compile("([a-zA-z]+)ExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH")
    _PATH_DICTIONARY = {
        "AbsBaseEstimator__DEFAULT_QUERY_POOL_FILE_PATH": "WordLists\\new_shine.txt",
        "AbsSolrExecutor__QUERY_POOL_PATH_LIST": ["WordLists\\new_shine.txt",
                                                  "WordLists\\new_shine.txt",
                                                  "WordLists\\new_shine.txt",
                                                  "WordLists\\new_shine.txt",
                                                  "WordLists\\new_shine.txt",
                                                  "WordLists\\new_shine.txt"],
        "AbsSolrExecutor__CORE_PATH_LIST": ["Cores\\newsgroups",
                                            "Cores\\dbcomp_abstract_core",
                                            "Cores\\dbcomp_title_core",
                                            "Cores\\dbcomp_en",
                                            "Cores\\dblp",
                                            "Cores\\artigos0313_en"],
        "AbsSolrExecutor__CREATE_CORE_COMMAND": "Commands\\CreateCore.bat experiment ",
        "AbsSolrExecutor__UNLOAD_CORE_COMMAND": "Commands\\UnloadCore.bat experiment ",
        "AbsSolrExecutor__START_SOLR_COMMAND": "Commands\\StartSolr.bat experiment ",
        "AbsSolrExecutor__STOP_SOLR_COMMAND": "Commands\\StopSolr.bat experiment ",
        "AbsACMCrawlerApi__DATA_FOLDER_PATH": "Data\\acm",
        "AbsIEEECrawlerApi__DATA_FOLDER_PATH": "Data\\ieee"
    }

    def get_path(self, key):
        regex_search_result = type(self)._RESULTS_FILE_PATH_REGEX.match(key)
        if regex_search_result is not None:
            return "Logs\\" + regex_search_result.group(1) + "\\ExperimentResults.csv"
        regex_search_result = type(self)._DETAILS_FILE_PATH_REGEX.match(key)
        if regex_search_result is not None:
            return "Logs\\" + regex_search_result.group(1) + "\\Log.txt"
        return WindowsPathDictionary._PATH_DICTIONARY[key]
