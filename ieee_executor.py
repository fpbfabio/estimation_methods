from ieee_executor_factory import IEEEExecutorFactory
from abs_base_executor import AbsBaseExecutor


class IEEEExecutor(AbsBaseExecutor):
    def __init__(self):
        super().__init__()
        self.factory = IEEEExecutorFactory()
        self.estimator = self.factory.create_estimator()
        self.logger = self.factory.create_logger()


if __name__ == "__main__":
    executor = IEEEExecutor()
    executor.execute()
