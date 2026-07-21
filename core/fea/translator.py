from circlecircle2.core.fea.dataframe import dataframe
from abc import ABC, abstractmethod


class Translator(ABC):
    def __init__(self):
        self.dataframe = dataframe

    @abstractmethod
    def translate(self, version):
        pass
