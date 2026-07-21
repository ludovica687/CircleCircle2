from circlecircle2.core.fea.dataframe import dataframe
from abc import ABC, abstractmethod

class Parser:
    def __init__(self):
        """
        self.version is a function mapping, must be define, like this:
        self.version = {
            "12.0": f1,
            "13.0": f2,
        }

        f1, f2, ... is a user define function to parse line raw data
        """
        self.dataframe = dataframe
        self.line_number = 0
        self.temp = []
        self.version = {}

    def reset(self):
        self.line_number = 0
        self.temp = []

    @abstractmethod
    def parse(self, line_raw, version):
        """
        :param line_raw: raw data
        :return: Node Object
        """

        try:
            if version in self.version:
                self.version[version](line_raw)

        except Exception as e:

            raise e
