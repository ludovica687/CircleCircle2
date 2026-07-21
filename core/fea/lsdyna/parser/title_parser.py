from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.title import Title


class TitleParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        context = line_raw.strip()

        uid = len(self.dataframe.title) + 1
        self.dataframe.title[uid] = Title(uid=uid,
                                          context=context)

        return