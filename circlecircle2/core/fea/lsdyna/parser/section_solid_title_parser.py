from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.section_solid import SectionSolid


class SectionSolidTitleParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            name_raw = line_raw.strip()

            self.temp.append(name_raw)

            self.line_number = 1

            return

        if self.line_number == 1:
            name_raw = self.temp[0]
            secid_raw = line_raw[0:10].strip()
            elform_raw = line_raw[10:20].strip()

            name = name_raw
            secid = secid_raw[1:] if secid_raw.startswith("&") else int(secid_raw)
            elform = elform_raw[1:] if elform_raw.startswith("&") else int(elform_raw)

            self.dataframe.section_solid[secid] = SectionSolid(uid=secid,
                                                               elform=elform,
                                                               name=name)

            self.reset()

            return

