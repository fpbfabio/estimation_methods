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


class AbsSolrExecutorFactory(AbsBaseFactory, metaclass=abc.ABCMeta):
    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(type(self)._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(type(self)._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.SolrCrawlerApi.get_data_set_size(),
                                    module_crawler_api.SolrCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MhrSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.SolrCrawlerApi())


class ExactMhrSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "ExactMhrSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ExactMhrSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.ExactMhr(module_crawler_api.SolrCrawlerApi())


class TeacherMhrSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "TeacherMhrSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "TeacherMhrSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.TeacherMhr(module_crawler_api.SolrCrawlerApi())


class RandomWalkSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.SolrCrawlerApi())


class BroderEtAlSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.SolrCrawlerApi())


class SumEstSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.SolrCrawlerApi())


class MCRSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.SolrCrawlerApi())


class MCRRegSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(
            module_crawler_api.SolrCrawlerApi())


class CHSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.SolrCrawlerApi())


class CHRegSolrExecutorFactory(AbsSolrExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegSolrExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegSolrExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.SolrCrawlerApi())


class AbsIEEEExecutorFactory(AbsBaseFactory, metaclass=abc.ABCMeta):
    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(type(self)._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(type(self)._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.AbsIEEECrawlerApi.get_data_set_size(),
                                    module_crawler_api.AbsIEEECrawlerApi.DEFAULT_LIMIT_RESULTS)


class MhrIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.IEEECrawlerApi())


class ExactMhrIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "ExactMhrIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ExactMhrIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.ExactMhr(module_crawler_api.IEEECrawlerApi())


class TeacherMhrIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "TeacherMhrIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "TeacherMhrIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.TeacherMhr(module_crawler_api.IEEECrawlerApi())


class RandomWalkIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.IEEECrawlerApi())


class BroderEtAlIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.IEEECrawlerApi())


class SumEstIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.IEEECrawlerApi())


class MCRIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.IEEECrawlerApi())


class MCRRegIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(
            module_crawler_api.IEEECrawlerApi())


class CHIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.IEEECrawlerApi())


class CHRegIEEEExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegIEEEExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegIEEEExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.IEEECrawlerApi())


class MhrIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class RandomWalkIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class BroderEtAlIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class SumEstIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class MCRIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class MCRRegIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class CHIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class CHRegIEEEOnlyTitleExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegIEEEOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.IEEEOnlyTitleCrawlerApi())


class MhrIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class ExactMhrIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "ExactMhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ExactMhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.ExactMhr(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class TeacherMhrIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "TeacherMhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "TeacherMhrIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.TeacherMhr(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class RandomWalkIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class BroderEtAlIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class SumEstIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class MCRIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class MCRRegIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class CHIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class CHRegIEEEOnlyAbstractExecutorFactory(AbsIEEEExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegIEEEOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.IEEEOnlyAbstractCrawlerApi())


class AbsACMExecutorFactory(AbsBaseFactory):
    def create_logger(self, query_pool_file_path):
        path_dict = self.create_path_dictionary()
        return module_logger.Logger(path_dict.get_path(type(self)._EXPERIMENT_DETAILS_FILE_PATH),
                                    path_dict.get_path(type(self)._EXPERIMENT_RESULTS_FILE_PATH),
                                    module_crawler_api.AbsACMCrawlerApi.get_data_set_size(),
                                    module_crawler_api.AbsACMCrawlerApi.DEFAULT_LIMIT_RESULTS)


class MhrACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.ACMCrawlerApi())


class ExactMhrACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "ExactMhrACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ExactMhrACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.ExactMhr(module_crawler_api.ACMCrawlerApi())


class TeacherMhrACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "TeacherMhrACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "TeacherMhrACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.TeacherMhr(module_crawler_api.ACMCrawlerApi())


class RandomWalkACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.ACMCrawlerApi())


class BroderEtAlACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.ACMCrawlerApi())


class SumEstACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.ACMCrawlerApi())


class MCRACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.ACMCrawlerApi())


class MCRRegACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.ACMCrawlerApi())


class CHACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.ACMCrawlerApi())


class CHRegACMExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegACMExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegACMExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.ACMCrawlerApi())


class MhrACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.ACMOnlyTitleCrawlerApi())


class ExactMhrACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "ExactMhrACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ExactMhrACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.ExactMhr(module_crawler_api.ACMOnlyTitleCrawlerApi())


class TeacherMhrACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "TeacherMhrACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "TeacherMhrACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.TeacherMhr(module_crawler_api.ACMOnlyTitleCrawlerApi())


class RandomWalkACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.ACMOnlyTitleCrawlerApi())


class BroderEtAlACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.ACMOnlyTitleCrawlerApi())


class SumEstACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.ACMOnlyTitleCrawlerApi())


class MCRACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.ACMOnlyTitleCrawlerApi())


class MCRRegACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.ACMOnlyTitleCrawlerApi())


class CHACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.ACMOnlyTitleCrawlerApi())


class CHRegACMOnlyTitleExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegACMOnlyTitleExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegACMOnlyTitleExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.ACMOnlyTitleCrawlerApi())


class MhrACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MhrACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MhrACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.Mhr(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class ExactMhrACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "ExactMhrACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "ExactMhrACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.ExactMhr(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class TeacherMhrACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "TeacherMhrACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "TeacherMhrACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.TeacherMhr(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class RandomWalkACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "RandomWalkACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "RandomWalkACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.RandomWalk(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class BroderEtAlACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "BroderEtAlACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "BroderEtAlACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.BroderEtAl(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class SumEstACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "SumEstACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "SumEstACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.SumEst(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class MCRACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCR(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class MCRRegACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "MCRRegACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "MCRRegACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.MCRReg(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class CHACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CH(module_crawler_api.ACMOnlyAbstractCrawlerApi())


class CHRegACMOnlyAbstractExecutorFactory(AbsACMExecutorFactory):
    _EXPERIMENT_RESULTS_FILE_PATH = "CHRegACMOnlyAbstractExecutorFactory__EXPERIMENT_RESULTS_FILE_PATH"
    _EXPERIMENT_DETAILS_FILE_PATH = "CHRegACMOnlyAbstractExecutorFactory__EXPERIMENT_DETAILS_FILE_PATH"

    def create_estimator(self):
        return module_estimator.CHReg(module_crawler_api.ACMOnlyAbstractCrawlerApi())


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
