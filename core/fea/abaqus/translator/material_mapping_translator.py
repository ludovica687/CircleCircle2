from circlecircle2.core.fea.translator import Translator
import json


class MaterialMappingTranslator(Translator):
    def __init__(self):
        super().__init__()

        self.version = {
            "6.14": self._6p14,
        }

    def translate(self, version, material_mapping_file_path):
        try:
            if version in self.version:
                self.version[version](material_mapping_file_path)

        except Exception as e:
            raise Exception(f"ABAQUS NodeTranslator ERROR: {e}") from e

    def _6p14(self, material_mapping_file_path):
        if len(self.dataframe.material) > 0:
            with open(material_mapping_file_path, mode="r", encoding="utf-8", errors="ignore") as f:
                all_material_mapping = json.load(f)

            material_mapping = all_material_mapping["abaqus"]

            part_dict = self.dataframe.part
            material_dict = self.dataframe.material

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
                        map_tag = material.map_tag

                        if map_tag in material_mapping:
                            curve = material_mapping[map_tag]

                            curve = curve.replace("{material_name}", material_name)

                            output_storge.append(curve)
