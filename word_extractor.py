""""
This is the module that provides an abstract interface for a
class used to extract the words of a text.
"""
from abc import ABCMeta, abstractmethod
import re


class AbsWordExtractor(metaclass=ABCMeta):
    """
    Helper class for extracting the words of a text.
    """

    @abstractmethod
    def extract_words(self, text):
        """
        Returns the words in the text as a list.
        """
        pass


class WordExtractor(AbsWordExtractor):

    def extract_words(self, text):
        word = []
        word_dictionary = {}
        count = 0
        letter_or_hyphen_pattern = re.compile(r"[a-z]|[A-Z]|-")
        for character in text:
            if letter_or_hyphen_pattern.match(character) is not None:
                word.append(character)
            else:
                word = str.join("", word)
                word = word.lower().strip("-").strip("-")
                if len(word) > 0 and word not in word_dictionary:
                    word_dictionary[word] = count
                    count += 1
                word = []
        return list(word_dictionary.keys())
