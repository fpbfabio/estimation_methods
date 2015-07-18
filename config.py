""""
This is the module used for configure the parameters of a estimation experiment.
"""


class Config:
    """
    Class used to hold constants.

    Attributes:
        DATA_SET_SIZE                   The size of the data set being estimated.
        SEARCH_ENGINE_LIMIT             The limit in the number of results imposed by the search engine.
        QUERY_POOL_FILE_PATH            Path to a file containing a query pool.
        EXPERIMENT_RESULTS_FILE_PATH    Path to the file where the results of the estimation will be saved.
        EXPERIMENT_DETAILS_FILE_PATH    Path to the file where parameters of the experiment will be saved.
    """
    SEARCH_ENGINE_LIMIT = 4501
    QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    DATA_SET_SIZE = 3697177
    EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ExperimentResults.csv"
    EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/Log.txt"
    THREAD_LIMIT = 1
