from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.define_curve import DefineCurve


class DefineCurveTitleParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

        self.current_curve_id = None

    def _12p0(self, line_raw):
        if self.line_number == 0:
            name_raw = line_raw.strip()

            self.temp.append(name_raw)

            self.line_number = 1

            return

        if self.line_number == 1:
            name_raw = self.temp[0]
            lcid_raw = line_raw[0:10].strip()
            sidr_raw = line_raw[10:20].strip()
            sfa_raw = line_raw[20:30].strip()
            sfo_raw = line_raw[30:40].strip()
            offa_raw = line_raw[40:50].strip()
            offo_raw = line_raw[50:60].strip()
            dattyp_raw = line_raw[60:70].strip()
            lcint_raw = line_raw[70:80].strip()

            name = name_raw
            lcid = self.dataframe.parameter[lcid_raw[1:]].value if lcid_raw.startswith("&") else int(lcid_raw)

            if len(sidr_raw) > 0:
                sidr = self.dataframe.parameter[sidr_raw[1:]].value if sidr_raw.startswith("&") else int(sidr_raw)
            else:
                sidr = 0

            if len(sfa_raw) > 0:
                sfa = self.dataframe.parameter[sfa_raw[1:]].value if sfa_raw.startswith("&") else float(sfa_raw)
            else:
                sfa = 1.0

            if len(sfo_raw) > 0:
                sfo = self.dataframe.parameter[sfo_raw[1:]].value if sfo_raw.startswith("&") else float(sfo_raw)
            else:
                sfo = 1.0

            if len(offa_raw) > 0:
                offa = self.dataframe.parameter[offa_raw[1:]].value if offa_raw.startswith("&") else float(offa_raw)
            else:
                offa = 0.0

            if len(offo_raw) > 0:
                offo = self.dataframe.parameter[offo_raw[1:]].value if offo_raw.startswith("&") else float(offo_raw)
            else:
                offo = 0.0

            if len(dattyp_raw) > 0:
                dattyp = self.dataframe.parameter[dattyp_raw[1:]].value if dattyp_raw.startswith("&") else int(
                    dattyp_raw)
            else:
                dattyp = 0

            if len(lcint_raw) > 0:
                lcint = self.dataframe.parameter[lcint_raw[1:]].value if lcint_raw.startswith("&") else int(lcint_raw)
            else:
                lcint = 0

            self.dataframe.define_curve[lcid] = DefineCurve(uid=lcid,
                                                            sidr=sidr,
                                                            sfa=sfa,
                                                            sfo=sfo,
                                                            offa=offa,
                                                            offo=offo,
                                                            dattyp=dattyp,
                                                            lcint=lcint,
                                                            name=name)

            self.current_curve_id = lcid

            self.line_number = 2

            return

        if (self.line_number != 0) and (self.line_number != 1):
            a1_raw = line_raw[0:20].strip()
            o1_raw = line_raw[20:40].strip()

            a1 = self.dataframe.parameter[a1_raw[1:]].value if a1_raw.startswith("&") else float(a1_raw)
            o1 = self.dataframe.parameter[o1_raw[1:]].value if o1_raw.startswith("&") else float(o1_raw)

            self.dataframe.define_curve[self.current_curve_id].a1.append(a1)
            self.dataframe.define_curve[self.current_curve_id].o1.append(o1)

            return
