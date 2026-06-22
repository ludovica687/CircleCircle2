from circlecircle2.core.fea.dataframe import dataframe
from abc import ABC, abstractmethod


class Parser:
    def __init__(self):
        self.dataframe = dataframe

    @abstractmethod
    def parse(self, raw_line):
        pass
