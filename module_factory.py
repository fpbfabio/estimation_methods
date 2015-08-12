# region imports


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

# endregion

# region AbsFactory


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

# endregion

# region AbsExceptionFactory


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

# endregion

# region AbsBaseFactory


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

# endregion

# region SolrExecutorFactory


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
                                    module_crawler_api.SolrCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.SolrCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.SolrCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.SolrCrawlerApi.LIMIT_RESULTS)


# endregion

# region IEEEExecutorFactory


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
                                    module_crawler_api.IEEECrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.IEEECrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.IEEECrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.IEEECrawlerApi.LIMIT_RESULTS)


# endregion

# region IEEEOnlyTitleExecutorFactory


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
                                    module_crawler_api.IEEEOnlyTitleCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.IEEEOnlyTitleCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.IEEEOnlyTitleCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.IEEEOnlyTitleCrawlerApi.LIMIT_RESULTS)


# endregion

# region IEEEOnlyAbstractExecutorFactory


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
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.IEEEOnlyAbstractCrawlerApi.LIMIT_RESULTS)


# endregion

# region ACMExecutorFactory


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
                                    module_crawler_api.ACMCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.ACMCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.ACMCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.ACMCrawlerApi.LIMIT_RESULTS)


# endregion

# region ACMOnlyTitleExecutorFactory


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
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.ACMOnlyTitleCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.ACMOnlyTitleCrawlerApi.LIMIT_RESULTS)


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
                                    module_crawler_api.ACMOnlyTitleCrawlerApi.LIMIT_RESULTS)


# endregion

# region ACMOnlyAbstractExecutorFactory


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
                                    module_crawler_api.ACMOnlyAbstractCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.ACMOnlyAbstractCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.ACMOnlyAbstractCrawlerApi.LIMIT_RESULTS)


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
            module_crawler_api.ACMOnlyAbstractCrawlerApi.LIMIT_RESULTS)


# endregion

# region EstimatorFactory


class EstimatorFactory(AbsBaseFactory):
    def create_parallelizer(self):
        return module_parallelizer.Parallelizer()

    def create_word_extractor(self):
        return module_word_extractor.WordExtractor()

# endregion

# region CrawlerApiFactory


class CrawlerApiFactory(AbsBaseFactory):
    def create_search_result(self, number_results, results):
        return module_search_result.SearchResult(number_results, results)

    def create_data(self, identifier, content):
        return module_data.Data(identifier, content)

    def create_terminator(self):
        return module_terminator.Terminator()

# endregion
