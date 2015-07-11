from abs_executor import AbsExecutor
from factory import Factory


class Executor(AbsExecutor):
    def __init__(self):
        self.__factory = Factory()
        self.__estimator = None

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
        for i in range(0, 20):
            self.estimator = self.factory.create_estimator()
            self.estimator.estimate()


if __name__ == "__main__":
    executor = Executor()
    executor.execute()
