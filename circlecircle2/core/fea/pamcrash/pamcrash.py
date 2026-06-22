from circlecircle2.core.fea.solver import Solver


class PamCrash(Solver):
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def parse(self, file_path):
        print(f"pamcrash parse")

    def translate(self, file_path):
        print(f"pamcrash translate")
