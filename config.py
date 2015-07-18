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
    """
    SEARCH_ENGINE_LIMIT = 4501
    QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/new_shine.txt"
    DATA_SET_SIZE = 3697177
    THREAD_LIMIT = 1
