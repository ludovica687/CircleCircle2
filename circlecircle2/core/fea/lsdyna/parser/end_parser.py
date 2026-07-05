from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.end import End


class EndParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        self.dataframe.end[0] = "reserved"

        self.reset()

