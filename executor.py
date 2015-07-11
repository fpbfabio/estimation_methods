from abs_executor import AbsExecutor
from factory import Factory

from datetime import datetime, timedelta


class Executor(AbsExecutor):
    NUMBER_ITERATIONS = 20

    def __init__(self):
        self.__factory = Factory()
        self.__estimator = None
        self.__logger = self.factory.create_logger()

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

    def execute(self):
        self.logger.write_header()
        self.estimator = self.factory.create_estimator()
        self.logger.write_experiment_details(self.estimator.experiment_details)
        estimation_list = []
        duration_sum = timedelta()
        connections_sum = 0
        for i in range(0, Executor.NUMBER_ITERATIONS):
            self.estimator = self.factory.create_estimator()
            start = datetime.now()
            estimation = self.estimator.estimate()
            end = datetime.now()
            estimation_list.append(estimation)
            self.logger.write_result_iteration(i + 1, estimation, end - start, self.estimator.download_count)
            duration_sum += end - start
            connections_sum += self.estimator.download_count
        self.logger.write_final_result(estimation_list, duration_sum, connections_sum)


if __name__ == "__main__":
    executor = Executor()
    executor.execute()
