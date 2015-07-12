from config import Config
from abs_logger import AbsLogger
import os
import math
import statistics


class Logger(AbsLogger):
    def write_header(self):
        with open(Config.EXPERIMENT_RESULTS_FILE_PATH, "a+") as file:
            file.write(str(Config.DATA_SET_SIZE) + "," + os.linesep)
            file.write("Iteração,Estimativa,Erro,Duração,Conexões," + os.linesep)

    def write_result_iteration(self, iteration_number, estimation, duration, connections):
        error = math.fabs(Config.DATA_SET_SIZE - estimation) / Config.DATA_SET_SIZE
        with open(Config.EXPERIMENT_RESULTS_FILE_PATH, "a+") as file:
            file.write(str(iteration_number) + "," + str(estimation) + "," + str(error) + "," + str(duration) + ","
                       + str(connections) + "," + os.linesep)

    def write_final_result(self, estimation_list, total_duration, total_connections):
        average = statistics.mean(estimation_list)
        std_deviation = statistics.pstdev(estimation_list, average)
        coef_variation = std_deviation / average
        error = math.fabs(Config.DATA_SET_SIZE - average) / Config.DATA_SET_SIZE
        with open(Config.EXPERIMENT_RESULTS_FILE_PATH, "a+") as file:
            file.write("Coeficiente de Variação,Estimativa Média,Erro da Média,Duração Total,Total de Conexões,"
                       + os.linesep)
            file.write(str(coef_variation) + "," + str(average) + "," + str(error) + "," + str(total_duration)
                       + "," + str(total_connections) + "," + os.linesep)

    def write_experiment_details(self, additional_information=None):
        with open(Config.EXPERIMENT_DETAILS_FILE_PATH, "a+") as file:
            file.write("Limite da máquina de busca: " + str(Config.SEARCH_ENGINE_LIMIT) + os.linesep)
            file.write("Lista de palavras: " + Config.QUERY_POOL_FILE_PATH + os.linesep)
            if additional_information is not None:
                key_list = list(additional_information.keys())
                for key in key_list:
                    file.write(str(key) + ": " + str(additional_information[key]) + os.linesep)
