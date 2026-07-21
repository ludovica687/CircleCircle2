from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.boundary_prescribed_motion_rigid import BoundaryPrescribedMotionRigid


class BoundaryPrescribedMotionRigidParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        typeid_raw = line_raw[0:10].strip()
        dof_raw = line_raw[10:20].strip()
        lcid_raw = line_raw[30:40].strip()

        if len(typeid_raw) > 0:
            typeid = self.dataframe.parameter[typeid_raw[1:]] if typeid_raw.startswith("&") else int(typeid_raw)
        else:
            typeid = 0

        if len(dof_raw) > 0:
            dof = self.dataframe.parameter[dof_raw[1:]] if dof_raw.startswith("&") else int(dof_raw)
        else:
            dof = 0

        if len(lcid_raw) > 0:
            lcid = self.dataframe.parameter[lcid_raw[1:]] if lcid_raw.startswith("&") else int(lcid_raw)
        else:
            lcid = 0

        uid = len(self.dataframe.boundary_prescribed_motion_rigid) + 1

        self.dataframe.boundary_prescribed_motion_rigid[uid] = BoundaryPrescribedMotionRigid(uid=uid,
                                                                                             typeid=typeid,
                                                                                             dof=dof,
                                                                                             lcid=lcid)

        return
