from circlecircle2.core.fea.translator import Translator
import time


class UserHeadNoteTranslator(Translator):
    def __init__(self):
        super().__init__()

        self.version = {
            "2020": self._2020,
        }

    def translate(self, version):
        try:
            if version in self.version:
                self.version[version]()

        except Exception as e:
            raise Exception(f"PAMCRASH UserHeadNoteTranslator ERROR: {e}") from e

    def _2020(self):
        output_storge = self.dataframe.output_storge.setdefault("USER_NOTE", [])

        current_time = time.ctime()

        output_storge.append(f"$# this file was translated by software: CircleCircle2, {current_time}\n"
                             f"$# software isn't human, it can make mistakes\n"
                             f"$# \n"
                             f"$# \n")
