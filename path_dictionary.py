import abc


class AbsPathDictionary(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_path(self, key):
        pass


class WindowsPathDictionary(AbsPathDictionary):

    _PATH_DICTIONARY = {
        "AbsIEEECrawlerApi__DATA_FOLDER_PATH":
            "Data\\ieee",
        "AbsACMCrawlerApi__DATA_FOLDER_PATH":
            "Data\\acm",
        "Mhr__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "RandomWalk__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "SumEst__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "BroderEtAl__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists\\new_shine.txt",
        "SolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\Solr\\ExperimentResults.csv",
        "SolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\Solr\\Log.txt",
        "IEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\IEEE\\ExperimentResults.csv",
        "IEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\IEEE\\Log.txt",
        "IEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\IEEEOnlyTitle\\ExperimentResults.csv",
        "IEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\IEEEOnlyTitle\\Log.txt",
        "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\IEEEOnlyAbstract\\ExperimentResults.csv",
        "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\IEEEOnlyAbstract\\Log.txt",
        "ACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\ACM\\ExperimentResults.csv",
        "ACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\ACM\\Log.txt",
        "ACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\ACMOnlyTitle\\ExperimentResults.csv",
        "ACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\ACMOnlyTitle\\Log.txt",
        "ACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\ACMOnlyAbstract\\ExperimentResults.csv",
        "ACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
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
        "Mhr__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "RandomWalk__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "SumEst__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "BroderEtAl__DEFAULT_QUERY_POOL_FILE_PATH":
            "WordLists/new_shine.txt",
        "SolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/Solr/ExperimentResults.csv",
        "SolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/Solr/Log.txt",
        "IEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/IEEE/ExperimentResults.csv",
        "IEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/IEEE/Log.txt",
        "IEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/IEEEOnlyTitle/ExperimentResults.csv",
        "IEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/IEEEOnlyTitle/Log.txt",
        "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/IEEEOnlyAbstract/ExperimentResults.csv",
        "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/IEEEOnlyAbstract/Log.txt",
        "ACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/ACM/ExperimentResults.csv",
        "ACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/ACM/Log.txt",
        "ACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/ACMOnlyTitle/ExperimentResults.csv",
        "ACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/ACMOnlyTitle/Log.txt",
        "ACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs/ACMOnlyAbstract/ExperimentResults.csv",
        "ACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs/ACMOnlyAbstract/Log.txt",
    }

    def get_path(self, key):
        return LinuxPathDictionary._PATH_DICTIONARY[key]

