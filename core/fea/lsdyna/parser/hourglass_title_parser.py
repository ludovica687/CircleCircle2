from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.hourglass import Hourglass


class HourglassTitleParser(Parser):
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
            hgid_raw = line_raw[0:10].strip()
            ihq_raw = line_raw[10:20].strip()
            qm_raw = line_raw[20:30].strip()
            ibq_raw = line_raw[30:40].strip()
            q1_raw = line_raw[40:50].strip()
            q2_raw = line_raw[50:60].strip()
            qb_raw = line_raw[60:70].strip()
            qw_raw = line_raw[70:80].strip()

            name = name_raw
            hgid = self.dataframe.parameter[hgid_raw[1:]].value if hgid_raw.startswith("&") else int(hgid_raw)
            ihq = self.dataframe.parameter[ihq_raw[1:]].value if ihq_raw.startswith("&") else int(ihq_raw)
            qm = self.dataframe.parameter[qm_raw[1:]].value if qm_raw.startswith("&") else float(qm_raw)
            ibq = self.dataframe.parameter[ibq_raw[1:]].value if ibq_raw.startswith("&") else int(ibq_raw)
            q1 = self.dataframe.parameter[q1_raw[1:]].value if q1_raw.startswith("&") else float(q1_raw)
            q2 = self.dataframe.parameter[q2_raw[1:]].value if q2_raw.startswith("&") else float(q2_raw)
            qb = self.dataframe.parameter[qb_raw[1:]].value if qb_raw.startswith("&") else float(qb_raw)
            qw = self.dataframe.parameter[qw_raw[1:]].value if qw_raw.startswith("&") else float(qw_raw)

            self.dataframe.hourglass[hgid] = Hourglass(uid=hgid,
                                                       ihq=ihq,
                                                       qm=qm,
                                                       ibq=ibq,
                                                       q1=q1,
                                                       q2=q2,
                                                       qb=qb,
                                                       qw=qw,
                                                       name=name)

            self.reset()

        return
