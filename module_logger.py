import abc
import math
import statistics
import os


class AbsLogger(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def data_set_size(self):
        pass

    @data_set_size.setter
    @abc.abstractmethod
    def data_set_size(self, val):
        pass

    @abc.abstractmethod
    def write_header(self):
        pass

    @abc.abstractmethod
    def write_result_iteration(self, iteration_number, result, duration, cost):
        pass

    @abc.abstractmethod
    def write_final_result(self, result_list, total_duration, total_cost):
        pass

    @abc.abstractmethod
    def write_experiment_details(self, additional_information=None):
        pass


class Logger(AbsLogger):

    @property
    def data_set_size(self):
        return self.__data_set_size

    @data_set_size.setter
    def data_set_size(self, val):
        self.__data_set_size = val

    def __init__(self, details_file_path, results_file_path, data_set_size, limit_results):
        self.experiment_details_file_path = details_file_path
        self.experiment_results_file_path = results_file_path
        self.__data_set_size = data_set_size
        self.limit_results = limit_results

    def write_header(self):
        os.makedirs(os.path.dirname(self.experiment_results_file_path), exist_ok=True)
        with open(self.experiment_results_file_path, "a+") as file:
            file.write("Gabarito = " + str(self.__data_set_size) + "," + "\n")
            file.write("Iteração,Estimativa,Erro,Duração,Conexões," + "\n")

    def write_result_iteration(self, iteration_number, result, duration, cost):
        error = "%.3f" % (math.fabs(self.__data_set_size - result) / self.__data_set_size)
        result = "%.3f" % result
        os.makedirs(os.path.dirname(self.experiment_results_file_path), exist_ok=True)
        with open(self.experiment_results_file_path, "a+") as file:
            file.write(str(iteration_number) + "," + result + "," + str(error) + "," + str(duration) + ","
                       + str(cost) + "," + "\n")

    def write_final_result(self, result_list, total_duration, total_cost):
        average = "%.3f" % statistics.mean(result_list)
        coef_variation = "%.3f" % (statistics.pstdev(result_list, statistics.mean(result_list))
                                   / statistics.mean(result_list))
        error = "%.3f" % (math.fabs(self.__data_set_size - statistics.mean(result_list)) / self.__data_set_size)
        os.makedirs(os.path.dirname(self.experiment_results_file_path), exist_ok=True)
        with open(self.experiment_results_file_path, "a+") as file:
            file.write("Coeficiente de Variação,Estimativa Média,Erro da Média,Duração Total,Total de Conexões,"
                       + "\n")
            file.write(coef_variation + "," + average + "," + error + "," + str(total_duration)
                       + "," + str(total_cost) + "," + "\n")

    def write_experiment_details(self, additional_information=None):
        os.makedirs(os.path.dirname(self.experiment_details_file_path), exist_ok=True)
        with open(self.experiment_details_file_path, "a+") as file:
            file.write("Limite da máquina de busca: " + str(self.limit_results) + "\n")
            if additional_information is not None:
                key_list = list(additional_information.keys())
                for key in key_list:
                    file.write(str(key) + ": " + str(additional_information[key]) + "\n")
