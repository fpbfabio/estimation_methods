# region imports


import abc
import signal
import datetime

import module_factory


# endregion

# region AbsExecutor


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

# endregion

# region AbsBaseExecutor


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


# endregion

# region SolrExecutor


class AbsSolrExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsSolrExecutor._NUMBER_ITERATIONS


class MhrSolrExecutor(AbsSolrExecutor):

    def _create_factory(self):
        return module_factory.MhrSolrExecutorFactory()


class SumEstSolrExecutor(AbsSolrExecutor):

    def _create_factory(self):
        return module_factory.SumEstSolrExecutorFactory()


class RandomWalkSolrExecutor(AbsSolrExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkSolrExecutorFactory()


class BroderEtAlSolrExecutor(AbsSolrExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlSolrExecutorFactory()


# endregion

# region IEEEExecutor


class AbsIEEEExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsIEEEExecutor._NUMBER_ITERATIONS


class MhrIEEEExecutor(AbsIEEEExecutor):

    def _create_factory(self):
        return module_factory.MhrIEEEExecutorFactory()


class SumEstIEEEExecutor(AbsIEEEExecutor):

    def _create_factory(self):
        return module_factory.SumEstIEEEExecutorFactory()


class RandomWalkIEEEExecutor(AbsIEEEExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkIEEEExecutorFactory()


class BroderEtAlIEEEExecutor(AbsIEEEExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlIEEEExecutorFactory()


# endregion

# region IEEEOnlyTitleExecutor


class AbsIEEEOnlyTitleExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsIEEEOnlyTitleExecutor._NUMBER_ITERATIONS


class MhrIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.MhrIEEEOnlyTitleExecutorFactory()


class SumEstIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.SumEstIEEEOnlyTitleExecutorFactory()


class RandomWalkIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkIEEEOnlyTitleExecutorFactory()


class BroderEtAlIEEEOnlyTitleExecutor(AbsIEEEOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlIEEEOnlyTitleExecutorFactory()


# endregion

# region IEEEOnlyAbstractExecutor


class AbsIEEEOnlyAbstractExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsIEEEOnlyAbstractExecutor._NUMBER_ITERATIONS


class MhrIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.MhrIEEEOnlyAbstractExecutorFactory()


class SumEstIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.SumEstIEEEOnlyAbstractExecutorFactory()


class RandomWalkIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkIEEEOnlyAbstractExecutorFactory()


class BroderEtAlIEEEOnlyAbstractExecutor(AbsIEEEOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlIEEEOnlyAbstractExecutorFactory()


# endregion

# region ACMExecutor


class AbsACMExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsACMExecutor._NUMBER_ITERATIONS


class MhrACMExecutor(AbsACMExecutor):

    def _create_factory(self):
        return module_factory.MhrACMExecutorFactory()


class SumEstACMExecutor(AbsACMExecutor):

    def _create_factory(self):
        return module_factory.SumEstACMExecutorFactory()


class RandomWalkACMExecutor(AbsACMExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkACMExecutorFactory()


class BroderEtAlACMExecutor(AbsACMExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlACMExecutorFactory()


# endregion

# region ACMOnlyTitleExecutor


class AbsACMOnlyTitleExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsACMOnlyTitleExecutor._NUMBER_ITERATIONS


class MhrACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.MhrACMOnlyTitleExecutorFactory()


class SumEstACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.SumEstACMOnlyTitleExecutorFactory()


class RandomWalkACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkACMOnlyTitleExecutorFactory()


class BroderEtAlACMOnlyTitleExecutor(AbsACMOnlyTitleExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlACMOnlyTitleExecutorFactory()


# endregion

# region ACMOnlyAbstractExecutor


class AbsACMOnlyAbstractExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    @abc.abstractmethod
    def _create_factory(self):
        pass

    def __init__(self):
        super().__init__()
        self.number_iterations = AbsACMOnlyAbstractExecutor._NUMBER_ITERATIONS


class MhrACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.MhrACMOnlyAbstractExecutorFactory()


class SumEstACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.SumEstACMOnlyAbstractExecutorFactory()


class RandomWalkACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.RandomWalkACMOnlyAbstractExecutorFactory()


class BroderEtAlACMOnlyAbstractExecutor(AbsACMOnlyAbstractExecutor):

    def _create_factory(self):
        return module_factory.BroderEtAlACMOnlyAbstractExecutorFactory()


# endregion
