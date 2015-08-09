import abc

import crawler_api
import data
import estimator
import logger
import parallelizer
import path_dictionary
import search_result
import terminator
import word_extractor


class AbsFactory(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_search_result(self, number_results, results):
        pass

    @abc.abstractmethod
    def create_data(self, identifier, content):
        pass

    @abc.abstractmethod
    def create_terminator(self):
        pass

    @abc.abstractmethod
    def create_parallelizer(self):
        pass

    @abc.abstractmethod
    def create_word_extractor(self):
        pass

    @abc.abstractmethod
    def create_estimator(self):
        pass

    @abc.abstractmethod
    def create_logger(self, query_pool_file_path):
        pass

    @abc.abstractmethod
    def create_path_dictionary(self):
        pass


class AbsExceptionFactory(AbsFactory, metaclass=abc.ABCMeta):

    def create_search_result(self, number_results, results):
        raise NotImplementedError()

    def create_data(self, identifier, content):
        raise NotImplementedError()

    def create_terminator(self):
        raise NotImplementedError()

    def create_parallelizer(self):
        raise NotImplementedError()

    def create_word_extractor(self):
        raise NotImplementedError()

    def create_estimator(self):
        raise NotImplementedError()

    def create_logger(self, query_pool_file_path):
        raise NotImplementedError()

    def create_path_dictionary(self):
        raise NotImplementedError()


class AbsBaseFactory(AbsExceptionFactory, metaclass=abc.ABCMeta):

    def create_search_result(self, number_results, results):
        return super().create_search_result(number_results, results)

    def create_data(self, identifier, content):
        return super().create_data(identifier, content)

    def create_terminator(self):
        return super().create_terminator()

    def create_parallelizer(self):
        return super().create_parallelizer()

    def create_word_extractor(self):
        return super().create_word_extractor()

    def create_estimator(self):
        return super().create_estimator()

    def create_logger(self, query_pool_file_path):
        return super().create_logger(query_pool_file_path)

    def create_path_dictionary(self):
        return path_dictionary.WindowsPathDictionary()


class SolrExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "SolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(SolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(SolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.SolrCrawlerApi.get_data_set_size(),
                             crawler_api.SolrCrawlerApi.LIMIT_RESULTS)


class IEEEExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "IEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "IEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(IEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(IEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.AbsIEEECrawlerApi.get_data_set_size(),
                             crawler_api.AbsIEEECrawlerApi.LIMIT_RESULTS)


class IEEEOnlyTitleExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "IEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "IEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(IEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(IEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.AbsIEEECrawlerApi.get_data_set_size(),
                             crawler_api.AbsIEEECrawlerApi.LIMIT_RESULTS)


class IEEEOnlyAbstractExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "IEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(IEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(IEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.AbsIEEECrawlerApi.get_data_set_size(),
                             crawler_api.AbsIEEECrawlerApi.LIMIT_RESULTS)


class ACMExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "ACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(ACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(ACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.AbsACMCrawlerApi.get_data_set_size(),
                             crawler_api.AbsACMCrawlerApi.LIMIT_RESULTS)


class ACMOnlyTitleExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "ACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(ACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(ACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.AbsACMCrawlerApi.get_data_set_size(),
                             crawler_api.AbsACMCrawlerApi.LIMIT_RESULTS)


class ACMOnlyAbstractExecutorFactory(AbsBaseFactory):

    _EXPERIMENT_RESULTS_FILE_PATH = "ACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return estimator.Mhr(crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return logger.Logger(path_dict.get_path(ACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                             path_dict.get_path(ACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                             crawler_api.AbsACMCrawlerApi.get_data_set_size(),
                             crawler_api.AbsACMCrawlerApi.LIMIT_RESULTS)


class EstimatorFactory(AbsBaseFactory):

    def create_parallelizer(self):
        return parallelizer.Parallelizer()

    def create_word_extractor(self):
        return word_extractor.WordExtractor()


class CrawlerApiFactory(AbsBaseFactory):

    def create_search_result(self, number_results, results):
        return search_result.SearchResult(number_results, results)

    def create_data(self, identifier, content):
        return data.Data(identifier, content)

    def create_terminator(self):
        return terminator.Terminator()
