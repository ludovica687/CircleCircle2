from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.mat_elastic import MatElastic


class MatElasticParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        mid_raw = line_raw[0:10].strip()
        rho_raw = line_raw[10:20].strip()
        e_raw = line_raw[20:30].strip()
        pr_raw = line_raw[30:40].strip()
        da_raw = line_raw[40:50].strip()
        db_raw = line_raw[50:60].strip()
        k_raw = line_raw[60:70].strip()

        mid = self.dataframe.parameter[mid_raw[1:]].value if mid_raw.startswith("&") else int(mid_raw)
        rho = self.dataframe.parameter[rho_raw[1:]].value if rho_raw.startswith("&") else float(rho_raw)
        e = self.dataframe.parameter[e_raw[1:]].value if e_raw.startswith("&") else float(e_raw)
        pr = self.dataframe.parameter[pr_raw[1:]].value if pr_raw.startswith("&") else float(pr_raw)

        if len(da_raw) > 0:
            da = self.dataframe.parameter[da_raw[1:]].value if da_raw.startswith("&") else float(da_raw)
        else:
            da = 0

        if len(db_raw) > 0:
            db = self.dataframe.parameter[db_raw[1:]].value if db_raw.startswith("&") else float(db_raw)
        else:
            db = 0

        if len(k_raw) > 0:
            k = self.dataframe.parameter[k_raw[1:]].value if k_raw.startswith("&") else float(k_raw)
        else:
            k = 0

        self.dataframe.material[mid] = MatElastic(uid=mid,
                                                  rho=rho,
                                                  e=e,
                                                  pr=pr,
                                                  da=da,
                                                  db=db,
                                                  k=k)

        self.dataframe.storge_material_id.append(mid)

        self.reset()

        return

