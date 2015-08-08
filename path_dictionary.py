from abc import ABCMeta, abstractmethod


class AbsPathDictionary(metaclass=ABCMeta):

    @abstractmethod
    def get_path(self, key):
        pass


class WindowsPathDictionary(AbsPathDictionary):

    _PATH_DICTIONARY = {
        "AbsIEEECrawlerApi__DATA_FOLDER_PATH":
            "Data\\ieee",
        "AbsACMCrawlerApi__DATA_FOLDER_PATH":
            "Data\\acm",
        "Mhr___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "RandomWalk___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "SumEst___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "BroderEtAl___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "SolrExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\Solr\\ExperimentResults.csv",
        "SolrExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\Solr\\Log.txt",
        "IEEEExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\IEEE\\ExperimentResults.csv",
        "IEEEExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\IEEE\\Log.txt",
        "IEEEOnlyTitleExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\IEEEOnlyTitle\\ExperimentResults.csv",
        "IEEEOnlyTitleExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\IEEEOnlyTitle\\Log.txt",
        "IEEEOnlyAbstractExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\IEEEOnlyAbstract\\ExperimentResults.csv",
        "IEEEOnlyAbstractExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\IEEEOnlyAbstract\\Log.txt",
        "ACMExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\ACM\\ExperimentResults.csv",
        "ACMExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\ACM\\Log.txt",
        "ACMOnlyTitleExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\ACMOnlyTitle\\ExperimentResults.csv",
        "ACMOnlyTitleExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\ACMOnlyTitle\\Log.txt",
        "ACMOnlyAbstractExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\ACMOnlyAbstract\\ExperimentResults.csv",
        "ACMOnlyAbstractExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\ACMOnlyAbstract\\Log.txt",
    }

    def get_path(self, key):
        return WindowsPathDictionary._PATH_DICTIONARY[key]


class LinuxPathDictionary(AbsPathDictionary):

    _PATH_DICTIONARY = {
        "AbsIEEECrawlerApi__DATA_FOLDER_PATH":
            "Data/ieee",
        "AbsACMCrawlerApi__DATA_FOLDER_PATH":
            "Data/acm",
        "Mhr___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "RandomWalk___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "SumEst___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "BroderEtAl___DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "SolrExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/Solr/ExperimentResults.csv",
        "SolrExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/Solr/Log.txt",
        "IEEEExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/IEEE/ExperimentResults.csv",
        "IEEEExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/IEEE/Log.txt",
        "IEEEOnlyTitleExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/IEEEOnlyTitle/ExperimentResults.csv",
        "IEEEOnlyTitleExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/IEEEOnlyTitle/Log.txt",
        "IEEEOnlyAbstractExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/IEEEOnlyAbstract/ExperimentResults.csv",
        "IEEEOnlyAbstractExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/IEEEOnlyAbstract/Log.txt",
        "ACMExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/ACM/ExperimentResults.csv",
        "ACMExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/ACM/Log.txt",
        "ACMOnlyTitleExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/ACMOnlyTitle/ExperimentResults.csv",
        "ACMOnlyTitleExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/ACMOnlyTitle/Log.txt",
        "ACMOnlyAbstractExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/ACMOnlyAbstract/ExperimentResults.csv",
        "ACMOnlyAbstractExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/ACMOnlyAbstract/Log.txt",
    }

    def get_path(self, key):
        return LinuxPathDictionary._PATH_DICTIONARY[key]

