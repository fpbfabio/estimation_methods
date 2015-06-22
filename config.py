""""This is the module used for configure the parameters of a estimation experiment"""

class Config():

	URL = "http://localhost:8984/solr/new_shine/select?q=::FIELD:::::QUERY::&rows=::LIMIT::&wt=json"
	SEARCH_ENGINE_LIMIT = 1000000
	QUERY_POOL_FILE_PATH = "C:\\Users\\Fabio\\Documents\\tcc\\listas_palavras\\new_shine.txt"
	FIELD_TO_SEARCH = "text"
	THREAD_LIMIT = 10
	LIMIT_MASK = "::LIMIT::"
	FIELD_TO_SEARCH_MASK = "::FIELD::"
	QUERY_MASK = "::QUERY::"
	LOG_FILE_PATH = "C:\\Users\\Fabio\\Documents\\projetos\\estimation_methods\\logs\\log.txt"
	ID_FIELD = "id"