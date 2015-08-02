""""
This is the module that provides an abstract interface for a
class used to obtain estimations of the size of a data set.
"""

from abc import ABCMeta, abstractmethod
import signal
from datetime import timedelta, datetime

from executor_factory import IEEEExecutorFactory, ACMExecutorFactory, SolrExecutorFactory


class AbsExecutor(metaclass=ABCMeta):
    """
    Class used to execute the program.
    """

    @property
    @abstractmethod
    def logger(self):
        """
        Returns the instance of an AbsLogger class.
        """
        pass

    @logger.setter
    @abstractmethod
    def logger(self, val):
        """
        Sets the instance of an AbsLogger class.
        """
        pass

    @property
    @abstractmethod
    def factory(self):
        """
        Returns the instance of an AbsExecutorFactory class.
        """
        pass

    @factory.setter
    @abstractmethod
    def factory(self, val):
        """
        Sets the instance of an AbsExecutorFactory class.
        """
        pass

    @property
    @abstractmethod
    def estimator(self):
        """
        Returns the instance of an AbsEstimator class.
        """
        pass

    @estimator.setter
    @abstractmethod
    def estimator(self, val):
        """
        Sets the instance of an AbsEstimator class.
        """
        pass

    @abstractmethod
    def execute(self):
        """
        Executes the code.
        """
        pass


class AbsBaseExecutor(AbsExecutor, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        self.__factory = None
        self.__estimator = None
        self.__logger = None
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

    def _on_fatal_failure(self, signal_param, frame):
        class FatalFailure(Exception):
            pass
        raise FatalFailure()

    def execute(self):
        signal.signal(signal.SIGUSR1, self._on_fatal_failure)
        self.logger.write_header()
        self.logger.write_experiment_details(self.estimator.experiment_details)
        estimation_list = []
        duration_sum = timedelta()
        connections_sum = 0
        for i in range(0, self.number_iterations):
            start = datetime.now()
            estimation = self.estimator.estimate()
            end = datetime.now()
            estimation_list.append(estimation)
            self.logger.write_result_iteration(i + 1, estimation, end - start, self.estimator.download_count)
            duration_sum += end - start
            connections_sum += self.estimator.download_count
        if self.number_iterations > 1:
            self.logger.write_final_result(estimation_list, duration_sum, connections_sum)


class SolrExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 20

    def __init__(self):
        super().__init__()
        self.factory = SolrExecutorFactory()
        self.estimator = self.factory.create_estimator()
        self.logger = self.factory.create_logger(self.estimator.query_pool_file_path)
        self.number_iterations = SolrExecutor._NUMBER_ITERATIONS


class IEEEExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 1

    def __init__(self):
        super().__init__()
        self.factory = IEEEExecutorFactory()
        self.estimator = self.factory.create_estimator()
        self.logger = self.factory.create_logger(self.estimator.query_pool_file_path)
        self.number_iterations = IEEEExecutor._NUMBER_ITERATIONS


class ACMExecutor(AbsBaseExecutor):

    _NUMBER_ITERATIONS = 1

    def __init__(self):
        super().__init__()
        self.factory = ACMExecutorFactory()
        self.estimator = self.factory.create_estimator()
        self.logger = self.factory.create_logger(self.estimator.query_pool_file_path)
        self.number_iterations = ACMExecutor._NUMBER_ITERATIONS
