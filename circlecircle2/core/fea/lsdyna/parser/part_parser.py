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
            pid = pid_raw[1:] if pid_raw.startswith("&") else int(pid_raw)
            secid = secid_raw[1:] if secid_raw.startswith("&") else int(secid_raw)
            mid = mid_raw[1:] if mid_raw.startswith("&") else int(mid_raw)

            if len(eosid_raw) > 0:
                eosid = eosid_raw[1:] if eosid_raw.startswith("&") else int(eosid_raw)
            else:
                eosid = 0

            hgid = hgid_raw[1:] if hgid_raw.startswith("&") else int(hgid_raw)

            self.dataframe.part[pid] = Part(name, pid, secid, mid, eosid, hgid)
            self.dataframe.part_tensor.append([pid, secid, mid, eosid, hgid])

            self.reset()

            return

