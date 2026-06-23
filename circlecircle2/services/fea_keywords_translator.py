import os
from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.dataframe import dataframe
from circlecircle2.core.fea.lsdyna.lsdyna import LsDyna
from circlecircle2.core.fea.abaqus.abaqus import Abaqus
from circlecircle2.core.fea.pamcrash.pamcrash import PamCrash


class FeaKeywordsTranslator:
    def __init__(self):
        self.logger = logger

        self.dataframe = dataframe

    def reset(self):
        self.dataframe.reset()

    def translate(self, *args, **kwargs):
        """
        :param file_path: target file full path
        :param solver1: parser solver
        :param version1:
        :param solver2: translate solver
        :param version2:
        :return:
        """
        self.reset()

        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        solver1 = kwargs.get("solver1", args[1] if len(args) > 1 else None)
        version1 = kwargs.get("version1", args[2] if len(args) > 2 else None)
        solver2 = kwargs.get("solver2", args[3] if len(args) > 3 else None)
        version2 = kwargs.get("version2", args[4] if len(args) > 4 else None)

        folder = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        file_name, file_extension = os.path.splitext(basename)

        if solver1 == solver2:
            self.logger.error(f"solver1 {solver1} and solver2 {solver2} must be different")

        else:
            if solver1 == "lsdyna":
                if version1 in ["12.0", "13.0"]:
                    self._lsdyna(version=version1, file_path=file_path, mode="parse")
                else:
                    self.logger.error(f"current ls-dyna version {version1} not supported")

            elif solver1 == "abaqus":
                if version1 in ["6.14"]:
                    self._abaqus(version=version1, file_path=file_path, mode="parse")
                else:
                    self.logger.error(f"current abaqus version {version1} not supported")

            elif solver1 == "pamcrash":
                if version1 in ["2020"]:
                    self._pamcrash(version=version1, file_path=file_path, mode="parse")
                else:
                    self.logger.error(f"current pamcrash version {version1} not supported")

            if solver2 == "lsdyna":
                if version2 in ["12.0", "13.0"]:
                    self._lsdyna(version=version2, file_path=file_path, mode="translate")
                else:
                    self.logger.error(f"current ls-dyna version {version2} not supported")

            elif solver2 == "abaqus":
                if version2 in ["6.14"]:
                    self._abaqus(version=version2, file_path=file_path, mode="translate")
                else:
                    self.logger.error(f"current abaqus version {version2} not supported")

            elif solver2 == "pamcrash":
                if version2 in ["2020"]:
                    self._pamcrash(version=version2, file_path=file_path, mode="translate")
                else:
                    self.logger.error(f"current pamcrash version {version2} not supported")

    def _lsdyna(self, version, file_path, mode):
        lsdyna = LsDyna()

        if mode == "parse":
            lsdyna.parse(file_path=file_path)

        elif mode == "translate":
            self.logger.debug(f"lsdyna translate mode, version: {version}, file_path: {file_path}")

    def _abaqus(self, version, file_path, mode):
        abaqus = Abaqus()

        if mode == "parse":
            abaqus.parse(file_path=file_path)

        elif mode == "translate":
            self.logger.debug(f"abaqus translate mode, version: {version}, file_path: {file_path}")

    def _pamcrash(self, version, file_path, mode):
        pamcrash = PamCrash()

        if mode == "parse":
            pamcrash.parse(file_path=file_path)

        elif mode == "translate":
            self.logger.debug(f"pamcrash translate mode, version: {version}, file_path: {file_path}")


fea_keywords_translator = FeaKeywordsTranslator()


if __name__ == '__main__':
    # file_path = r"C:\Users\jiand\Downloads\Test_Data\test_model.k"
    # file_path = r"C:\Users\jiand\Downloads\Test_Data\test_model.inp"
    file_path = r"C:\Users\jiand\Downloads\Test_Data\test_.pc"

    fea_keywords_translator.translate(file_path=file_path,
                                      solver1="pamcrash",
                                      version1="2020",
                                      solver2="abaqus",
                                      version2="7.14")
    print(f"Node Length is {len(fea_keywords_translator.dataframe.node)}")
