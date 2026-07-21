from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.solver import Solver
from circlecircle2.core.fea.pamcrash.parser.node_parser import NodeParser
from circlecircle2.core.fea.pamcrash.translator.user_head_note_translator import UserHeadNoteTranslator
from circlecircle2.core.fea.pamcrash.translator.node_translator import NodeTranslator
from circlecircle2.core.fea.pamcrash.translator.shell_translator import ShellTranslator
from circlecircle2.core.fea.pamcrash.translator.solid_translator import SolidTranslator
from circlecircle2.core.fea.pamcrash.translator.part_translator import PartTranslator
from circlecircle2.core.fea.pamcrash.translator.material_translator import MaterialTranslator
from circlecircle2.core.fea.pamcrash.translator.material_mapping_translator import MaterialMappingTranslator
from circlecircle2.core.fea.pamcrash.translator.funct_translator import FunctTranslator
from circlecircle2.core.fea.pamcrash.translator.funct_mapping_translator import FunctMappingTranslator


class PamCrash(Solver):
    def __init__(self):
        self.logger = logger

        self.parse_keywords = {
            "NODE": NodeParser(),
        }
        self.translate_keywords = {
            "note": UserHeadNoteTranslator(),
            "NODE": NodeTranslator(),
            "SHELL": ShellTranslator(),
            "SOLID": SolidTranslator(),
            "PART": PartTranslator(),
            "MATER": MaterialTranslator(),
            "FUNCT": FunctTranslator(),
        }
        self.translate_keywords_mapping = {
            "note": UserHeadNoteTranslator(),
            "NODE": NodeTranslator(),
            "SHELL": ShellTranslator(),
            "SOLID": SolidTranslator(),
            "PART": PartTranslator(),
            "MATER": MaterialMappingTranslator(),
            "FUNCT": FunctMappingTranslator(),
        }

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

    def translate(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        version = kwargs.get("version", args[1] if len(args) > 1 else None)
        material_mapping = kwargs.get("material_mapping", args[2] if len(args) > 2 else None)
        material_mapping_file_path = kwargs.get("material_mapping_file_path", args[3] if len(args) > 3 else None)

        if file_path:
            if material_mapping:
                for key, translator in self.translate_keywords_mapping.items():
                    self.current_translator = translator

                    if key == "MATER":
                        self.current_translator.translate(version=version,
                                                          material_mapping_file_path=material_mapping_file_path)
                    else:
                        self.current_translator.translate(version=version)
            else:
                for key, translator in self.translate_keywords.items():
                    self.current_translator = translator
                    self.current_translator.translate(version=version)

            self.logger.info(f"PAMCRASH translation finished")

        else:
            self.logger.error(f"PAMCRASH TRANSLATOR ERROR: file path cannot be empty\n")
