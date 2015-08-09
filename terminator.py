import abc
import os
import signal


class AbsTerminator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def terminate(self, message):
        pass


class Terminator(AbsTerminator):

    def terminate(self, message):
        print(message)
        os.kill(os.getpid(), signal.SIGTERM)

        class AbortedException(Exception):
            pass

        raise AbortedException()
