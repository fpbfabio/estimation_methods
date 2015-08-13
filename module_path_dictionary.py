import abc


class AbsPathDictionary(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_path(self, key):
        pass


class WindowsPathDictionary(AbsPathDictionary):
    _PATH_DICTIONARY = {
        "MhrSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrSolr\\ExperimentResults.csv",
        "MhrSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrSolr\\Log.txt",
        "MhrIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrIEEE\\ExperimentResults.csv",
        "MhrIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrIEEE\\Log.txt",
        "MhrIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrIEEEOnlyTitle\\ExperimentResults.csv",
        "MhrIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrIEEEOnlyTitle\\Log.txt",
        "MhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrIEEEOnlyAbstract\\ExperimentResults.csv",
        "MhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrIEEEOnlyAbstract\\Log.txt",
        "MhrACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrACM\\ExperimentResults.csv",
        "MhrACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrACM\\Log.txt",
        "MhrACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrACMOnlyTitle\\ExperimentResults.csv",
        "MhrACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrACMOnlyTitle\\Log.txt",
        "MhrACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\MhrACMOnlyAbstract\\ExperimentResults.csv",
        "MhrACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\MhrACMOnlyAbstract\\Log.txt",
        "SumEstSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstSolr\\ExperimentResults.csv",
        "SumEstSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstSolr\\Log.txt",
        "SumEstIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstIEEE\\ExperimentResults.csv",
        "SumEstIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstIEEE\\Log.txt",
        "SumEstIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstIEEEOnlyTitle\\ExperimentResults.csv",
        "SumEstIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstIEEEOnlyTitle\\Log.txt",
        "SumEstIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstIEEEOnlyAbstract\\ExperimentResults.csv",
        "SumEstIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstIEEEOnlyAbstract\\Log.txt",
        "SumEstACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstACM\\ExperimentResults.csv",
        "SumEstACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstACM\\Log.txt",
        "SumEstACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstACMOnlyTitle\\ExperimentResults.csv",
        "SumEstACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstACMOnlyTitle\\Log.txt",
        "SumEstACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\SumEstACMOnlyAbstract\\ExperimentResults.csv",
        "SumEstACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\SumEstACMOnlyAbstract\\Log.txt",
        "RandomWalkSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkSolr\\ExperimentResults.csv",
        "RandomWalkSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkSolr\\Log.txt",
        "RandomWalkIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkIEEE\\ExperimentResults.csv",
        "RandomWalkIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkIEEE\\Log.txt",
        "RandomWalkIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkIEEEOnlyTitle\\ExperimentResults.csv",
        "RandomWalkIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkIEEEOnlyTitle\\Log.txt",
        "RandomWalkIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkIEEEOnlyAbstract\\ExperimentResults.csv",
        "RandomWalkIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkIEEEOnlyAbstract\\Log.txt",
        "RandomWalkACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkACM\\ExperimentResults.csv",
        "RandomWalkACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkACM\\Log.txt",
        "RandomWalkACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkACMOnlyTitle\\ExperimentResults.csv",
        "RandomWalkACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkACMOnlyTitle\\Log.txt",
        "RandomWalkACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\RandomWalkACMOnlyAbstract\\ExperimentResults.csv",
        "RandomWalkACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\RandomWalkACMOnlyAbstract\\Log.txt",
        "BroderEtAlSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlSolr\\ExperimentResults.csv",
        "BroderEtAlSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlSolr\\Log.txt",
        "BroderEtAlIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlIEEE\\ExperimentResults.csv",
        "BroderEtAlIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlIEEE\\Log.txt",
        "BroderEtAlIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlIEEEOnlyTitle\\ExperimentResults.csv",
        "BroderEtAlIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlIEEEOnlyTitle\\Log.txt",
        "BroderEtAlIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlIEEEOnlyAbstract\\ExperimentResults.csv",
        "BroderEtAlIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlIEEEOnlyAbstract\\Log.txt",
        "BroderEtAlACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlACM\\ExperimentResults.csv",
        "BroderEtAlACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlACM\\Log.txt",
        "BroderEtAlACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlACMOnlyTitle\\ExperimentResults.csv",
        "BroderEtAlACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlACMOnlyTitle\\Log.txt",
        "BroderEtAlACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH":
            "Logs\\BroderEtAlACMOnlyAbstract\\ExperimentResults.csv",
        "BroderEtAlACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH":
            "Logs\\BroderEtAlACMOnlyAbstract\\Log.txt",
        "Mhr__DEFAULT_QUERY_POOL_FILE_PATH": "WordLists\\new_shine.txt",
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
        return WindowsPathDictionary._PATH_DICTIONARY[key]
