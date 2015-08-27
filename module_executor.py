import abc
import signal
import time
import datetime
import subprocess

import module_factory


class AbsExecutor(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def logger(self):
        pass

    @logger.setter
    @abc.abstractmethod
    def logger(self, val):
        pass

    @property
    @abc.abstractmethod
    def factory(self):
        pass

    @factory.setter
    @abc.abstractmethod
    def factory(self, val):
        pass

    @property
    @abc.abstractmethod
    def estimator(self):
        pass

    @estimator.setter
    @abc.abstractmethod
    def estimator(self, val):
        pass

    @abc.abstractmethod
    def execute(self):
        pass


class AbsBaseExecutor(AbsExecutor, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.__factory = self._create_factory()
        self.__estimator = self.factory.create_estimator()
        self.__logger = self.factory.create_logger(self.__estimator.query_pool_file_path)
        self.__number_iterations = None

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, val):
        self.__logger = val

    @property
    def factory(self):
        return self.__factory

    @factory.setter
    def factory(self, val):
        self.__factory = val

    @property
    def estimator(self):
        return self.__estimator

    @estimator.setter
    def estimator(self, val):
        self.__estimator = val

    @property
    def number_iterations(self):
        return self.__number_iterations

    @number_iterations.setter
    def number_iterations(self, val):
        self.__number_iterations = val

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def _on_fatal_failure(self, signal_param, frame):
        class FatalFailure(Exception):
            pass
        raise FatalFailure()

    def execute(self):
        signal.signal(signal.SIGTERM, self._on_fatal_failure)
        self.logger.write_header()
        self.logger.write_experiment_details(self.estimator.experiment_details)
        estimation_list = []
        duration_sum = datetime.timedelta()
        connections_sum = 0
        for i in range(0, self.number_iterations):
            start = datetime.datetime.now()
            estimation = self.estimator.estimate()
            end = datetime.datetime.now()
            estimation_list.append(estimation)
            self.logger.write_result_iteration(i + 1, estimation, end - start, self.estimator.download_count)
            duration_sum += end - start
            connections_sum += self.estimator.download_count
        if self.number_iterations > 1:
            self.logger.write_final_result(estimation_list, duration_sum, connections_sum)


class AbsSolrExecutor(AbsBaseExecutor):
    _CREATE_CORE_COMMAND = "AbsSolrExecutor__CREATE_CORE_COMMAND"
    _UNLOAD_CORE_COMMAND = "AbsSolrExecutor__UNLOAD_CORE_COMMAND"
    _START_SOLR_COMMAND = "AbsSolrExecutor__START_SOLR_COMMAND"
    _STOP_SOLR_COMMAND = "AbsSolrExecutor__STOP_SOLR_COMMAND"
    _QUERY_POOL_PATH_LIST = "AbsSolrExecutor__QUERY_POOL_PATH_LIST"
    _CORE_PATH_LIST = "AbsSolrExecutor__CORE_PATH_LIST"
    _NUMBER_ITERATIONS = 20

    def __init__(self):
        self.factory = self._create_factory()
        path_dict = self.factory.create_path_dictionary()
        subprocess.call(path_dict.get_path(AbsSolrExecutor._STOP_SOLR_COMMAND), shell=True)
        time.sleep(2)
        subprocess.call(path_dict.get_path(AbsSolrExecutor._START_SOLR_COMMAND), shell=True)
        time.sleep(10)
        self.estimator = self.factory.create_estimator()
        self.number_iterations = AbsSolrExecutor._NUMBER_ITERATIONS

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def execute(self):
        path_dict = self.factory.create_path_dictionary()
        solr_core_path_list = path_dict.get_path(AbsSolrExecutor._CORE_PATH_LIST)
        query_pool_path_list = path_dict.get_path(AbsSolrExecutor._QUERY_POOL_PATH_LIST)
        count = 0
        for core_path, query_pool_path in zip(solr_core_path_list, query_pool_path_list):
            subprocess.call(path_dict.get_path(AbsSolrExecutor._UNLOAD_CORE_COMMAND), shell=True)
            time.sleep(5)
            subprocess.call(path_dict.get_path(AbsSolrExecutor._CREATE_CORE_COMMAND) + core_path, shell=True)
            time.sleep(5)
            self.estimator.query_pool_file_path = query_pool_path
            self.logger = self.factory.create_logger(self.estimator.query_pool_file_path)
            super().execute()
            count += 1
            print("Experiment " + str(count) + " complete.")


class MhrSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.MhrSolrExecutorFactory()


class ExactMhrSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrSolrExecutorFactory()


class TeacherMhrSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrSolrExecutorFactory()


class SumEstSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.SumEstSolrExecutorFactory()


class RandomWalkSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkSolrExecutorFactory()


class BroderEtAlSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlSolrExecutorFactory()


class MCRSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.MCRSolrExecutorFactory()


class MCRRegSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.MCRRegSolrExecutorFactory()


class CHSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.CHSolrExecutorFactory()


class CHRegSolrExecutor(AbsSolrExecutor):
    def _create_factory(self):
        return module_factory.CHRegSolrExecutorFactory()


class AbsIEEEExecutor(AbsBaseExecutor):
    _NUMBER_ITERATIONS = 1

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsIEEEExecutor._NUMBER_ITERATIONS


class MhrIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.MhrIEEEExecutorFactory()


class ExactMhrIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrIEEEExecutorFactory()


class TeacherMhrIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrIEEEExecutorFactory()


class SumEstIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.SumEstIEEEExecutorFactory()


class RandomWalkIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkIEEEExecutorFactory()


class BroderEtAlIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlIEEEExecutorFactory()


class MCRIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.MCRIEEEExecutorFactory()


class MCRRegIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.MCRRegIEEEExecutorFactory()


class CHIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.CHIEEEExecutorFactory()


class CHRegIEEEExecutor(AbsIEEEExecutor):
    def _create_factory(self):
        return module_factory.CHRegIEEEExecutorFactory()


class AbsIEEEOnlyTitleExecutor(AbsBaseExecutor):
    _NUMBER_ITERATIONS = 3

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsIEEEOnlyTitleExecutor._NUMBER_ITERATIONS


class MhrIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.MhrIEEEOnlyTitleExecutorFactory()


class ExactMhrIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrIEEEOnlyTitleExecutorFactory()


class TeacherMhrIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrIEEEOnlyTitleExecutorFactory()


class SumEstIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.SumEstIEEEOnlyTitleExecutorFactory()


class RandomWalkIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkIEEEOnlyTitleExecutorFactory()


class BroderEtAlIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlIEEEOnlyTitleExecutorFactory()


class MCRIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.MCRIEEEOnlyTitleExecutorFactory()


class MCRRegIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.MCRRegIEEEOnlyTitleExecutorFactory()


class CHIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.CHIEEEOnlyTitleExecutorFactory()


class CHRegIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.CHRegIEEEOnlyTitleExecutorFactory()


class AbsIEEEOnlyAbstractExecutor(AbsBaseExecutor):
    _NUMBER_ITERATIONS = 3

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsIEEEOnlyAbstractExecutor._NUMBER_ITERATIONS


class MhrIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.MhrIEEEOnlyAbstractExecutorFactory()


class ExactMhrIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrIEEEOnlyAbstractExecutorFactory()


class TeacherMhrIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrIEEEOnlyAbstractExecutorFactory()


class SumEstIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.SumEstIEEEOnlyAbstractExecutorFactory()


class RandomWalkIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkIEEEOnlyAbstractExecutorFactory()


class BroderEtAlIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlIEEEOnlyAbstractExecutorFactory()


class MCRIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.MCRIEEEOnlyAbstractExecutorFactory()


class MCRRegIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.MCRRegIEEEOnlyAbstractExecutorFactory()


class CHIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.CHIEEEOnlyAbstractExecutorFactory()


class CHRegIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.CHRegIEEEOnlyAbstractExecutorFactory()


class AbsACMExecutor(AbsBaseExecutor):
    _NUMBER_ITERATIONS = 1

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsACMExecutor._NUMBER_ITERATIONS


class MhrACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.MhrACMExecutorFactory()


class ExactMhrACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrACMExecutorFactory()


class TeacherMhrACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrACMExecutorFactory()


class SumEstACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.SumEstACMExecutorFactory()


class RandomWalkACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkACMExecutorFactory()


class BroderEtAlACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlACMExecutorFactory()


class MCRACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.MCRACMExecutorFactory()


class MCRRegACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.MCRRegACMExecutorFactory()


class CHACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.CHACMExecutorFactory()


class CHRegACMExecutor(AbsACMExecutor):
    def _create_factory(self):
        return module_factory.CHRegACMExecutorFactory()


class AbsACMOnlyTitleExecutor(AbsBaseExecutor):
    _NUMBER_ITERATIONS = 3

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsACMOnlyTitleExecutor._NUMBER_ITERATIONS


class MhrACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.MhrACMOnlyTitleExecutorFactory()


class ExactMhrACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrACMOnlyTitleExecutorFactory()


class TeacherMhrACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrACMOnlyTitleExecutorFactory()


class SumEstACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.SumEstACMOnlyTitleExecutorFactory()


class RandomWalkACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkACMOnlyTitleExecutorFactory()


class BroderEtAlACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlACMOnlyTitleExecutorFactory()


class MCRACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.MCRACMOnlyTitleExecutorFactory()


class MCRRegACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.MCRRegACMOnlyTitleExecutorFactory()


class CHACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.CHACMOnlyTitleExecutorFactory()


class CHRegACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):
    def _create_factory(self):
        return module_factory.CHRegACMOnlyTitleExecutorFactory()


class AbsACMOnlyAbstractExecutor(AbsBaseExecutor):
    _NUMBER_ITERATIONS = 3

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsACMOnlyAbstractExecutor._NUMBER_ITERATIONS


class MhrACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.MhrACMOnlyAbstractExecutorFactory()


class ExactMhrACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.ExactMhrACMOnlyAbstractExecutorFactory()


class TeacherMhrACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.TeacherMhrACMOnlyAbstractExecutorFactory()


class SumEstACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.SumEstACMOnlyAbstractExecutorFactory()


class RandomWalkACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.RandomWalkACMOnlyAbstractExecutorFactory()


class BroderEtAlACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.BroderEtAlACMOnlyAbstractExecutorFactory()


class MCRACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.MCRACMOnlyAbstractExecutorFactory()


class MCRRegACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.MCRRegACMOnlyAbstractExecutorFactory()


class CHACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.CHACMOnlyAbstractExecutorFactory()


class CHRegACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):
    def _create_factory(self):
        return module_factory.CHRegACMOnlyAbstractExecutorFactory()
