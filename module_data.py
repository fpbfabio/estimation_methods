import abc


class AbsData(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def identifier(self):
        pass

    @property
    @abc.abstractmethod
    def content(self):
        pass


class Data(AbsData):
    def __init__(self, identifier, content):
        self.__identifier = identifier
        self.__content = content

    @property
    def identifier(self):
        return self.__identifier

    @property
    def content(self):
        return self.__content
