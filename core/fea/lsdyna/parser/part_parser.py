from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.part import Part


class PartParser(Parser):
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
            pid_raw = line_raw[0:10].strip()
            secid_raw = line_raw[10:20].strip()
            mid_raw = line_raw[20:30].strip()
            eosid_raw = line_raw[30:40].strip()
            hgid_raw = line_raw[40:50].strip()

            name = name_raw

            if len(pid_raw) > 0:
                pid = self.dataframe.parameter[pid_raw[1:]].value if pid_raw.startswith("&") else int(pid_raw)
            else:
                pid = 0

            if len(secid_raw) > 0:
                secid = self.dataframe.parameter[secid_raw[1:]].value if secid_raw.startswith("&") else int(secid_raw)
            else:
                secid = 0

            if len(mid_raw) > 0:
                mid = self.dataframe.parameter[mid_raw[1:]].value if mid_raw.startswith("&") else int(mid_raw)
            else:
                mid = 0

            if len(eosid_raw) > 0:
                eosid = self.dataframe.parameter[eosid_raw[1:]].value if eosid_raw.startswith("&") else int(eosid_raw)
            else:
                eosid = 0

            if len(hgid_raw) > 0:
                hgid = self.dataframe.parameter[hgid_raw[1:]].value if hgid_raw.startswith("&") else int(hgid_raw)
            else:
                hgid = 0

            self.dataframe.part[pid] = Part(name, pid, secid, mid, eosid, hgid)
            self.dataframe.part_tensor.append([pid, secid, mid, eosid, hgid])

            self.reset()

            return

