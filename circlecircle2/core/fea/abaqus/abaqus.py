from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.solver import Solver
from circlecircle2.core.fea.abaqus.parser.node_parser import NodeParser


class Abaqus(Solver):
    def __init__(self):
        self.logger = logger

        self.parse_keywords = {
            "*NODE": NodeParser(),
        }
        self.translate_keywords = {}
        self.not_support_keywords = []

        self.current_parser = None

    def reset(self):
        self.current_parser = None
        self.not_support_keywords.clear()

    def parse(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)

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
                                self.not_support_keywords.append(abaqus_keyword)
                                self.current_parser = None
                                continue
                        else:
                            if self.current_parser:
                                self.current_parser.parse(line_raw=line)

                except Exception as e:
                    raise e

            for not_support_keyword in self.not_support_keywords:
                self.logger.warning(f"ABAQUS not support keyword: {not_support_keyword}")

        else:
            self.logger.error(f"file path cannot be empty\n")

    def translate(self, file_path):
        pass
