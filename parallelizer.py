""""
This is the module that provides an abstract interface for a
class used to execute code in multiple threads.
"""

from abc import ABCMeta, abstractmethod
from threading import Thread


class AbsParallelizer(metaclass=ABCMeta):
    """
    Helper class for executing code in multiple threads
    """

    @abstractmethod
    def execute_in_parallel(self, thread_limit, collection, callback):
        """
        Executes a function in multiple threads, for each thread
        the callback receives an item from the collection.
        """
        pass


class Parallelizer(AbsParallelizer):

    def execute_in_parallel(self, thread_limit, collection, callback):
        thread_list = []
        for item in collection:
            if len(thread_list) >= thread_limit:
                thread_list[0].join()
                del (thread_list[0])
            thread = Thread(target=callback, args=(item,))
            thread_list.append(thread)
            thread.start()
        for thread in thread_list:
            thread.join()
