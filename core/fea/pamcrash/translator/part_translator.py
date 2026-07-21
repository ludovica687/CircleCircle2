from circlecircle2.core.fea.translator import Translator


class PartTranslator(Translator):
    def __init__(self):
        super().__init__()

        self.version = {
            "2020": self._2020,
        }

    def translate(self, version):
        try:
            if version in self.version:
                self.version[version]()

        except Exception as e:
            raise Exception(f"PAMCRASH PartTranslator ERROR: {e}") from e

    def _2020(self):
        part_dict = self.dataframe.part
        material_dict = self.dataframe.material
        material_id_list = self.dataframe.storge_material_id
        max_material_id = max(material_id_list)
        elastic_solid_material = self.dataframe.storge_pam_elastic_solid_material
        section_shell_dict = self.dataframe.section_shell
        section_solid_dict = self.dataframe.section_solid

        if len(part_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("PART", [])

            for pid, part in part_dict.items():
                part_name = part.name
                mid = part.mid
                secid = part.secid

                material = material_dict[mid]
                material_name = material.name
                material_tag = material.tag

                if material_tag == "elastic":
                    if secid in section_shell_dict:
                        t = section_shell_dict[secid].t1

                        output_storge.append(
                            f"$#         IDPRT   ATYPE   IDMAT                  IDPMATIDNUMPAR\n"
                            f"PART  /{pid:>9}   SHELL{mid:>8}\n"
                            f"$#   TITLE\n"
                            f"NAME {part_name}\n"
                            f"$#  DTELIM    TSCALF   DTRATIO\n"
                            f"       0.0       1.0          \n"
                            f"$#   TCONT    EPSINI  COULFRIC\n"
                            f"                              \n"
                            f"$#       H NINT          NTHDO\n"
                            f"{t:>10}               \n"
                            f"$#                            \n"
                            f"                              \n"
                            "END_PART\n"
                        )

                    elif secid in section_solid_dict:
                        max_material_id += 1

                        output_storge.append(
                            f"$#         IDPRT   ATYPE   IDMAT                  IDPMATIDNUMPAR\n"
                            f"PART  /{pid:>9}   SOLID{max_material_id:>8}\n"
                            f"$#   TITLE\n"
                            f"NAME {part_name}\n"
                            f"$#  DTELIM    TSCALF   DTRATIO\n"
                            f"       0.0       1.0          \n"
                            f"$#   TCONT    EPSINI  COULFRIC\n"
                            f"                              \n"
                            f"$#       H NINT          NTHDO\n"
                            f"                              \n"
                            f"$#                            \n"
                            f"                              \n"
                            "END_PART\n"
                        )

                        material_id_list.append(max_material_id)
                        elastic_solid_material[max_material_id] = material

                elif material_tag == "plastic":
                    if secid in section_shell_dict:
                        t = section_shell_dict[secid].t1

                        output_storge.append(
                            f"$#         IDPRT   ATYPE   IDMAT                  IDPMATIDNUMPAR\n"
                            f"PART  /{pid:>9}   SHELL{mid:>8}\n"
                            f"$#   TITLE\n"
                            f"NAME {part_name}\n"
                            f"$#  DTELIM    TSCALF   DTRATIO\n"
                            f"       0.0       1.0          \n"
                            f"$#   TCONT    EPSINI  COULFRIC\n"
                            f"                              \n"
                            f"$#       H NINT          NTHDO\n"
                            f"{t:>10}               \n"
                            f"$#                            \n"
                            f"                              \n"
                            "END_PART\n"
                        )

                    elif secid in section_solid_dict:
                        output_storge.append(
                            f"$#         IDPRT   ATYPE   IDMAT                  IDPMATIDNUMPAR\n"
                            f"PART  /{pid:>9}   SOLID{mid:>8}\n"
                            f"$#   TITLE\n"
                            f"NAME {part_name}\n"
                            f"$#  DTELIM    TSCALF   DTRATIO\n"
                            f"       0.0       1.0          \n"
                            f"$#   TCONT    EPSINI  COULFRIC\n"
                            f"                              \n"
                            f"$#       H NINT          NTHDO\n"
                            f"                              \n"
                            f"$#                            \n"
                            f"                              \n"
                            "END_PART\n"
                        )

                elif material_tag == "rigid":
                    if secid in section_shell_dict:
                        t = section_shell_dict[secid].t1

                        output_storge.append(
                            f"$#         IDPRT   ATYPE   IDMAT                  IDPMATIDNUMPAR\n"
                            f"PART  /{pid:>9}   SHELL{mid:>8}\n"
                            f"$#   TITLE\n"
                            f"NAME {part_name}\n"
                            f"$#  DTELIM    TSCALF   DTRATIO\n"
                            f"       0.0       1.0          \n"
                            f"$#   TCONT    EPSINI  COULFRIC\n"
                            f"                              \n"
                            f"$#       H NINT          NTHDO\n"
                            f"{t:>10}               \n"
                            f"$#                            \n"
                            f"                              \n"
                            "END_PART\n"
                        )

                    elif secid in section_solid_dict:
                        max_material_id += 1

                        output_storge.append(
                            f"$#         IDPRT   ATYPE   IDMAT                  IDPMATIDNUMPAR\n"
                            f"PART  /{pid:>9}   SOLID{max_material_id:>8}\n"
                            f"$#   TITLE\n"
                            f"NAME {part_name}\n"
                            f"$#  DTELIM    TSCALF   DTRATIO\n"
                            f"       0.0       1.0          \n"
                            f"$#   TCONT    EPSINI  COULFRIC\n"
                            f"                              \n"
                            f"$#       H NINT          NTHDO\n"
                            f"                              \n"
                            f"$#                            \n"
                            f"                              \n"
                            "END_PART\n"
                        )

                        material_id_list.append(max_material_id)
                        elastic_solid_material[max_material_id] = material

                else:
                    pass





