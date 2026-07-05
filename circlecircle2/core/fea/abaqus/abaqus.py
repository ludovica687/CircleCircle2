from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.solver import Solver
from circlecircle2.core.fea.abaqus.parser.node_parser import NodeParser
from circlecircle2.core.fea.abaqus.translator.node_translator import NodeTranslator


class Abaqus(Solver):
    def __init__(self):
        self.logger = logger

        self.parse_keywords = {
            "*NODE": NodeParser(),
        }
        self.translate_keywords = {
            "*NODE": NodeTranslator(),
        }
        self.not_support_keywords = set()

        self.current_parser = None
        self.current_translator = None

    def reset(self):
        self.not_support_keywords.clear()

        self.current_parser = None
        self.current_translator = None

    def parse(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        version = kwargs.get("version", args[1] if len(args) > 1 else None)

        if file_path:
            with open(file=file_path, mode="r", encoding="utf-8", errors="ignore") as f:
                try:
                    for line in f:
                        if not line or line.startswith("**"):
                            continue

                        if line.startswith("*") and (not line.startswith("**")):
                            abaqus_keyword = line.split(",")[0].strip().upper()

                            if abaqus_keyword in self.parse_keywords:
                                self.current_parser = self.parse_keywords[abaqus_keyword]
                                continue
                            else:
                                self.not_support_keywords.add(abaqus_keyword)
                                self.current_parser = None
                                continue
                        else:
                            if self.current_parser:
                                self.current_parser.parse(line_raw=line, version=version)

                except Exception as e:
                    raise e

            for not_support_keyword in self.not_support_keywords:
                self.logger.warning(f"ABAQUS WARNING: not support keyword: {not_support_keyword}")

        else:
            self.logger.error(f"ABAQUS PARSER ERROR: file path cannot be empty\n")

    def translate(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        version = kwargs.get("version", args[1] if len(args) > 1 else None)

        if file_path:
            for key, translator in self.translate_keywords.items():
                self.current_translator = translator
                self.current_translator.translate(version=version)

            self.logger.info(f"ABAQUS translation finished")

        else:
            self.logger.error(f"ABAQUS TRANSLATOR ERROR: file path cannot be empty\n")
