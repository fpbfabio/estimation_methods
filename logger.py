import os
import math
import statistics

from config import Config
from abs_logger import AbsLogger


class Logger(AbsLogger):
    def __init__(self, details_file_path, results_file_path, data_set_size, query_pool_file_path):
        self.experiment_details_file_path = details_file_path
        self.experiment_results_file_path = results_file_path
        self.data_set_size = data_set_size
        self.query_pool_file_path = query_pool_file_path

    def write_header(self):
        with open(self.experiment_results_file_path, "a+") as file:
            file.write(str(self.data_set_size) + "," + os.linesep)
            file.write("Iteração,Estimativa,Erro,Duração,Conexões," + os.linesep)

    def write_result_iteration(self, iteration_number, estimation, duration, connections):
        error = math.fabs(self.data_set_size - estimation) / self.data_set_size
        with open(self.experiment_results_file_path, "a+") as file:
            file.write(str(iteration_number) + "," + str(estimation) + "," + str(error) + "," + str(duration) + ","
                       + str(connections) + "," + os.linesep)

    def write_final_result(self, estimation_list, total_duration, total_connections):
        average = statistics.mean(estimation_list)
        std_deviation = statistics.pstdev(estimation_list, average)
        coef_variation = std_deviation / average
        error = math.fabs(self.data_set_size - average) / self.data_set_size
        with open(self.experiment_results_file_path, "a+") as file:
            file.write("Coeficiente de Variação,Estimativa Média,Erro da Média,Duração Total,Total de Conexões,"
                       + os.linesep)
            file.write(str(coef_variation) + "," + str(average) + "," + str(error) + "," + str(total_duration)
                       + "," + str(total_connections) + "," + os.linesep)

    def write_experiment_details(self, additional_information=None):
        with open(self.experiment_details_file_path, "a+") as file:
            file.write("Limite da máquina de busca: " + str(Config.SEARCH_ENGINE_LIMIT) + os.linesep)
            file.write("Lista de palavras: " + self.query_pool_file_path + os.linesep)
            if additional_information is not None:
                key_list = list(additional_information.keys())
                for key in key_list:
                    file.write(str(key) + ": " + str(additional_information[key]) + os.linesep)
