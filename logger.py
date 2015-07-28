""""
Module with an abstract class for writing logs.
"""

from abc import ABCMeta, abstractmethod
import math
import os
import statistics


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
    def write_result_iteration(self, iteration_number, result, duration, cost):
        """
        Writes the result of an iteration of the experiment.
        """
        pass

    @abstractmethod
    def write_final_result(self, result_list, total_duration, total_cost):
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


class Logger(AbsLogger):

    def __init__(self, details_file_path, results_file_path, data_set_size, limit_results, query_pool_file_path):
        self.__experiment_details_file_path = details_file_path
        self.__experiment_results_file_path = results_file_path
        self.__data_set_size = data_set_size
        self.__limit_results = limit_results
        self.__query_pool_file_path = query_pool_file_path

    def write_header(self):
        with open(self.__experiment_results_file_path, "a+") as file:
            file.write(str(self.__data_set_size) + "," + os.linesep)
            file.write("Iteração,Estimativa,Erro,Duração,Conexões," + os.linesep)

    def write_result_iteration(self, iteration_number, result, duration, cost):
        error = math.fabs(self.__data_set_size - result) / self.__data_set_size
        with open(self.__experiment_results_file_path, "a+") as file:
            file.write(str(iteration_number) + "," + str(result) + "," + str(error) + "," + str(duration) + ","
                       + str(cost) + "," + os.linesep)

    def write_final_result(self, result_list, total_duration, total_cost):
        average = statistics.mean(result_list)
        std_deviation = statistics.pstdev(result_list, average)
        coef_variation = std_deviation / average
        error = math.fabs(self.__data_set_size - average) / self.__data_set_size
        with open(self.__experiment_results_file_path, "a+") as file:
            file.write("Coeficiente de Variação,Estimativa Média,Erro da Média,Duração Total,Total de Conexões,"
                       + os.linesep)
            file.write(str(coef_variation) + "," + str(average) + "," + str(error) + "," + str(total_duration)
                       + "," + str(total_cost) + "," + os.linesep)

    def write_experiment_details(self, additional_information=None):
        with open(self.__experiment_details_file_path, "a+") as file:
            file.write("Limite da máquina de busca: " + str(self.__limit_results) + os.linesep)
            file.write("Lista de palavras: " + self.__query_pool_file_path + os.linesep)
            if additional_information is not None:
                key_list = list(additional_information.keys())
                for key in key_list:
                    file.write(str(key) + ": " + str(additional_information[key]) + os.linesep)
