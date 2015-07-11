""""
This is the module used for configure the parameters of a estimation experiment
"""


class Config:
    URL = "http://localhost:8984/solr/newsgroups/select?q=::FIELD:::::QUERY::&rows=::LIMIT::&wt=json"
    DATA_SET_SIZE = 19994
    SEARCH_ENGINE_LIMIT = 1000000
    QUERY_POOL_FILE_PATH = "C:\\Users\\Fabio\\Documents\\tcc\\listas_palavras\\newsgroups.txt"
    FIELD_TO_SEARCH = "text"
    THREAD_LIMIT = 20
    LIMIT_MASK = "::LIMIT::"
    FIELD_TO_SEARCH_MASK = "::FIELD::"
    QUERY_MASK = "::QUERY::"
    EXPERIMENT_RESULTS_FILE_PATH = "C:\\Users\\Fabio\\Documents\\projetos\\estimation_methods\\logs\\log.txt"
    EXPERIMENT_DETAILS_FILE_PATH = "C:\\Users\\Fabio\\Documents\\projetos\\estimation_methods\\logs\\log.txt"
    ID_FIELD = "id"
