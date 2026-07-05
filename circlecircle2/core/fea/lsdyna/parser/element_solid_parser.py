from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.element_solid import ElementSolid


class ElementSolidParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            uid_raw = line_raw[0:8].strip()
            pid_raw = line_raw[8:16].strip()

            self.temp.append(uid_raw)
            self.temp.append(pid_raw)

            self.line_number = 1

            return

        if self.line_number == 1:
            uid_raw = self.temp[0]
            pid_raw = self.temp[1]
            n1_raw = line_raw[0:8].strip()
            n2_raw = line_raw[8:16].strip()
            n3_raw = line_raw[16:24].strip()
            n4_raw = line_raw[24:32].strip()
            n5_raw = line_raw[32:40].strip()
            n6_raw = line_raw[40:48].strip()
            n7_raw = line_raw[48:56].strip()
            n8_raw = line_raw[56:64].strip()

            uid = uid_raw[1:] if uid_raw.startswith("&") else int(uid_raw)
            pid = pid_raw[1:] if pid_raw.startswith("&") else int(pid_raw)
            n1 = n1_raw[1:] if n1_raw.startswith("&") else int(n1_raw)
            n2 = n2_raw[1:] if n2_raw.startswith("&") else int(n2_raw)
            n3 = n3_raw[1:] if n3_raw.startswith("&") else int(n3_raw)
            n4 = n4_raw[1:] if n4_raw.startswith("&") else int(n4_raw)
            n5 = n5_raw[1:] if n5_raw.startswith("&") else int(n5_raw)
            n6 = n6_raw[1:] if n6_raw.startswith("&") else int(n6_raw)
            n7 = n7_raw[1:] if n7_raw.startswith("&") else int(n7_raw)
            n8 = n8_raw[1:] if n8_raw.startswith("&") else int(n8_raw)

            self.dataframe.element_solid[uid] = ElementSolid(uid=uid,
                                                             pid=pid,
                                                             n1=n1,
                                                             n2=n2,
                                                             n3=n3,
                                                             n4=n4,
                                                             n5=n5,
                                                             n6=n6,
                                                             n7=n7,
                                                             n8=n8)
            self.dataframe.element_solid_tensor.append([uid, pid, n1, n2, n3, n4, n5, n6, n7, n8])

            solid_surface_tensor = self.dataframe.element_solid[uid].surface_tensor
            self.dataframe.element_solid_surface_tensor.extend(solid_surface_tensor)

            self.reset()

            return
