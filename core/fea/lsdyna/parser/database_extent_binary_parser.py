from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.database_extent_binary import DatabaseExtentBinary


class DatabaseExtentBinaryParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            neiph_raw = line_raw[0:10].strip()
            neips_raw = line_raw[10:20].strip()
            maxint_raw = line_raw[20:30].strip()
            strflg_raw = line_raw[30:40].strip()
            sigflg_raw = line_raw[40:50].strip()
            epsflg_raw = line_raw[50:60].strip()
            rltflg_raw = line_raw[60:70].strip()
            engflg_raw = line_raw[70:80].strip()

            self.temp.append(neiph_raw)
            self.temp.append(neips_raw)
            self.temp.append(maxint_raw)
            self.temp.append(strflg_raw)
            self.temp.append(sigflg_raw)
            self.temp.append(epsflg_raw)
            self.temp.append(rltflg_raw)
            self.temp.append(engflg_raw)

            self.line_number = 1

            return

        if self.line_number == 1:
            neiph_raw = self.temp[0]
            neips_raw = self.temp[1]
            maxint_raw = self.temp[2]
            strflg_raw = self.temp[3]
            sigflg_raw = self.temp[4]
            epsflg_raw = self.temp[5]
            rltflg_raw = self.temp[6]
            engflg_raw = self.temp[7]

            cmpflg_raw = line_raw[0:10].strip()
            ieverp_raw = line_raw[10:20].strip()
            beamip_raw = line_raw[20:30].strip()
            dcomp_raw = line_raw[30:40].strip()
            shge_raw = line_raw[40:50].strip()
            stssz_raw = line_raw[50:60].strip()
            n3thdt_raw = line_raw[60:70].strip()
            ialemat_raw = line_raw[70:80].strip()

            if len(neiph_raw) > 0:
                neiph = self.dataframe.parameter[neiph_raw[1:]] if neiph_raw.startswith("&") else float(neiph_raw)
            else:
                neiph = 0

            if len(neips_raw) > 0:
                neips = self.dataframe.parameter[neips_raw[1:]] if neips_raw.startswith("&") else float(neips_raw)
            else:
                neips = 0

            if len(maxint_raw) > 0:
                maxint = self.dataframe.parameter[maxint_raw[1:]] if maxint_raw.startswith("&") else float(maxint_raw)
            else:
                maxint = 0

            if len(strflg_raw) > 0:
                strflg = self.dataframe.parameter[strflg_raw[1:]] if strflg_raw.startswith("&") else float(strflg_raw)
            else:
                strflg = 0

            if len(sigflg_raw) > 0:
                sigflg = self.dataframe.parameter[sigflg_raw[1:]] if sigflg_raw.startswith("&") else float(sigflg_raw)
            else:
                sigflg = 0

            if len(epsflg_raw) > 0:
                epsflg = self.dataframe.parameter[epsflg_raw[1:]] if epsflg_raw.startswith("&") else float(epsflg_raw)
            else:
                epsflg = 0

            if len(rltflg_raw) > 0:
                rltflg = self.dataframe.parameter[rltflg_raw[1:]] if rltflg_raw.startswith("&") else float(rltflg_raw)
            else:
                rltflg = 0

            if len(engflg_raw) > 0:
                engflg = self.dataframe.parameter[engflg_raw[1:0]] if engflg_raw.startswith("&") else float(engflg_raw)
            else:
                engflg = 0

            if len(cmpflg_raw) > 0:
                cmpflg = self.dataframe.parameter[cmpflg_raw[1:]] if cmpflg_raw.startswith("&") else float(cmpflg_raw)
            else:
                cmpflg = 0

            if len(ieverp_raw) > 0:
                ieverp = self.dataframe.parameter[ieverp_raw[1:]] if ieverp_raw.startswith("&") else float(ieverp_raw)
            else:
                ieverp = 0

            if len(beamip_raw) > 0:
                beamip = self.dataframe.parameter[beamip_raw[1:]] if beamip_raw.startswith("&") else float(beamip_raw)
            else:
                beamip = 0

            if len(dcomp_raw) > 0:
                dcomp = self.dataframe.parameter[dcomp_raw[1:]] if dcomp_raw.startswith("&") else float(dcomp_raw)
            else:
                dcomp = 0

            if len(shge_raw) > 0:
                shge = self.dataframe.parameter[shge_raw[1:]] if shge_raw.startswith("&") else float(shge_raw)
            else:
                shge = 0

            if len(stssz_raw) > 0:
                stssz = self.dataframe.parameter[stssz_raw[1:]] if stssz_raw.startswith("&") else float(stssz_raw)
            else:
                stssz = 0

            if len(n3thdt_raw) > 0:
                n3thdt = self.dataframe.parameter[n3thdt_raw[1:]] if n3thdt_raw.startswith("&") else float(n3thdt_raw)
            else:
                n3thdt = 0

            if len(ialemat_raw) > 0:
                ialemat = self.dataframe.parameter[ialemat_raw[1:]] if ialemat_raw.startswith("&") else float(ialemat_raw)
            else:
                ialemat = 0

            uid = len(self.dataframe.database_extent_binary) + 1

            self.dataframe.database_extent_binary[uid] = DatabaseExtentBinary(uid=uid,
                                                                              neiph=neiph,
                                                                              neips=neips,
                                                                              maxint=maxint,
                                                                              strflg=strflg,
                                                                              sigflg=sigflg,
                                                                              epsflg=epsflg,
                                                                              rltflg=rltflg,
                                                                              engflg=engflg,
                                                                              cmpflg=cmpflg,
                                                                              ieverp=ieverp,
                                                                              beamip=beamip,
                                                                              dcomp=dcomp,
                                                                              shge=shge,
                                                                              stssz=stssz,
                                                                              n3thdt=n3thdt,
                                                                              ialemat=ialemat)

            self.reset()

            return