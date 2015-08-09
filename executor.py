import abc
import signal
import datetime

import factory


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


class SolrExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    def _create_factory(self):
        return factory.SolrExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = SolrExecutor._NUMBER_ITERATIONS


class IEEEExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 5

    def _create_factory(self):
        return factory.IEEEExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = IEEEExecutor._NUMBER_ITERATIONS


class IEEEOnlyTitleExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 5

    def _create_factory(self):
        return factory.IEEEOnlyTitleExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = IEEEOnlyTitleExecutor._NUMBER_ITERATIONS


class IEEEOnlyAbstractExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 5

    def _create_factory(self):
        return factory.IEEEOnlyAbstractExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = IEEEOnlyAbstractExecutor._NUMBER_ITERATIONS


class ACMExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 5

    def _create_factory(self):
        return factory.ACMExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = ACMExecutor._NUMBER_ITERATIONS


class ACMOnlyTitleExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 5

    def _create_factory(self):
        return factory.ACMOnlyTitleExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = ACMOnlyTitleExecutor._NUMBER_ITERATIONS


class ACMOnlyAbstractExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 5

    def _create_factory(self):
        return factory.ACMOnlyAbstractExecutorFactory()

    def __init__(self):
        super().__init__()
        self.number_iterations = ACMOnlyAbstractExecutor._NUMBER_ITERATIONS
