""""
Module with an abstract class for writing logs.
"""

from abc import ABCMeta, abstractmethod


class AbsLogger(metaclass=ABCMeta):
    """"
    Class for writing logs.
    """

    @abstractmethod
    def write_header(self):
        """
        Writes the header of the log.
        """
        pass

    @abstractmethod
    def write_result_iteration(self, iteration_number, estimation, duration, connections):
        """
        Writes the result of an iteration of the experiment.
        """
        pass

    @abstractmethod
    def write_final_result(self, estimation_list, total_duration, total_connections):
        """
        Writes the aggregate result of the many iterations of the experiment.
        """
        pass

    @abstractmethod
    def write_experiment_details(self, additional_information=None):
        """
        Writes the values of parameters used in the experiment.
        """
        pass
