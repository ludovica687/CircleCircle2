import json
from circlecircle2.utilities.logger import logger


class MaterialGenerator:
    def __init__(self):
        self.material_id = "{material_id}"
        self.material_name = "{material_name}"
        self.logger = logger

        self.abaqus_material = {
            "minth_s620":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 200.0,\n"
                f"0.01, 201.2, \n"
                f"0.02, 202.2, \n"
                f"0.04, 210.5, \n"
            ,
            "minth_s620_haz":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 180.0,\n"
                f"0.01, 181.2, \n"
                f"0.02, 182.2, \n"
                f"0.04, 190.5, \n"
            ,
            "minth_s624":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 240.0,\n"
                f"0.02, 241.2, \n"
                f"0.03, 242.2, \n"
                f"0.05, 240.5, \n"
            ,
            "minth_s624_haz":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 210.0,\n"
                f"0.02, 211.2, \n"
                f"0.03, 212.2, \n"
                f"0.05, 213.5, \n"
            ,
            "minth_s628":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 280.0,\n"
                f"0.02, 281.2, \n"
                f"0.03, 282.2, \n"
                f"0.05, 280.5, \n"
            ,
            "minth_s628_haz":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 260.0,\n"
                f"0.02, 261.2, \n"
                f"0.03, 262.2, \n"
                f"0.05, 264.5, \n"
            ,
            "minth_s632":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 320.0,\n"
                f"0.02, 321.2, \n"
                f"0.03, 322.2, \n"
                f"0.05, 325.5, \n"
            ,
            "minth_s632_haz":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 300.0,\n"
                f"0.02, 301.2, \n"
                f"0.03, 302.2, \n"
                f"0.05, 305.5, \n"
            ,
            "minth_s636":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 360.0,\n"
                f"0.02, 361.2, \n"
                f"0.03, 362.2, \n"
                f"0.05, 365.5, \n"
            ,
            "minth_s636_haz":
                f"*MATERIAL, NAME={self.material_name}\n"
                f"*DENSITY\n"
                f"2.7e-06, 0.0\n"
                f"*ELASTIC, TYPE = ISOTROPIC\n"
                f"70.0, 0.3, 0.0\n"
                f"*PLASTIC\n"
                f"0.0, 340.0,\n"
                f"0.02, 341.2, \n"
                f"0.03, 342.2, \n"
                f"0.05, 345.5, \n"
            ,
        }

        self.lsdyna_material = {
            "minth_s620":
                f"*MAT_PIECEWISE_LINEAR_PLASTICITY_LOG_INTERPOLATION_TITLE\n"
                f"{self.material_name}\n"
                f"$      MID       RHO         E        PR      SIGY      ETAN      FAIL      TDEL\n"
                f"{self.material_id}2.7000E-06     62.81       0.3       0.2       0.0       0.0       0.0\n"
                f"       0.0       0.0      2082                              \n"
                f"$     EPS1      EPS2      EPS3      EPS4      EPS5      EPS6      EPS7      EPS8\n"
                f"       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0\n"
                f"$      ES1       ES2       ES3       ES4       ES5       ES6       ES7       ES8\n"
                f"       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0\n"
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
                f"*DEFINE_CURVE_TITLE\n"
                f"Minth_s620_SR_0.0001\n"
                f"$     LCID      SIDR       SFA       SFO      OFFA      OFFO    DATTYP     LCINT\n"
                f"      2037         0       1.01.0000E-03       0.0       0.0      1001         0\n"
                f"$                 A1                  O1\n"
                f"                 0.0              191.97\n"
                f"1.00000000000000E-04              200.39\n"
                f"2.00000000000000E-04              203.03\n"
            ,
            "minth_s620_haz":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s624":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s624_haz":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s628":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s628_haz":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s632":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s632_haz":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s636":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
            "minth_s636_haz":
                f"*DEFINE_TABLE\n"
                f"$     TBID       SFA      OFFA\n"
                f"      2000                    \n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-06      2001\n"
                f"$              VALUE      LCID\n"
                f"1.00000010000000E-05      2002\n"
            ,
        }

        self.pamcrash_material = {
            "minth_s620":
                f"$#         IDMAT   MATYP             RHO   ISINT    ISHG  ISTRAT   IFROZ\n"
                f"MATER /{self.material_id:}     1052.7000000000E-06       3       4       0       0\n"
                f"$#        AUXID1  AUXID2  AUXID3  AUXID4  AUXID5  AUXID6     QVM                \n"
                f"                                                             0.0                \n"
                f"$#   TITLE                                                                      \n"
                f"NAME minth_s620                                     \n"
                f"$#       E                  NUALPHA[IMP]       HGM       HGW       HGQ        As\n"
                f"      62.8CURVE            0.3                0.01      0.01       0.0  0.833333\n"
                f"$#     LC1       LC2       LC3       LC4       LC5       LC6       LC7       LC8\n"
                f"  99999991                                                                      \n"
                f"$#  ERATE1    ERATE2    ERATE3    ERATE4    ERATE5    ERATE6    ERATE7    ERATE8\n"
                f"       0.0                                                                      \n"
                f"$#REL_THIN                                                                      \n"
                f"                              HSRDTYP                                           \n"
                f"$#EPSIpmax    IFelim                                               KSI        Fo\n"
                f"       3.0         2                                               0.1       0.0\n"
                f"$#             VALUE  REL_THIC                                                  \n"
                f"      EPMX     0.286                                                            \n"
                f"$# REL_HSR                                                  \n"
                f"      0.83                                                  \n"
                f"$#         IDFUN  FUNTYP   SCALX   SCALY  SHIFTX  SHIFTY                \n"
                f"FUNCT / 99999991       0     1.01.00E-03     0.0     0.0                \n"
                f"$#   TITLE                  \n"
                f"NAME Minth_s620_SR_0.0000001\n"
                f"$#                             X               Y\n"
                f"                             0.0          291.97\n"
                f"                1.0000000000E-04          400.39\n"
                f"                             1.5          460.84\n"
                f"                END\n",
            "minth_s624":
                f"$#         IDMAT   MATYP             RHO   ISINT    ISHG  ISTRAT   IFROZ\n"
                f"MATER /{self.material_id}     1052.7000000000E-06       3       4       0       0\n"
                f"$#        AUXID1  AUXID2  AUXID3  AUXID4  AUXID5  AUXID6     QVM                \n"
                f"                                                             0.0                \n"
                f"$#   TITLE                                                                      \n"
                f"NAME minth_s624                                     \n"
                f"$#       E                  NUALPHA[IMP]       HGM       HGW       HGQ        As\n"
                f"      62.8CURVE            0.3                0.01      0.01       0.0  0.833333\n"
                f"$#     LC1       LC2       LC3       LC4       LC5       LC6       LC7       LC8\n"
                f"  99999992                                                                      \n"
                f"$#  ERATE1    ERATE2    ERATE3    ERATE4    ERATE5    ERATE6    ERATE7    ERATE8\n"
                f"       0.0                                                                      \n"
                f"$#REL_THIN                                                                      \n"
                f"                              HSRDTYP                                           \n"
                f"$#EPSIpmax    IFelim                                               KSI        Fo\n"
                f"       3.0         2                                               0.1       0.0\n"
                f"$#             VALUE  REL_THIC                                                  \n"
                f"      EPMX     0.286                                                            \n"
                f"$# REL_HSR                                                  \n"
                f"      0.83                                                  \n"
                f"$#         IDFUN  FUNTYP   SCALX   SCALY  SHIFTX  SHIFTY                \n"
                f"FUNCT / 99999992       0     1.01.00E-03     0.0     0.0                \n"
                f"$#   TITLE                  \n"
                f"NAME Minth_s620_SR_0.0000001\n"
                f"$#                             X               Y\n"
                f"                             0.0          391.97\n"
                f"                1.0000000000E-04          300.39\n"
                f"                             1.5          360.84\n"
                f"                END\n",
        }

    def generate(self, file_path):
        all_material = {
            "abaqus": self.abaqus_material,
            "lsdyna": self.lsdyna_material,
            "pamcrash": self.pamcrash_material
        }

        with open(file_path, mode="w", encoding="utf-8", errors="ignore") as f:
            json.dump(all_material, f, ensure_ascii=False, indent=4)

        self.logger.info(f"Material Mapping File Generated: {material_mapping_file_path}\n")


material_generator = MaterialGenerator()


if __name__ == "__main__":
    material_mapping_file_path = r"E:\PythonProject\circlecircle2\Test_Items\material_mapping.json"

    material_generator.generate(file_path=material_mapping_file_path)
