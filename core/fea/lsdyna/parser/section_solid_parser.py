from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.section_solid import SectionSolid


class SectionSolidParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        secid_raw = line_raw[0:10].strip()
        elform_raw = line_raw[10:20].strip()

        secid = self.dataframe.parameter[secid_raw[1:]].value if secid_raw.startswith("&") else int(secid_raw)
        elform = self.dataframe.parameter[elform_raw[1:]].value if elform_raw.startswith("&") else int(elform_raw)

        self.dataframe.section_solid[secid] = SectionSolid(uid=secid,
                                                           elform=elform)

        self.reset()

        return

