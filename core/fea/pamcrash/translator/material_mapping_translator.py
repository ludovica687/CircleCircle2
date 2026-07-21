from circlecircle2.core.fea.translator import Translator
import json


class MaterialMappingTranslator(Translator):
    def __init__(self):
        super().__init__()

        self.version = {
            "2020": self._2020,
        }

    def translate(self, version, material_mapping_file_path):
        try:
            if version in self.version:
                self.version[version](material_mapping_file_path)

        except Exception as e:
            raise Exception(f"PAMCRASH MatElasticTranslator ERROR: {e}") from e

    def _2020(self, material_mapping_file_path):
        part_dict = self.dataframe.part
        material_dict = self.dataframe.material
        elastic_solid_material_dict = self.dataframe.storge_pam_elastic_solid_material
        section_shell_dict = self.dataframe.section_shell
        curve_dict = self.dataframe.define_curve
        table_dict = self.dataframe.define_table

        with open(material_mapping_file_path, mode="r", encoding="utf-8", errors="ignore") as f:
            all_material_mapping = json.load(f)

        material_mapping = all_material_mapping["pamcrash"]

        if len(part_dict) > 0 and len(material_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("MATER", [])
            temp_material_id = set()

            for pid, part in part_dict.items():
                mid = part.mid
                secid = part.secid

                if mid in material_dict and (mid not in temp_material_id):
                    material = material_dict[mid]

                    material_name = material.name
                    rho = material.rho
                    e = material.e
                    pr = material.pr
                    material_tag = material.tag

                    if material_tag == "elastic" or material_tag == "rigid":
                        output_storge.append(
                            f"$#         IDMAT   MATYP             RHO   ISINT    ISHG  ISTRAT   IFROZ\n"
                            f"MATER /{mid: >9}     100{rho: >16}       0       0       0       0\n"
                            f"$#        AUXID1  AUXID2  AUXID3  AUXID4  AUXID5  AUXID6     QVM                \n"
                            f"                                                             1.0                \n"
                            f"$#   TITLE                                                                      \n"
                            f"NAME {material_name}\n"
                            f"$#       E                  NU\n"
                            f"{e: >10.2f}{pr: >20.2f}\n"
                            f"                              \n"
                            f"                              \n"
                            f"                              \n"
                            f"                              \n"
                            f"                              \n"
                        )

                    elif material_tag == "plastic":
                        map_tag = material.map_tag

                        if map_tag in material_mapping:
                            curve = material_mapping[map_tag]

                            curve = curve.replace("{material_id}", f"{mid: >9}")

                            output_storge.append(curve)

                    else:
                        pass

                    temp_material_id.add(mid)

            if len(elastic_solid_material_dict) > 0:
                for mid, material in elastic_solid_material_dict.items():
                    if mid not in temp_material_id:
                        material_name = f"{material.name}_{mid}"
                        rho = material.rho
                        e = material.e
                        pr = material.pr
                        g = e / (2 * (1 + pr))  # G: Shear Modules, G = E / (2 * (1 + PR))
                        k = e / (3 * (1 - 2 * pr))  # K: Bulk Module, K = E / (3 * (1 - PR))

                        output_storge.append(
                            f"$#         IDMAT   MATYP             RHO   ISINT    ISHG  ISTRAT   IFROZ\n"
                            f"MATER /{mid: >9}       1{rho: >16}       0       0       0       0\n"
                            f"$#                                                           QVM                \n"
                            f"                                                             1.0                \n"
                            f"$#   TITLE                                                                      \n"
                            f"NAME {material_name}\n"
                            f"$#       G    SIGMAy        EtALPHA[IMP]                                        \n"
                            f"{g: >10.6f}     999.0       0.0                                                  \n"
                            f"$#       K          \n"
                            f"{k: >10.6f}          \n"
                            f"                    \n"
                            f"                    \n"
                            f"$#                                                                 KSI        Fo\n"
                            f"                                                                   0.0       0.0\n"
                            f"$#                                              Q1        Q2        Q3\n"
                            f"                                                                      \n"
                        )

                        temp_material_id.add(mid)

    def _extract_shrf_from_part(self, secid, section_shell_dict):
        if secid in section_shell_dict:
            section = section_shell_dict[secid]

            shrf = section.shrf

            return shrf
        else:
            return 0.8333

    def check_tabel_curve(self, lcss_id, curve_dict, table_dict):
        if lcss_id in curve_dict:
            return "curve"

        elif lcss_id in table_dict:
            return "table"

        else:
            return None

    def _extract_curve_from_table(self, lcss_id, table_dict):
        current_table = table_dict[lcss_id]

        value = current_table.value
        lcid = current_table.lcid

        sorted_indices = sorted(range(len(value)), key=lambda i: value[i])

        return lcid[sorted_indices[0]], value, lcid