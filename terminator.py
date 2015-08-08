""""
Module with classes responsible for terminating a program.
"""

from abc import ABCMeta, abstractmethod
import os
import signal


class AbsTerminator(metaclass=ABCMeta):
    """"
    Class responsible for terminating a program.
    """

    @abstractmethod
    def terminate(self, message):
        """
        Terminates the program showing the given message.
        """
        pass


class Terminator(AbsTerminator):

    def terminate(self, message):
        print(message)
        os.kill(os.getpid(), signal.SIGTERM)

        class AbortedException(Exception):
            pass

        raise AbortedException()
