from abc import ABCMeta, abstractmethod


class AbsPathDictionary(metaclass=ABCMeta):

    @abstractmethod
    def get_path(self, key):
        pass


class WindowsPathDictionary(AbsPathDictionary):

    _PATH_DICTIONARY = {
        "AbsIEEECrawlerApi__DATA_FOLDER_PATH":
            "E:\\ieee",
        "AbsACMCrawlerApi__DATA_FOLDER_PATH":
            "E:\\acm",
        "Mhr___DEFAULT_QUERY_POOL_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ArquivosSolr\\ListaPalavras\\new_shine.txt",
        "RandomWalk___DEFAULT_QUERY_POOL_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ArquivosSolr\\ListaPalavras\\new_shine.txt",
        "SumEst___DEFAULT_QUERY_POOL_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ArquivosSolr\\ListaPalavras\\new_shine.txt",
        "BroderEtAl___DEFAULT_QUERY_POOL_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ArquivosSolr\\ListaPalavras\\new_shine.txt",
        "SolrExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\Solr\\ExperimentResults.csv",
        "SolrExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\Solr\\Log.txt",
        "IEEEExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\IEEE\\ExperimentResults.csv",
        "IEEEExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\IEEE\\Log.txt",
        "IEEEOnlyTitleExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\IEEEOnlyTitle\\ExperimentResults.csv",
        "IEEEOnlyTitleExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\IEEEOnlyTitle\\Log.txt",
        "IEEEOnlyAbstractExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\IEEEOnlyAbstract\\" +
            "ExperimentResults.csv",
        "IEEEOnlyAbstractExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\IEEEOnlyAbstract\\Log.txt",
        "ACMExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\ACM\\ExperimentResults.csv",
        "ACMExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\ACM\\Log.txt",
        "ACMOnlyTitleExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\ACMOnlyTitle\\ExperimentResults.csv",
        "ACMOnlyTitleExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\ACMOnlyTitle\\Log.txt",
        "ACMOnlyAbstractExecutorFactory___EXPERIMENT_RESULTS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\ACMOnlyAbstract\\ExperimentResults.csv",
        "ACMOnlyAbstractExecutorFactory___EXPERIMENT_DETAILS_FILE_PATH":
            "C:\\Users\\Fabio\\Documents\\ProjetosGit\\EstimationMethods\\Logs\\ACMOnlyAbstract\\Log.txt",
    }

    def get_path(self, key):
        return WindowsPathDictionary._PATH_DICTIONARY[key]
