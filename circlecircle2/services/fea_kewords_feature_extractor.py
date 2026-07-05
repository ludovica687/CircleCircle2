from circlecircle2.utilities.logger import logger
from circlecircle2.services.fea_keywords_translator import fea_keywords_translator
from circlecircle2.core.tbox import tbox


class FeaKeywordsExtractor:
    def __init__(self):
        self.logger = logger
        self.fea_keywords_translator = fea_keywords_translator

    def extract(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        solver1 = kwargs.get("solver1", args[1] if len(args) > 1 else None)
        version1 = kwargs.get("version1", args[2] if len(args) > 2 else None)

        self.fea_keywords_translator.translate(
            file_path=file_path,
            solver1=solver1,
            version1=version1,
            solver2="parse_only",
            version2="0.0"
        )

        dataframe = self.fea_keywords_translator.dataframe

        node_id_tensor = dataframe.node_id_tensor
        node_xyz_tensor = dataframe.node_xyz_tensor
        element_shell_tensor = dataframe.element_shell_tensor
        element_solid_surface_tensor = dataframe.element_solid_surface_tensor

        # element shell
        mapping, num_nodes = tbox.map_id_to_idx(uid=node_id_tensor)

        if len(element_shell_tensor) > 0 or len(element_solid_surface_tensor) > 0:
            all_shell_element = tbox.combine_shell_solid_surfaces(elements_shell=element_shell_tensor,
                                                                  elements_solid=element_solid_surface_tensor)

            p = tbox.match_element_nid_and_coords(mapping=mapping,
                                                  coords=node_xyz_tensor,
                                                  elements=all_shell_element)

            element_normal, element_areas = tbox.calculate_element_info(p=p)

            node_normal = tbox.calculate_node_info(nums=num_nodes,
                                                   norms=element_normal,
                                                   areas=element_areas,
                                                   p=p)

            part_node_norm_dict, part_node_dict, part_element_dict = tbox.assign_node_element_to_part(
                mapping=mapping,
                norms=node_normal,
                elements=all_shell_element)

            new_part_dict = tbox.combine_part(p_dict=part_node_norm_dict,
                                              map_dict=dataframe.part_name_mapping)

            tbox.save_dict(file_path=file_path,
                           target=new_part_dict)


fea_keywords_extractor = FeaKeywordsExtractor()


# if __name__ == '__main__':
#     file_path = r"C:\Users\jiand\Downloads\Ludovica\Test_Data\test_model_no_part_initial.k"
#
#     fea_keywords_extractor.extract(file_path=file_path, solver1="lsdyna", version1="12.0")