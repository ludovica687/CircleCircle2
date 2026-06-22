from abc import ABC, abstractmethod


class Solver(ABC):
    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def parse(self, file_path):
        pass

    @abstractmethod
    def translate(self, file_path):
        pass
