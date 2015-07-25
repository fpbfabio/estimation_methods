from acm_executor_factory import ACMExecutorFactory
from abs_base_executor import AbsBaseExecutor


class ACMExecutor(AbsBaseExecutor):
    def __init__(self):
        super().__init__()
        self.factory = ACMExecutorFactory()
        self.estimator = self.factory.create_estimator()
        self.logger = self.factory.create_logger()


if __name__ == "__main__":
    executor = ACMExecutor()
    executor.execute()
