from circlecircle2.core.fea.translator import Translator
import numpy as np


class KinematicCouplingTranslator(Translator):
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
        part_dict = self.dataframe.part
        part_node_xyz_dict = self.dataframe.storge_part_node_xyz
        part_node_id_dict = self.dataframe.storge_part_node_id
        node_id_list = self.dataframe.storge_node_id
        max_node_id = max(node_id_list)
        material_dict = self.dataframe.material
        rigid_part_goc_xyz_dict = self.dataframe.storge_rigid_part_goc_xyz
        rigid_part_goc_con_dict = self.dataframe.storge_rigid_part_goc_con

        output_storge_node = self.dataframe.output_storge.setdefault("*NODE", [])
        output_storge_kinematic = self.dataframe.output_storge.setdefault("*KINEMATIC", [])

        # check mat20
        temp_node_line = []

        for pid, part in part_dict.items():
            mid = part.mid

            material = material_dict[mid]

            tag = material.tag

            if tag == "rigid":
                related_node = part_node_xyz_dict[pid]

                related_node_array = np.array(list(related_node), dtype=np.float64)

                part_coords_mean = np.mean(related_node_array, axis=0)

                x = part_coords_mean[0]
                y = part_coords_mean[1]
                z = part_coords_mean[2]

                max_node_id += 1

                temp_node_line.append(f"{max_node_id:<10},{x:17.10f},{y:17.10f},{z:17.10f}\n")

                output_storge_kinematic.append(f"*KINEMATIC COUPLING,REF NODE={max_node_id}\n")
                for node_id in part_node_id_dict[pid]:
                    output_storge_kinematic.append(f"{node_id:<10}, 1, 6\n")

                rigid_part_goc_xyz_dict[max_node_id] = (x, y, z)

                con1 = material.con1
                con2 = material.con2
                rigid_part_goc_con_dict[max_node_id] = (con1, con2)

        output_storge_node.append(f"*NODE\n")
        for line in temp_node_line:
            output_storge_node.append(line)

        # check constrained_nodal_rigid_body
        constrained_nodal_rigid_body_dict = self.dataframe.constrained_nodal_rigid_body
        set_node_list_dict = self.dataframe.set_node_list

        if len(constrained_nodal_rigid_body_dict) > 0:
            for uid, rb2 in constrained_nodal_rigid_body_dict.items():
                sid = rb2.sid

                if sid in set_node_list_dict:
                    set_node_list = set_node_list_dict[sid]

                    node_ids = set_node_list.ids

                    master_node = node_ids[0]
                    output_storge_kinematic.append(f"*KINEMATIC COUPLING,REF NODE={master_node}\n")

                    slave_nodes = node_ids[1:]

                    for nid in slave_nodes:
                        output_storge_kinematic.append(f"{nid:<10}, 1, 6\n")


