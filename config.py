""""
This is the module used for configure the parameters of a estimation experiment.
"""


class Config:
    """
    Class used to hold constants.

    Attributes:
        URL                             The url used to submit queries to the search engine.
        DATA_SET_SIZE                   The size of the data set being estimated.
        SEARCH_ENGINE_LIMIT             The limit in the number of results imposed by the search engine.
        QUERY_POOL_FILE_PATH            Path to a file containing a query pool.
        FIELD_TO_SEARCH                 The field in the Solr core schema whose content will be targeted by the queries.
        QUERY_MASK                      A special string contained in URL where the queries will be inserted.
        EXPERIMENT_RESULTS_FILE_PATH    Path to the file where the results of the estimation will be saved.
        EXPERIMENT_DETAILS_FILE_PATH    Path to the file where parameters of the experiment will be saved.
        ID_FIELD                        The field in the Solr core schema which is the unique identifier of a document.
    """
    URL = ("http://localhost:8984/solr/newsgroups/select?"
           + "q=::FIELD:::::QUERY::&start=::OFFSET::&rows=::LIMIT::&fl=::FIELDS_TO_RETURN::&wt=json")
    DATA_SET_SIZE = 19994
    SEARCH_ENGINE_LIMIT = 1000000
    QUERY_POOL_FILE_PATH = "/home/fabio/SolrCores/WordLists/newsgroups.txt"
    FIELD_TO_SEARCH = "text"
    THREAD_LIMIT = 20
    OFFSET_MASK = "::OFFSET::"
    LIMIT_MASK = "::LIMIT::"
    FIELD_TO_SEARCH_MASK = "::FIELD::"
    FIELDS_TO_RETURN_MASK = "::FIELDS_TO_RETURN::"
    QUERY_MASK = "::QUERY::"
    EXPERIMENT_RESULTS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/ExperimentResults.csv"
    EXPERIMENT_DETAILS_FILE_PATH = "/home/fabio/GitProjects/EstimationMethods/Logs/Log.txt"
    ID_FIELD = "id"
