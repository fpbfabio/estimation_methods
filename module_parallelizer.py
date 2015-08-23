import abc
import threading


class AbsParallelizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute_in_parallel(self, thread_limit, collection, callback):
        pass


class Parallelizer(AbsParallelizer):
    def execute_in_parallel(self, thread_limit, collection, callback):
        thread_list = []
        for item in collection:
            if len(thread_list) >= thread_limit:
                thread_list[0].join()
                del (thread_list[0])
            thread = threading.Thread(target=callback, args=(item,))
            thread_list.append(thread)
            thread.start()
        for thread in thread_list:
            thread.join()
