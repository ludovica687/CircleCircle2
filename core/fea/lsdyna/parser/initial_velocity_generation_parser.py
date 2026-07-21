from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.initial_velocity_generation import InitialVelocityGeneration


class InitialVelocityGenerationParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            pid_raw = line_raw[0:10].strip()
            styp_raw = line_raw[10:20].strip()
            omega_raw = line_raw[20:30].strip()
            vx_raw = line_raw[30:40].strip()
            vy_raw = line_raw[40:50].strip()
            vz_raw = line_raw[50:60].strip()
            ivant_raw = line_raw[60:70].strip()
            lcid_raw = line_raw[70:80].strip()

            self.temp.append(pid_raw)
            self.temp.append(styp_raw)
            self.temp.append(omega_raw)
            self.temp.append(vx_raw)
            self.temp.append(vy_raw)
            self.temp.append(vz_raw)
            self.temp.append(ivant_raw)
            self.temp.append(lcid_raw)

            self.line_number = 1

            return

        if self.line_number == 1:
            pid_raw = self.temp[0]
            styp_raw = self.temp[1]
            omega_raw = self.temp[2]
            vx_raw = self.temp[3]
            vy_raw = self.temp[4]
            vz_raw = self.temp[5]
            ivant_raw = self.temp[6]
            lcid_raw = self.temp[7]

            xc_raw = line_raw[0:10].strip()
            yc_raw = line_raw[10:20].strip()
            zc_raw = line_raw[20:30].strip()
            nx_raw = line_raw[30:40].strip()
            ny_raw = line_raw[40:50].strip()
            nz_raw = line_raw[50:60].strip()
            phase_raw = line_raw[60:70].strip()
            irigid_raw = line_raw[70:80].strip()

            if len(pid_raw) > 0:
                pid = pid_raw[1:] if pid_raw.startswith("&") else int(pid_raw)
            else:
                pid = 0

            if len(styp_raw) > 0:
                styp = styp_raw[1:] if styp_raw.startswith("&") else int(styp_raw)
            else:
                styp = 0

            if len(omega_raw) > 0:
                omega = omega_raw[1:] if omega_raw.startswith("&") else float(omega_raw)
            else:
                omega = 0.0

            if len(vx_raw) > 0:
                vx = vx_raw[1:] if vx_raw.startswith("&") else float(vx_raw)
            else:
                vx = 0.0

            if len(vy_raw) > 0:
                vy = vy_raw[1:] if vy_raw.startswith("&") else float(vy_raw)
            else:
                vy = 0.0

            if len(vz_raw) > 0:
                vz = vz_raw[1:] if vz_raw.startswith("&") else float(vz_raw)
            else:
                vz = 0.0

            if len(ivant_raw) > 0:
                ivant = ivant_raw[1:] if ivant_raw.startswith("&") else int(ivant_raw)
            else:
                ivant = 0.0

            if len(lcid_raw) > 0:
                lcid = lcid_raw[1:] if lcid_raw.startswith("&") else int(lcid_raw)
            else:
                lcid = 0

            if len(xc_raw) > 0:
                xc = xc_raw[1:] if xc_raw.startswith("&") else float(xc_raw)
            else:
                xc = 0.0

            if len(yc_raw) > 0:
                yc = yc_raw[1:] if yc_raw.startswith("&") else float(yc_raw)
            else:
                yc = 0.0

            if len(zc_raw) > 0:
                zc = zc_raw[1:] if zc_raw.startswith("&") else float(zc_raw)
            else:
                zc = 0.0

            if len(nx_raw) > 0:
                nx = nx_raw[1:] if nx_raw.startswith("&") else float(nx_raw)
            else:
                nx = 0.0

            if len(ny_raw) > 0:
                ny = ny_raw[1:] if ny_raw.startswith("&") else float(ny_raw)
            else:
                ny = 0.0

            if len(nz_raw) > 0:
                nz = nz_raw[1:] if nz_raw.startswith("&") else float(nz_raw)
            else:
                nz = 0.0

            if len(phase_raw) > 0:
                phase = phase_raw[1:] if phase_raw.startswith("&") else float(phase_raw)
            else:
                phase = 0.0

            if len(irigid_raw) > 0:
                irigid = irigid_raw[1:] if irigid_raw.startswith("&") else int(irigid_raw)
            else:
                irigid = 0

            uid = len(self.dataframe.initial_velocity_generation) + 1

            self.dataframe.initial_velocity_generation[pid] = InitialVelocityGeneration(uid=uid,
                                                                                        pid=pid,
                                                                                        styp=styp,
                                                                                        omega=omega,
                                                                                        vx=vx,
                                                                                        vy=vy,
                                                                                        vz=vz,
                                                                                        ivant=ivant,
                                                                                        lcid=lcid,
                                                                                        xc=xc,
                                                                                        yc=yc,
                                                                                        zc=zc,
                                                                                        nx=nx,
                                                                                        ny=ny,
                                                                                        nz=nz,
                                                                                        phase=phase,
                                                                                        irigid=irigid)

            self.reset()

            return
