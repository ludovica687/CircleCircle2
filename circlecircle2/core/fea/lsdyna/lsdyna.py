from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.solver import Solver
from circlecircle2.core.fea.lsdyna.parser.node_parser import NodeParser


class LsDyna(Solver):
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

                        if not line or line.startswith("$"):
                            continue

                        if line.startswith("*"):
                            dyna_keyword = line.split()[0].strip().upper()

                            if dyna_keyword in self.parse_keywords:
                                self.current_parser = self.parse_keywords[dyna_keyword]
                                continue
                            else:
                                self.not_support_keywords.append(dyna_keyword)
                                self.current_parser = None
                                continue

                        elif line.strip().strip("-") == "BEGIN PGP MESSAGE":
                            dyna_keyword = "BEGIN PGP MESSAGE"

                            if dyna_keyword in self.parse_keywords:
                                self.current_parser = self.parse_keywords[dyna_keyword]
                                continue

                        elif line.strip().strip("-") == "END PGP MESSAGE":
                            self.current_parser = None
                            continue

                        else:
                            if self.current_parser is not None:
                                self.current_parser.parse(line_raw=line)

                except Exception as e:
                    raise e

            for not_support_keyword in self.not_support_keywords:
                self.logger.warning(f"Ls-Dyna not support keywords: {not_support_keyword}")

        else:
            self.logger.error(f"file_path cannot be empty\n")

    def translate(self, file_path):
        print(f"lsdyna translate")
