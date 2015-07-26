import signal
from datetime import datetime, timedelta

from abs_executor import AbsExecutor
from abc import ABCMeta, abstractmethod


class AbsBaseExecutor(AbsExecutor, metaclass=ABCMeta):
    NUMBER_ITERATIONS = 1

    @abstractmethod
    def __init__(self):
        self.__factory = None
        self.__estimator = None
        self.__logger = None

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

    # noinspection PyUnusedLocal
    def _on_fatal_failure(self, signal_param, frame):
        class FatalFailure(Exception):
            pass
        raise FatalFailure

    def execute(self):
        signal.signal(signal.SIGUSR1, self._on_fatal_failure)
        self.logger.write_header()
        self.estimator = self.factory.create_estimator()
        self.logger.write_experiment_details(self.estimator.experiment_details)
        estimation_list = []
        duration_sum = timedelta()
        connections_sum = 0
        for i in range(0, AbsBaseExecutor.NUMBER_ITERATIONS):
            start = datetime.now()
            estimation = self.estimator.estimate()
            end = datetime.now()
            estimation_list.append(estimation)
            self.logger.write_result_iteration(i + 1, estimation, end - start, self.estimator.download_count)
            duration_sum += end - start
            connections_sum += self.estimator.download_count
        if AbsBaseExecutor.NUMBER_ITERATIONS > 1:
            self.logger.write_final_result(estimation_list, duration_sum, connections_sum)
