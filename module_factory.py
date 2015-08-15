import abc

import module_crawler_api
import module_data
import module_estimator
import module_logger
import module_parallelizer
import module_path_dictionary
import module_search_result
import module_terminator
import module_word_extractor


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
        return module_path_dictionary.WindowsPathDictionary()


class MhrSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MhrSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MhrSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_crawler_api.SolrCrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(RandomWalkSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(RandomWalkSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_crawler_api.SolrCrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(BroderEtAlSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(BroderEtAlSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_crawler_api.SolrCrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(SumEstSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(SumEstSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_crawler_api.SolrCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(
            module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRRegSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRRegSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegSolrExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.SolrCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHRegSolrExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHRegSolrExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MhrIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MhrIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MhrIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_crawler_api.IEEECrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(RandomWalkIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(RandomWalkIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_crawler_api.IEEECrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(BroderEtAlIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(BroderEtAlIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_crawler_api.IEEECrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(SumEstIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(SumEstIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_crawler_api.IEEECrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(
            module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRRegIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRRegIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegIEEEExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.IEEECrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHRegIEEEExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHRegIEEEExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEECrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MhrIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MhrIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MhrIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_crawler_api.IEEEOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(RandomWalkIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(RandomWalkIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(BroderEtAlIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(BroderEtAlIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(SumEstIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(SumEstIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(MCRRegIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(MCRRegIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
            module_estimator.AbsShokouhi.FACTOR_N)


class CHIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegIEEEOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.IEEEOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHRegIEEEOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHRegIEEEOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEEOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MhrIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(MhrIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(MhrIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(RandomWalkIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(RandomWalkIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(BroderEtAlIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(BroderEtAlIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(SumEstIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(SumEstIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(MCRIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(MCRIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(MCRRegIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(MCRRegIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_estimator.AbsShokouhi.FACTOR_N)


class CHIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegIEEEOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.IEEEOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(CHRegIEEEOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(CHRegIEEEOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.get_data_set_size(),
            module_estimator.AbsShokouhi.FACTOR_N)


class MhrACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MhrACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MhrACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMCrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(RandomWalkACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(RandomWalkACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMCrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(BroderEtAlACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(BroderEtAlACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMCrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(SumEstACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(SumEstACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRRegACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRRegACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegACMExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.ACMCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHRegACMExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHRegACMExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MhrACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MhrACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MhrACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(RandomWalkACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(RandomWalkACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
            module_crawler_api.ACMOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(BroderEtAlACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(BroderEtAlACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
            module_crawler_api.ACMOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(SumEstACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(SumEstACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRRegACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRRegACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegACMOnlyTitleExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.ACMOnlyTitleCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHRegACMOnlyTitleExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHRegACMOnlyTitleExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MhrACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MhrACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MhrACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
                                    module_crawler_api.ACMOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class RandomWalkACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(RandomWalkACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(RandomWalkACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class BroderEtAlACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(BroderEtAlACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(BroderEtAlACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class SumEstACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(SumEstACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(SumEstACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MCRACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(MCRACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(MCRACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class MCRRegACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(MCRRegACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(MCRRegACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
            module_estimator.AbsShokouhi.FACTOR_N)


class CHACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(CHACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(CHACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
                                    module_estimator.AbsShokouhi.FACTOR_N)


class CHRegACMOnlyAbstractExecutorFactory(AbsBaseFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.ACMOnlyAbstractCrawlerApi())

    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(
            path_dict.get_path(CHRegACMOnlyAbstractExecutorFactory._EXPERIMENT_DETAILS_FILE_PATH),
            path_dict.get_path(CHRegACMOnlyAbstractExecutorFactory._EXPERIMENT_RESULTS_FILE_PATH),
            module_crawler_api.ACMOnlyAbstractCrawlerApi.get_data_set_size(),
            module_estimator.AbsShokouhi.FACTOR_N)


class EstimatorFactory(AbsBaseFactory):
    def create_parallelizer(self):
        return module_parallelizer.Parallelizer()

    def create_word_extractor(self):
        return module_word_extractor.WordExtractor()


class CrawlerApiFactory(AbsBaseFactory):
    def create_search_result(self, number_results, results):
        return module_search_result.SearchResult(number_results, results)

    def create_data(self, identifier, content):
        return module_data.Data(identifier, content)

    def create_terminator(self):
        return module_terminator.Terminator()
