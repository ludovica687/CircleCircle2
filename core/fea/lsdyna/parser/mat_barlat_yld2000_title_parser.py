from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.mat_barlat_yld2000 import MatBarlatYld2000


class MatBarlatYld2000TitleParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            name = line_raw.strip()

            self.temp.append(name)
            self.line_number = 1

            return

        if self.line_number == 1:
            mid_raw = line_raw[0:10].strip()
            rho_raw = line_raw[10:20].strip()
            e_raw = line_raw[20:30].strip()
            pr_raw = line_raw[30:40].strip()
            fit_raw = line_raw[40:50].strip()
            beta_raw = line_raw[50:60].strip()
            iter_raw = line_raw[60:70].strip()
            iscale_raw = line_raw[70:80].strip()

            self.temp.append(mid_raw)
            self.temp.append(rho_raw)
            self.temp.append(e_raw)
            self.temp.append(pr_raw)
            self.temp.append(fit_raw)
            self.temp.append(beta_raw)
            self.temp.append(iter_raw)
            self.temp.append(iscale_raw)

            self.line_number = 2

            return

        if self.line_number == 2:
            k_raw = line_raw[0:10].strip()
            e0_raw = line_raw[10:20].strip()
            n_raw = line_raw[20:30].strip()
            c_raw = line_raw[30:40].strip()
            p_raw = line_raw[40:50].strip()
            hard_raw = line_raw[50:60].strip()
            a_raw = line_raw[60:70].strip()

            self.temp.append(k_raw)
            self.temp.append(e0_raw)
            self.temp.append(n_raw)
            self.temp.append(c_raw)
            self.temp.append(p_raw)
            self.temp.append(hard_raw)
            self.temp.append(a_raw)

            self.line_number = 3

            return

        if self.line_number == 3:
            alpha1_raw = line_raw[0:10].strip()
            alpha2_raw = line_raw[10:20].strip()
            alpha3_raw = line_raw[20:30].strip()
            alpha4_raw = line_raw[30:40].strip()
            alpha5_raw = line_raw[40:50].strip()
            alpha6_raw = line_raw[50:60].strip()
            alpha7_raw = line_raw[60:70].strip()
            alpha8_raw = line_raw[70:80].strip()

            self.temp.append(alpha1_raw)
            self.temp.append(alpha2_raw)
            self.temp.append(alpha3_raw)
            self.temp.append(alpha4_raw)
            self.temp.append(alpha5_raw)
            self.temp.append(alpha6_raw)
            self.temp.append(alpha7_raw)
            self.temp.append(alpha8_raw)

            self.line_number = 4

            return

        if self.line_number == 4:
            aopt_raw = line_raw[0:10].strip()
            offang_raw = line_raw[10:20].strip()
            p4_raw = line_raw[20:30].strip()
            htflag_raw = line_raw[30:40].strip()
            hta_raw = line_raw[40:50].strip()
            htb_raw = line_raw[50:60].strip()
            htc_raw = line_raw[60:70].strip()
            htd_raw = line_raw[70:80].strip()

            self.temp.append(aopt_raw)
            self.temp.append(offang_raw)
            self.temp.append(p4_raw)
            self.temp.append(htflag_raw)
            self.temp.append(hta_raw)
            self.temp.append(htb_raw)
            self.temp.append(htc_raw)
            self.temp.append(htd_raw)

            self.line_number = 5

            return

        if self.line_number == 5:
            a1_raw = line_raw[30:40].strip()
            a2_raw = line_raw[40:50].strip()
            a3_raw = line_raw[50:60].strip()

            self.temp.append(a1_raw)
            self.temp.append(a2_raw)
            self.temp.append(a3_raw)

            self.line_number = 6

            return

        if self.line_number == 6:
            name_raw = self.temp[0]
            mid_raw = self.temp[1]
            rho_raw = self.temp[2]
            e_raw = self.temp[3]
            pr_raw = self.temp[4]
            fit_raw = self.temp[5]
            beta_raw = self.temp[6]
            iter_raw = self.temp[7]
            iscale_raw = self.temp[8]
            k_raw = self.temp[9]
            e0_raw = self.temp[10]
            n_raw = self.temp[11]
            c_raw = self.temp[12]
            p_raw = self.temp[13]
            hard_raw = self.temp[14]
            a_raw = self.temp[15]
            alpha1_raw = self.temp[16]
            alpha2_raw = self.temp[17]
            alpha3_raw = self.temp[18]
            alpha4_raw = self.temp[19]
            alpha5_raw = self.temp[20]
            alpha6_raw = self.temp[21]
            alpha7_raw = self.temp[22]
            alpha8_raw = self.temp[23]
            aopt_raw = self.temp[24]
            offang_raw = self.temp[25]
            p4_raw = self.temp[26]
            htflag_raw = self.temp[27]
            hta_raw = self.temp[28]
            htb_raw = self.temp[29]
            htc_raw = self.temp[30]
            htd_raw = self.temp[31]
            a1_raw = self.temp[32]
            a2_raw = self.temp[33]
            a3_raw = self.temp[34]

            v1_raw = line_raw[0:10].strip()
            v2_raw = line_raw[10:20].strip()
            v3_raw = line_raw[20:30].strip()
            d1_raw = line_raw[30:40].strip()
            d2_raw = line_raw[40:50].strip()
            d3_raw = line_raw[50:60].strip()
            usrfail_raw = line_raw[60:70].strip()

            name = name_raw
            mid = self.dataframe.parameter[mid_raw[1:]].value if mid_raw.startswith("&") else int(mid_raw)
            rho = self.dataframe.parameter[rho_raw[1:]].value if rho_raw.startswith("&") else float(rho_raw)
            e = self.dataframe.parameter[e_raw[1:]].value if e_raw.startswith("&") else float(e_raw)
            pr = self.dataframe.parameter[pr_raw[1:]].value if pr_raw.startswith("&") else float(pr_raw)

            if len(fit_raw) > 0:
                fit = self.dataframe.parameter[fit_raw[1:]].value if fit_raw.startswith("&") else float(fit_raw)
            else:
                fit = 0.0

            if len(beta_raw) > 0:
                beta = self.dataframe.parameter[beta_raw[1:]].value if beta_raw.startswith("&") else float(beta_raw)
            else:
                beta = 0.0

            if len(iter_raw) > 0:
                iter = self.dataframe.parameter[iter_raw[1:]].value if iter_raw.startswith("&") else float(iter_raw)
            else:
                iter = 0.0

            if len(iscale_raw) > 0:
                iscale = self.dataframe.parameter[iscale_raw[1:]].value if iscale_raw.startswith("&") else float(iscale_raw)
            else:
                iscale = 0.0

            if len(k_raw) > 0:
                k = self.dataframe.parameter[k_raw[1:]].value if k_raw.startswith("&") else float(k_raw)
            else:
                k = 0.0

            if len(e0_raw) > 0:
                e0 = self.dataframe.parameter[e0_raw[1:]].value if e0_raw.startswith("&") else float(e0_raw)
            else:
                e0 = 0.0

            if len(n_raw) > 0:
                n = self.dataframe.parameter[n_raw[1:]].value if n_raw.startswith("&") else float(n_raw)
            else:
                n = 0.0

            if len(c_raw) > 0:
                c = self.dataframe.parameter[c_raw[1:]].value if c_raw.startswith("&") else float(c_raw)
            else:
                c = 0.0

            if len(p_raw) > 0:
                p = self.dataframe.parameter[p_raw[1:]].value if p_raw.startswith("&") else float(p_raw)
            else:
                p = 0.0

            if len(hard_raw) > 0:
                hard = self.dataframe.parameter[hard_raw[1:]].value if hard_raw.startswith("&") else int(hard_raw)
            else:
                hard = 0.0

            if len(a_raw) > 0:
                a = self.dataframe.parameter[a_raw[1:]].value if a_raw.startswith("&") else float(a_raw)
            else:
                a = 0.0

            if len(alpha1_raw) > 0:
                alpha1 = self.dataframe.parameter[alpha1_raw[1:]].value if alpha1_raw.startswith("&") else float(alpha1_raw)
            else:
                alpha1 = 0.0

            if len(alpha2_raw) > 0:
                alpha2 = self.dataframe.parameter[alpha2_raw[1:]].value if alpha2_raw.startswith("&") else float(alpha2_raw)
            else:
                alpha2 = 0.0

            if len(alpha3_raw) > 0:
                alpha3 = self.dataframe.parameter[alpha3_raw[1:]].value if alpha3_raw.startswith("&") else float(alpha3_raw)
            else:
                alpha3 = 0.0

            if len(alpha4_raw) > 0:
                alpha4 = self.dataframe.parameter[alpha4_raw[1:]].value if alpha4_raw.startswith("&") else float(alpha4_raw)
            else:
                alpha4 = 0.0

            if len(alpha5_raw) > 0:
                alpha5 = self.dataframe.parameter[alpha5_raw[1:]].value if alpha5_raw.startswith("&") else float(alpha5_raw)
            else:
                alpha5 = 0.0

            if len(alpha6_raw) > 0:
                alpha6 = self.dataframe.parameter[alpha6_raw[1:]].value if alpha6_raw.startswith("&") else float(alpha6_raw)
            else:
                alpha6 = 0.0

            if len(alpha7_raw) > 0:
                alpha7 = self.dataframe.parameter[alpha7_raw[1:]].value if alpha7_raw.startswith("&") else float(alpha7_raw)
            else:
                alpha7 = 0.0

            if len(alpha8_raw) > 0:
                alpha8 = self.dataframe.parameter[alpha8_raw[1:]].value if alpha8_raw.startswith("&") else float(alpha8_raw)
            else:
                alpha8 = 0.0

            if len(aopt_raw) > 0:
                aopt = self.dataframe.parameter[aopt_raw[1:]].value if aopt_raw.startswith("&") else float(aopt_raw)
            else:
                aopt = 0.0

            if len(offang_raw) > 0:
                offang = self.dataframe.parameter[offang_raw[1:]].value if offang_raw.startswith("&") else float(offang_raw)
            else:
                offang = 0.0

            if len(p4_raw) > 0:
                p4 = self.dataframe.parameter[p4_raw[1:]].value if p4_raw.startswith("&") else float(p4_raw)
            else:
                p4 = 0.0

            if len(htflag_raw) > 0:
                htflag = self.dataframe.parameter[htflag_raw[1:]].value if htflag_raw.startswith("&") else float(htflag_raw)
            else:
                htflag = 0.0

            if len(hta_raw) > 0:
                hta = self.dataframe.parameter[hta_raw[1:]].value if hta_raw.startswith("&") else float(hta_raw)
            else:
                hta = 0.0

            if len(htb_raw) > 0:
                htb = self.dataframe.parameter[htb_raw[1:]].value if htb_raw.startswith("&") else float(htb_raw)
            else:
                htb = 0.0

            if len(htc_raw) > 0:
                htc = self.dataframe.parameter[htc_raw[1:]].value if htc_raw.startswith("&") else float(htc_raw)
            else:
                htc = 0.0

            if len(htd_raw) > 0:
                htd = self.dataframe.parameter[htd_raw[1:]].value if htd_raw.startswith("&") else float(htd_raw)
            else:
                htd = 0.0

            if len(a1_raw) > 0:
                a1 = self.dataframe.parameter[a1_raw[1:]].value if a1_raw.startswith("&") else float(a1_raw)
            else:
                a1 = 0.0

            if len(a2_raw) > 0:
                a2 = self.dataframe.parameter[a2_raw[1:]].value if a2_raw.startswith("&") else float(a2_raw)
            else:
                a2 = 0.0

            if len(a3_raw) > 0:
                a3 = self.dataframe.parameter[a3_raw[1:]].value if a3_raw.startswith("&") else float(a3_raw)
            else:
                a3 = 0.0

            if len(v1_raw) > 0:
                v1 = self.dataframe.parameter[v1_raw[1:]].value if v1_raw.startswith("&") else float(v1_raw)
            else:
                v1 = 0.0

            if len(v2_raw) > 0:
                v2 = self.dataframe.parameter[v2_raw[1:]].value if v2_raw.startswith("&") else float(v2_raw)
            else:
                v2 = 0.0

            if len(v3_raw) > 0:
                v3 = self.dataframe.parameter[v3_raw[1:]].value if v3_raw.startswith("&") else float(v3_raw)
            else:
                v3 = 0.0

            if len(d1_raw) > 0:
                d1 = self.dataframe.parameter[d1_raw[1:]].value if d1_raw.startswith("&") else float(d1_raw)
            else:
                d1 = 0.0

            if len(d2_raw) > 0:
                d2 = self.dataframe.parameter[d2_raw[1:]].value if d2_raw.startswith("&") else float(d2_raw)
            else:
                d2 = 0.0

            if len(d3_raw) > 0:
                d3 = self.dataframe.parameter[d3_raw[1:]].value if d3_raw.startswith("&") else float(d3_raw)
            else:
                d3 = 0.0

            if len(usrfail_raw) > 0:
                usrfail = self.dataframe.parameter[usrfail_raw[1:]].value if usrfail_raw.startswith("&") else float(usrfail_raw)
            else:
                usrfail = 0.0

            self.dataframe.material[mid] = MatBarlatYld2000(uid=mid,
                                                            rho=rho,
                                                            e=e,
                                                            pr=pr,
                                                            fit=fit,
                                                            beta=beta,
                                                            iter=iter,
                                                            iscale=iscale,
                                                            k=k,
                                                            e0=e0,
                                                            n=n,
                                                            c=c,
                                                            p=p,
                                                            hard=hard,
                                                            a=a,
                                                            alpha1=alpha1,
                                                            alpha2=alpha2,
                                                            alpha3=alpha3,
                                                            alpha4=alpha4,
                                                            alpha5=alpha5,
                                                            alpha6=alpha6,
                                                            alpha7=alpha7,
                                                            alpha8=alpha8,
                                                            aopt=aopt,
                                                            offang=offang,
                                                            p4=p4,
                                                            htflag=htflag,
                                                            hta=hta,
                                                            htb=htb,
                                                            htc=htc,
                                                            htd=htd,
                                                            a1=a1,
                                                            a2=a2,
                                                            a3=a3,
                                                            v1=v1,
                                                            v2=v2,
                                                            v3=v3,
                                                            d1=d1,
                                                            d2=d2,
                                                            d3=d3,
                                                            usrfail=usrfail,
                                                            name=name)

            self.dataframe.storge_material_id.append(mid)

            self.reset()

            return

