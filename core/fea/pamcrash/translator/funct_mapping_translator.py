from circlecircle2.core.fea.translator import Translator


class FunctMappingTranslator(Translator):
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
            raise Exception(f"PAMCRASH FunctTranslator ERROR: {e}") from e

    def _2020(self):
        define_curve_dict = self.dataframe.define_curve
        material_dict = self.dataframe.material
        curve_dict = self.dataframe.define_curve
        table_dict = self.dataframe.define_table

        if len(define_curve_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("FUNCT", [])
            curve_ids = self._extract_curve_id_from_material(material_dict=material_dict,
                                                             curve_dict=curve_dict,
                                                             table_dict=table_dict)

            for curve_id, curve in define_curve_dict.items():
                if curve_id not in curve_ids:
                    sfa = curve.sfa
                    sfo = curve.sfo
                    offa = curve.offa
                    offo = curve.offo
                    name = curve.name

                    a1 = curve.a1
                    o1 = curve.o1

                    output_storge.append(
                        f"$#         IDFUN  FUNTYP   SCALX   SCALY  SHIFTX  SHIFTY                \n"
                        f"FUNCT /{curve_id: >9}       0{sfa: >8.5f}{sfo: >8.5f}{offa: >8.5f}{offo: >8.5f}                \n"
                        f"$#   TITLE                  \n"
                        f"NAME {name}\n"
                        f"$#                             X               Y\n"
                    )

                    for i in range(len(a1)):
                        x = a1[i]
                        y = o1[i]

                        output_storge.append(
                            f"                {x: >16.8f}{y: >16.8f}\n"
                        )

    def _extract_curve_id_from_material(self, material_dict, curve_dict, table_dict):
        curve_ids = set()

        for mid, material in material_dict.items():
            material_tag = material.tag

            if material_tag == "plastic":
                lcss = abs(material.lcss)

                curve_type = self.check_tabel_curve(lcss_id=lcss,
                                                    curve_dict=curve_dict,
                                                    table_dict=table_dict)

                if curve_type == "curve":
                    curve_ids.add(lcss)
                elif curve_type == "table":
                    current_table = table_dict[lcss]

                    lcid = current_table.lcid

                    for i in lcid:
                        curve_ids.add(i)

        return curve_ids

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