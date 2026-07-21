from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.section_shell import SectionShell


class SectionShellParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            secid_raw = line_raw[0:10].strip()
            elform_raw = line_raw[10:20].strip()
            shrf_raw = line_raw[20:30].strip()
            nip_raw = line_raw[30:40].strip()

            self.temp.append(secid_raw)
            self.temp.append(elform_raw)
            self.temp.append(shrf_raw)
            self.temp.append(nip_raw)
            self.line_number = 1

            return

        if self.line_number == 1:
            secid_raw = self.temp[0]
            elform_raw = self.temp[1]
            shrf_raw = self.temp[2]
            nip_raw = self.temp[3]

            t1_raw = line_raw[0:10].strip()
            t2_raw = line_raw[10:20].strip()
            t3_raw = line_raw[20:30].strip()
            t4_raw = line_raw[30:40].strip()

            if len(secid_raw) > 0:
                secid = self.dataframe.parameter[secid_raw[1:]].value if secid_raw.startswith("&") else int(secid_raw)
            else:
                secid = 0

            if len(elform_raw) > 0:
                elform = self.dataframe.parameter[elform_raw[1:]].value if elform_raw.startswith("&") else int(
                    elform_raw)
            else:
                elform = 0

            if len(shrf_raw) > 0:
                shrf = self.dataframe.parameter[shrf_raw[1:]].value if shrf_raw.startswith("&") else float(shrf_raw)
            else:
                shrf = 0.833

            if len(nip_raw) > 0:
                nip = self.dataframe.parameter[nip_raw[1:]].value if nip_raw.startswith("&") else int(nip_raw)
            else:
                nip = 5

            t1 = t1_raw[1:] if t1_raw.startswith("&") else float(t1_raw)
            t2 = t2_raw[1:] if t2_raw.startswith("&") else float(t2_raw)
            t3 = t3_raw[1:] if t3_raw.startswith("&") else float(t3_raw)
            t4 = t4_raw[1:] if t4_raw.startswith("&") else float(t4_raw)

            self.dataframe.section_shell[secid] = SectionShell(
                uid=secid,
                elform=elform,
                shrf=shrf,
                nip=nip,
                t1=t1,
                t2=t2,
                t3=t3,
                t4=t4,
            )

            self.reset()

            return

