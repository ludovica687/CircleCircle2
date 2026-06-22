import os
from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.dataframe import dataframe
from circlecircle2.core.fea.lsdyna.lsdyna import LsDyna


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

        if solver1 == "lsdyna":
            self._lsdyna(version=version1, file_path=file_path, mode="parse")
        elif solver1 == "abaqus":
            self._abaqus(version=version1, file_path=file_path, mode="parse")
        elif solver1 == "pamcrash":
            self._pamcrash(version=version1, file_path=file_path, mode="parse")

        if solver2 == "lsdyna":
            self._lsdyna(version=version2, file_path=file_path, mode="translate")
        elif solver2 == "abaqus":
            self._abaqus(version=version2, file_path=file_path, mode="translate")
        elif solver2 == "pamcrash":
            self._pamcrash(version=version2, file_path=file_path, mode="translate")

    def _lsdyna(self, version, file_path, mode):
        lsdyna = LsDyna()

        if mode == "parse":
            lsdyna.parse(file_path=file_path)

        elif mode == "translate":
            self.logger.debug(f"lsdyna translate mode, version: {version}, file_path: {file_path}")

    def _abaqus(self, version, file_path, mode):
        if mode == "parse":
            self.logger.debug(f"abaqus parse mode, version: {version}, file_path: {file_path}")

        elif mode == "translate":
            self.logger.debug(f"abaqus translate mode, version: {version}, file_path: {file_path}")

    def _pamcrash(self, version, file_path, mode):

        if mode == "parse":
            self.logger.debug(f"pamcrash parse mode, version: {version}, file_path: {file_path}")

        elif mode == "translate":
            self.logger.debug(f"pamcrash translate mode, version: {version}, file_path: {file_path}")


fea_keywords_translator = FeaKeywordsTranslator()


if __name__ == '__main__':
    file_path = r"C:\Users\jiand\Downloads\Test_Data\test_model.k"

    fea_keywords_translator.translate(file_path=file_path,
                                      solver1="lsdyna",
                                      version1="12.0",
                                      solver2="abaqus",
                                      version2="6.14")
    print(f"Node Length is {len(fea_keywords_translator.dataframe.node)}")
