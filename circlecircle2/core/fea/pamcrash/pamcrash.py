from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.solver import Solver
from circlecircle2.core.fea.pamcrash.parser.node_parser import NodeParser


class PamCrash(Solver):
    def __init__(self):
        self.logger = logger

        self.parse_keywords = {
            "NODE": NodeParser(),
        }
        self.translate_keywords = {}
        self.not_support_keywords = set()

        self.current_parser = None

    def reset(self):
        self.current_parser = None
        self.not_support_keywords.clear()

    def parse(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        version = kwargs.get("version", args[1] if len(args) > 1 else None)

        if file_path:
            with open(file=file_path, mode="r", encoding="utf-8", errors="ignore") as f:
                try:
                    for line in f:
                        if (len(line.strip()) == 0) or line.startswith("$"):
                            continue
                        else:
                            line_raw_split = line.split("/")
                            line_raw_length = len(line_raw_split)

                            if line_raw_length == 2:
                                pamcrash_keyword = line_raw_split[0].strip().upper()

                                if pamcrash_keyword in self.parse_keywords:
                                    self.current_parser = self.parse_keywords[pamcrash_keyword]
                                    self.current_parser.parse(line_raw=line, version=version)
                                    continue
                                else:
                                    self.not_support_keywords.add(pamcrash_keyword)
                                    self.current_parser = None
                                    continue

                            elif line_raw_length == 1 and (self.current_parser is not None):
                                self.current_parser.parse(line_raw=line, version=version)
                                continue

                except Exception as e:
                    raise e

            for not_support_keyword in self.not_support_keywords:
                self.logger.warning(f"Pam-Crash not support keyword: {not_support_keyword}")

        else:
            self.logger.error(f"file path cannot be empty\n")

    def translate(self, file_path):
        print(f"pamcrash translate")
