from circlecircle2.core.fea.translator import Translator


class BoundaryTranslator(Translator):
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
        rigid_part_goc_xyz_dict = self.dataframe.storge_rigid_part_goc_xyz
        rigid_part_goc_con_dict = self.dataframe.storge_rigid_part_goc_con

        output_storge = self.dataframe.output_storge.setdefault("*BOUNDARY", [])

        if len(rigid_part_goc_con_dict) > 0:
            for goc_id, goc_xyz in rigid_part_goc_xyz_dict.items():
                output_storge.append("*BOUNDARY\n")

                con = rigid_part_goc_con_dict[goc_id]

                con1 = con[0]
                con2 = con[1]

                # set boundary dof 1-3
                if con1 == 1:
                    output_storge.append(f"{goc_id:<18}, 1, 1, 0.0\n")
                elif con1 == 2:
                    output_storge.append(f"{goc_id:<18}, 2, 2, 0.0\n")
                elif con1 == 3:
                    output_storge.append(f"{goc_id:<18}, 3, 3, 0.0\n")
                elif con1 == 4:
                    output_storge.append(f"{goc_id:<18}, 1, 1, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 2, 2, 0.0\n")
                elif con1 == 5:
                    output_storge.append(f"{goc_id:<18}, 2, 2, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 3, 3, 0.0\n")
                elif con1 == 6:
                    output_storge.append(f"{goc_id:<18}, 1, 1, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 3, 3, 0.0\n")
                elif con1 == 7:
                    output_storge.append(f"{goc_id:<18}, 1, 1, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 2, 2, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 3, 3, 0.0\n")

                #  set boundary dof 4-6
                if con2 == 1:
                    output_storge.append(f"{goc_id:<18}, 4, 4, 0.0\n")
                elif con2 == 2:
                    output_storge.append(f"{goc_id:<18}, 5, 5, 0.0\n")
                elif con2 == 3:
                    output_storge.append(f"{goc_id:<18}, 6, 6, 0.0\n")
                elif con2 == 4:
                    output_storge.append(f"{goc_id:<18}, 4, 4, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 5, 5, 0.0\n")
                elif con2 == 5:
                    output_storge.append(f"{goc_id:<18}, 5, 5, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 6, 6, 0.0\n")
                elif con2 == 6:
                    output_storge.append(f"{goc_id:<18}, 4, 4, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 6, 6, 0.0\n")
                elif con2 == 7:
                    output_storge.append(f"{goc_id:<18}, 4, 4, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 5, 5, 0.0\n")
                    output_storge.append(f"{goc_id:<18}, 6, 6, 0.0\n")




