import torch
from torch.utils.data import Dataset, DataLoader
import json
import os


class TBox:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def update_device(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def map_id_to_idx(self, uid):
        """
        :param uid: node ids
        :return: mapping, num_nodes
        """

        uid_tensor = torch.as_tensor(uid, dtype=torch.long, device=self.device)

        num_nodes = uid_tensor.shape[0]

        max_id = uid_tensor.max().item()

        # check 1d tensor

        # fill -1
        mapping = torch.full([max_id + 1], -1, dtype=torch.long, device=self.device)

        mapping[uid_tensor] = torch.arange(uid_tensor.shape[0], device=self.device)

        return mapping, num_nodes

    def match_element_nid_and_coords(self, mapping, coords, elements):
        """
        :param mapping: mapping = map_id_to_idx
        :param coords: node coords
        :param elements: element shell
        :return: (p1, p2, p3, p4, idx1, idx2, idx3, idx4) = p
        """

        coords_tensor = torch.as_tensor(coords, dtype=torch.float64, device=self.device)
        elements_tensor = torch.as_tensor(elements, dtype=torch.int64, device=self.device)
        element_nids = elements_tensor[:, 2:]

        # element shell
        n_idx1 = element_nids[:, 0]
        n_idx2 = element_nids[:, 1]
        n_idx3 = element_nids[:, 2]
        n_idx4 = element_nids[:, 3]

        idx1 = mapping[n_idx1]
        idx2 = mapping[n_idx2]
        idx3 = mapping[n_idx3]
        idx4 = mapping[n_idx4]

        p1 = coords_tensor[idx1]
        p2 = coords_tensor[idx2]
        p3 = coords_tensor[idx3]
        p4 = coords_tensor[idx4]

        return (p1, p2, p3, p4, idx1, idx2, idx3, idx4)

    def calculate_element_info(self, p):
        """
        :param p: p = (p1, p2, p3, p4, idx1, idx2, idx3, idx4)
        :return: element_normal, element_areas
        """

        p1, p2, p3, p4, idx1, idx2, idx3, idx4 = p

        v31 = p3 - p1
        v42 = p4 - p2

        element_normal = torch.linalg.cross(v31, v42)

        element_areas = 0.5 * torch.linalg.norm(element_normal, dim=1)

        element_normal = torch.nn.functional.normalize(element_normal, p=2, dim=1)

        return element_normal, element_areas

    def calculate_node_info(self, nums, norms, areas, p):
        """
        :param nums: node nums
        :param norms: element_normal
        :param areas: element_areas
        :param p: p = (p1, p2, p3, p4, idx1, idx2, idx3, idx4)
        :return: node_normal
        """

        p1, p2, p3, p4, idx1, idx2, idx3, idx4 = p

        areas = areas.unsqueeze(1)

        weights_norms = norms * areas

        node_normal = torch.zeros((nums, 3), dtype=norms.dtype, device=self.device)

        node_normal.index_add_(dim=0, index=idx1, source=weights_norms)
        node_normal.index_add_(dim=0, index=idx2, source=weights_norms)
        node_normal.index_add_(dim=0, index=idx3, source=weights_norms)

        mask_s3_1d = (idx4 != idx3)
        mask_s3_2d = mask_s3_1d.unsqueeze(1)

        weights_norms_p4 = torch.where(mask_s3_2d, weights_norms, torch.zeros_like(weights_norms))

        node_normal.index_add_(dim=0, index=idx4, source=weights_norms_p4)

        return node_normal

    def assign_node_element_to_part(self, mapping, norms, elements):
        """
        :param mapping: mapping = map_id_to_idx
        :param norms: node_normal = calculate_node_info
        :param elements: element_shell
        :return: part_node_norm_dict, part_node_dict, part_element_dict
        """

        part_node_norm_dict = {}
        part_node_dict = {}
        part_element_dict = {}

        elements_tensor = torch.as_tensor(elements, dtype=torch.int64, device=self.device)

        pids = elements_tensor[:, 1]
        eids = elements_tensor[:, 0]
        nids = elements_tensor[:, 2:]
        unique_pids = pids.unique()

        for pid in unique_pids:
            mask = pids == pid

            part_eids = eids[mask]
            part_nids = nids[mask].unique()

            index = mapping[part_nids]
            node_norms = norms[index]

            part_node_norm_dict[pid.item()] = node_norms.tolist()
            part_node_dict[pid.item()] = part_nids.tolist()
            part_element_dict[pid.item()] = part_eids.tolist()

        return part_node_norm_dict, part_node_dict, part_element_dict

    def combine_part(self, p_dict, map_dict):
        """
        :param p_dict: part_node_dict = assign_node_element_to_part
        :param map_dict: {pid: pname, pid2: pname2, ...}
        :return:new_part_dict
        """

        new_part_dict = {
            "upper_beam": [],
            "lower_beam": [],
            "crash_box": [],
            "end_plate": [],
            "tow_hook": [],
            "bracket": [],
        }

        upper_beam_check = ["upper_beam", "up_beam"]
        lower_beam_check = ["lower_beam", "low_beam"]
        crash_box_check = ["crash_box", "cb"]
        end_plate_check = ["end_plate", "bottom_plate", "support_plate"]
        tow_hook_check = ["tow_hook", "towing_hook"]
        bracket_check = ["bracket", "bkt"]

        for pid, value in p_dict.items():
            p_name = map_dict[pid]

            if any(sub in p_name for sub in upper_beam_check):
                new_part_dict["upper_beam"].extend(value)
            elif any(sub in p_name for sub in lower_beam_check):
                new_part_dict["lower_beam"].extend(value)
            elif any(sub in p_name for sub in crash_box_check):
                new_part_dict["crash_box"].extend(value)
            elif any(sub in p_name for sub in end_plate_check):
                new_part_dict["end_plate"].extend(value)
            elif any(sub in p_name for sub in tow_hook_check):
                new_part_dict["tow_hook"].extend(value)
            elif any(sub in p_name for sub in bracket_check):
                new_part_dict["bracket"].extend(value)

        return new_part_dict

    def unique_solid_surface(self, elements):
        """
        :param elements: solid surface elements
        :return: unique solid_surface elements
        """

        elements_tensor = torch.as_tensor(elements, dtype=torch.int64, device=self.device)

        element_nids = elements_tensor[:, 2:]
        element_nidx3 = element_nids[:, 2]
        element_nidx4 = element_nids[:, 3]

        mask = element_nidx3 == element_nidx4
        element_s3_nids = element_nids[mask]
        element_s4_nids = element_nids[~mask]

        element_s3 = elements_tensor[mask]
        element_s4 = elements_tensor[~mask]

        # s3
        sorted_element_s3_nids, _ = torch.sort(element_s3_nids[:, :3], dim=-1)

        unique_element_s3_nids, inverse_s3, counts_s3 = torch.unique(sorted_element_s3_nids, dim=0, return_inverse=True, return_counts=True)

        mask_s3_faces = counts_s3 == 1

        surface_s3_idx = mask_s3_faces[inverse_s3]

        solid_surface_s3_faces = element_s3[surface_s3_idx]

        # s4
        sorted_element_s4_nids, _ = torch.sort(element_s4_nids, dim=-1)

        unique_element_s4_nids, inverse_s4, counts_s4 = torch.unique(sorted_element_s4_nids, dim=0, return_inverse=True, return_counts=True)

        mask_s4_faces = counts_s4 == 1

        surface_s4_idx = mask_s4_faces[inverse_s4]

        solid_surface_s4_faces = element_s4[surface_s4_idx]

        unique_solid_surface_faces = torch.cat([solid_surface_s3_faces, solid_surface_s4_faces], dim=0)

        return unique_solid_surface_faces

    def combine_shell_solid_surfaces(self, elements_shell, elements_solid):
        """
        :param elements_shell: original shell
        :param elements_solid: unique solid surface elements = unique_solid_surface
        :return: all_shell_element
        """
        elements_shell_tensor = torch.as_tensor(elements_shell, dtype=torch.int64, device=self.device)
        elements_solid_tensor = torch.as_tensor(elements_solid, dtype=torch.int64, device=self.device)

        unique_solid_surface_faces = self.unique_solid_surface(elements=elements_solid_tensor)

        all_shell_element = torch.cat([elements_shell_tensor, unique_solid_surface_faces], dim=0)

        return all_shell_element

    def save_dict(self, file_path, target):
        """
        :param file_path: original file path, like: .key file, .inp file ...
        :param target: dictionary to save
        :return:
        """

        folder = os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(basename)

        saved_file_path = os.path.join(folder, file_name + ".json")

        with open(saved_file_path, mode="w", encoding="utf-8") as f:
            json.dump(target, f, ensure_ascii=False, indent=4)


tbox = TBox()
