from urllib.request import urlopen
from threading import Thread, Lock
import json
import re
import os
import string

from abs_commom_api import AbsCommomApi
from config import Config


class CommomApi(AbsCommomApi):

	DOCUMENT_LIST_KEY = "docs"
	NUMBER_MATCHES_KEY = "numFound"
	RESPONSE_KEY = "response"
	LOG_FILE_PERMISSION = "a+"
	ENCODING = "utf-8"

	@property
	def download_count(self):
		return self.__download_count

	@download_count.setter
	def download_count(self, val):
		self.__download_count = val

	def __init__(self):
		self.download_count = 0;
		self.lock = Lock()

	def read_query_pool(self):
		query_pool = []
		with open(Config.QUERY_POOL_FILE_PATH) as archive:
			for line in archive:
				query_pool.append(line.rstrip("\n").rstrip("\r"))
		return query_pool

	def log(self, tag, content = ""):
		with open(Config.LOG_FILE_PATH, CommomApi.LOG_FILE_PERMISSION) as archive:
			archive.write(str(tag) + ": " + str(content) + os.linesep)

	def download_entire_data_set(self):
		dictionary = self.submit_query("*", 1000000, "*")
		return dictionary[CommomApi.DOCUMENT_LIST_KEY]

	def retrieve_number_matches(self, query):
		dictionary = self.submit_query(query, 1)
		return dictionary[CommomApi.NUMBER_MATCHES_KEY]

	def submit_query(self, query, limit, field_to_search = Config.FIELD_TO_SEARCH):
		url = Config.URL.replace(Config.LIMIT_MASK, str(limit))
		url = url.replace(Config.QUERY_MASK, str(query))
		url = url.replace(Config.FIELD_TO_SEARCH_MASK, field_to_search)
		response = urlopen(str(url))
		with self.lock:
			self.download_count += 1
		data = response.read().decode(CommomApi.ENCODING)
		dictionary = json.loads(data)
		return dictionary[CommomApi.RESPONSE_KEY]

	def download(self, query, limit = Config.SEARCH_ENGINE_LIMIT):
		dictionary = self.submit_query(query, limit)
		return dictionary[CommomApi.DOCUMENT_LIST_KEY]

	def execute_in_parallel(self, collection, callback):
		thread_list = []
		for item in collection:
			if(len(thread_list) > Config.THREAD_LIMIT):
				thread_list[0].join()
				del(thread_list[0])
			thread = Thread(target = callback, args = (item,))
			thread_list.append(thread)
			thread.start()
		for thread in thread_list:
			thread.join()

	def report_progress(self, progress, total):
		print("Progress: " + str(progress) + "/" + str(total))

	def log_result_experiment(self, estimation, duration, additional_information = {}):
		self.log("Estimation", estimation)
		self.log("Download count", self.download_count)
		self.log("Duration", duration)
		self.log("Search engine limit", Config.SEARCH_ENGINE_LIMIT)
		self.log("Query pool file", Config.QUERY_POOL_FILE_PATH)
		key_list = additional_information.keys()
		for key in key_list:
			self.log(key, additional_information[key])

	def extract_words(self, text):
		word = []
		word_dictionary = {}
		count = 0
		letter_or_hyphen_pattern = re.compile(r"[a-z]|[A-Z]|-")
		for character in text:
			if (letter_or_hyphen_pattern.match(character) is not None):
				word.append(character)
			else:
				word = str.join("", word)
				word = word.lower().strip("-").strip("-")
				if (len(word) > 0 and word not in word_dictionary):
					word_dictionary[word] = count
					count += 1
				word = []
		return list(word_dictionary.keys())