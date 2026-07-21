from circlecircle2.core.fea.translator import Translator


class MaterialTranslator(Translator):
    def __init__(self):
        super().__init__()

        self.version = {
            "6.14": self._6p14,
        }

    def translate(self, version):
        try:
            if version in self.version:
                self.version[version]()

        except Exception as e:
            raise Exception(f"ABAQUS NodeTranslator ERROR: {e}") from e

    def _6p14(self):
        if len(self.dataframe.material) > 0:
            part_dict = self.dataframe.part
            material_dict = self.dataframe.material
            curve_dict = self.dataframe.define_curve
            table_dict = self.dataframe.define_table

            output_storge = self.dataframe.output_storge.setdefault("*MATERIAL", [])

            temp_material_set = set()

            for pid, part in part_dict.items():
                mid = part.mid

                material = material_dict[mid]

                material_name = material.name

                rho = material.rho

                e = material.e

                pr = material.pr

                material_tag = material.tag

                if mid in temp_material_set:
                    continue
                else:
                    temp_material_set.add(mid)

                    if material_tag == "elastic" or material_tag == "rigid":
                        output_storge.append(
                            f"*MATERIAL, NAME={material_name}\n"
                            f"*DENSITY\n"
                            f"{rho}, 0.0\n"
                            f"*ELASTIC, TYPE = ISOTROPIC\n"
                            f"{e}, {pr}, 0.0\n"
                        )

                    elif material_tag == "plastic":
                        output_storge.append(
                            f"*MATERIAL, NAME={material_name}\n"
                            f"*DENSITY\n"
                            f"{rho}, 0.0\n"
                            f"*ELASTIC, TYPE = ISOTROPIC\n"
                            f"{e}, {pr}, 0.0\n"
                        )

                        lcss = abs(material.lcss)

                        curve_type = self.check_tabel_curve(lcss_id=lcss,
                                                            curve_dict=curve_dict,
                                                            table_dict=table_dict)

                        if curve_type == "curve":
                            self.combine_curve_data(lcss_id=lcss,
                                                    curve_dict=curve_dict,
                                                    output_storge=output_storge)
                        elif curve_type == "table":
                            lcid = self.extract_curve_from_table(lcss_id=lcss,
                                                                 table_dict=table_dict)

                            self.combine_curve_data(lcss_id=lcid,
                                                    curve_dict=curve_dict,
                                                    output_storge=output_storge)
                        else:
                            pass

    def combine_curve_data(self, lcss_id, curve_dict, output_storge):
        curve = curve_dict[lcss_id]

        sfa = curve.sfa
        sfo = curve.sfo
        offa = curve.offa
        offo = curve.offo

        output_storge.append("*PLASTIC\n")

        for item_index in range(len(curve.a1)):
            a1 = (curve.a1[item_index] + offa) * sfa
            o1 = (curve.o1[item_index] + offo) * sfo

            output_storge.append(f"{a1:<20},{o1:<20}\n")

    def check_tabel_curve(self, lcss_id, curve_dict, table_dict):
        if lcss_id in curve_dict:
            return "curve"

        elif lcss_id in table_dict:
            return "table"

        else:
            return None

    def extract_curve_from_table(self, lcss_id, table_dict):
        current_table = table_dict[lcss_id]

        value = current_table.value
        lcid = current_table.lcid

        sorted_indices = sorted(range(len(value)), key=lambda i: value[i])

        return lcid[sorted_indices[0]]