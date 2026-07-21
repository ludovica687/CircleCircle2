from circlecircle2.utilities.logger import logger
from circlecircle2.core.fea.solver import Solver
from circlecircle2.core.fea.lsdyna.parser.keyword_parser import KeyWordParser
from circlecircle2.core.fea.lsdyna.parser.parameter_parser import ParameterParser
from circlecircle2.core.fea.lsdyna.parser.node_parser import NodeParser
from circlecircle2.core.fea.lsdyna.parser.element_shell_parser import ElementShellParser
from circlecircle2.core.fea.lsdyna.parser.element_solid_parser import ElementSolidParser
from circlecircle2.core.fea.lsdyna.parser.part_parser import PartParser
from circlecircle2.core.fea.lsdyna.parser.part_inertia_parser import PartInertiaParser
from circlecircle2.core.fea.lsdyna.parser.section_shell_parser import SectionShellParser
from circlecircle2.core.fea.lsdyna.parser.section_shell_title_parser import SectionShellTitleParser
from circlecircle2.core.fea.lsdyna.parser.section_solid_parser import SectionSolidParser
from circlecircle2.core.fea.lsdyna.parser.section_solid_title_parser import SectionSolidTitleParser
from circlecircle2.core.fea.lsdyna.parser.hourglass_parser import HourglassParser
from circlecircle2.core.fea.lsdyna.parser.hourglass_title_parser import HourglassTitleParser
from circlecircle2.core.fea.lsdyna.parser.set_node_list_parser import SetNodeListParser
from circlecircle2.core.fea.lsdyna.parser.set_node_list_title_parser import SetNodeListTitleParser
from circlecircle2.core.fea.lsdyna.parser.set_shell_list_parser import SetShellListParser
from circlecircle2.core.fea.lsdyna.parser.set_shell_list_title_parser import SetShellListTitleParser
from circlecircle2.core.fea.lsdyna.parser.set_part_list_parser import SetPartListParser
from circlecircle2.core.fea.lsdyna.parser.set_part_list_title_parser import SetPartListTitleParser
from circlecircle2.core.fea.lsdyna.parser.set_part_list_generate_parser import SetPartListGenerateParser
from circlecircle2.core.fea.lsdyna.parser.database_history_node_parser import DatabaseHistoryNodeParser
from circlecircle2.core.fea.lsdyna.parser.database_history_node_title_parser import DatabaseHistoryNodeTitleParser
from circlecircle2.core.fea.lsdyna.parser.mat_elastic_parser import MatElasticParser
from circlecircle2.core.fea.lsdyna.parser.mat_elastic_title_parser import MatElasticTitleParser
from circlecircle2.core.fea.lsdyna.parser.mat_rigid_parser import MatRigidParser
from circlecircle2.core.fea.lsdyna.parser.mat_rigid_title_parser import MatRigidTitleParser
from circlecircle2.core.fea.lsdyna.parser.mat_piecewise_linear_plasticity_log_interpolation_parser import MatPiecewiseLinearPlasticityLogInterpolationParser
from circlecircle2.core.fea.lsdyna.parser.mat_piecewise_linear_plasticity_log_interpolation_title_parser import MatPiecewiseLinearPlasticityLogInterpolationTitleParser
from circlecircle2.core.fea.lsdyna.parser.mat_modified_piecewise_linear_plasticity_parser import MatModifiedPiecewiseLinearPlasticityParser
from circlecircle2.core.fea.lsdyna.parser.mat_modified_piecewise_linear_plasticity_title_parser import MatModifiedPiecewiseLinearPlasticityTitleParser
from circlecircle2.core.fea.lsdyna.parser.mat_barlat_yld2000_parser import MatBarlatYld2000Parser
from circlecircle2.core.fea.lsdyna.parser.mat_barlat_yld2000_title_parser import MatBarlatYld2000TitleParser
from circlecircle2.core.fea.lsdyna.parser.define_curve_parser import DefineCurveParser
from circlecircle2.core.fea.lsdyna.parser.define_curve_title_parser import DefineCurveTitleParser
from circlecircle2.core.fea.lsdyna.parser.define_table_parser import DefineTableParser
from circlecircle2.core.fea.lsdyna.parser.define_table_title_parser import DefineTableTitleParser
from circlecircle2.core.fea.lsdyna.parser.define_table_2d_parser import DefineTable2DParser
from circlecircle2.core.fea.lsdyna.parser.define_table_2d_title_parser import DefineTable2DTitleParser
from circlecircle2.core.fea.lsdyna.parser.mat_add_erosion_parser import MatAddErosionParser
from circlecircle2.core.fea.lsdyna.parser.mat_add_erosion_title_parser import MatAddErosionTitleParser
from circlecircle2.core.fea.lsdyna.parser.constrained_extra_nodes_set_parser import ConstrainedExtraNodesSetParser
from circlecircle2.core.fea.lsdyna.parser.constrained_extra_nodes_set_title_parser import ConstrainedExtraNodesSetTitleParser
from circlecircle2.core.fea.lsdyna.parser.constrained_nodal_rigid_body_parser import ConstrainedNodalRigidBodyParser
from circlecircle2.core.fea.lsdyna.parser.constrained_nodal_rigid_body_title_parser import ConstrainedNodalRigidBodyTitleParser
from circlecircle2.core.fea.lsdyna.parser.database_cross_section_plane_id_parser import DatabaseCrossSectionPlaneIDParser
from circlecircle2.core.fea.lsdyna.parser.contact_automatic_surface_to_surface_id_parser import ContactAutomaticSurfaceToSurfaceIDParser
from circlecircle2.core.fea.lsdyna.parser.contact_automatic_surface_to_surface_id_title_parser import ContactAutomaticSurfaceToSurfaceIDTitleParser
from circlecircle2.core.fea.lsdyna.parser.contact_automatic_single_surface_id_parser import ContactAutomaticSingleSurfaceIDParser
from circlecircle2.core.fea.lsdyna.parser.contact_automatic_single_surface_id_title_parser import ContactAutomaticSingleSurfaceIDTitleParser
from circlecircle2.core.fea.lsdyna.parser.initial_velocity_generation_parser import InitialVelocityGenerationParser
from circlecircle2.core.fea.lsdyna.parser.initial_velocity_generation_title_parser import InitialVelocityGenerationTitleParser
from circlecircle2.core.fea.lsdyna.parser.boundary_prescribed_motion_rigid_parser import BoundaryPrescribedMotionRigidParser
from circlecircle2.core.fea.lsdyna.parser.title_parser import TitleParser
from circlecircle2.core.fea.lsdyna.parser.database_deforc_parser import DatabaseDeforcParser
from circlecircle2.core.fea.lsdyna.parser.database_jntforc_parser import DatabaseJntforcParser
from circlecircle2.core.fea.lsdyna.parser.database_format_parser import DatabaseFormatParser
from circlecircle2.core.fea.lsdyna.parser.control_shell_parser import ControlShellParser
from circlecircle2.core.fea.lsdyna.parser.database_abstat_parser import DatabaseAbstatParser
from circlecircle2.core.fea.lsdyna.parser.database_swforc_parser import DatabaseSwforcParser
from circlecircle2.core.fea.lsdyna.parser.database_rwforc_parser import DatabaseRwforcParser
from circlecircle2.core.fea.lsdyna.parser.database_sleout_parser import DatabaseSleoutParser
from circlecircle2.core.fea.lsdyna.parser.database_elout_parser import DatabaseEloutParser
from circlecircle2.core.fea.lsdyna.parser.database_matsum_parser import DatabaseMatsumParser
from circlecircle2.core.fea.lsdyna.parser.database_nodout_parser import DatabaseNodoutParser
from circlecircle2.core.fea.lsdyna.parser.database_binary_intfor_parser import DatabaseBinaryIntforParser
from circlecircle2.core.fea.lsdyna.parser.control_dynamic_relaxation_parser import ControlDynamicRelaxationParser
from circlecircle2.core.fea.lsdyna.parser.end_parser import EndParser


class LsDyna(Solver):
    def __init__(self):
        self.logger = logger

        # must parse first, and only one keyword: *PARAMETER
        self.parse_keywords_initial = {
            "*PARAMETER": ParameterParser(),
        }

        self.parse_keywords_1 = {
            "*KEYWORD": KeyWordParser(),
            "*NODE": NodeParser(),
            "*SECTION_SHELL": SectionShellParser(),
            "*SECTION_SHELL_TITLE": SectionShellTitleParser(),
            "*SECTION_SOLID": SectionSolidParser(),
            "*SECTION_SOLID_TITLE": SectionSolidTitleParser(),
            "*HOURGLASS": HourglassParser(),
            "*HOURGLASS_TITLE": HourglassTitleParser(),
            "*SET_NODE_LIST": SetNodeListParser(),
            "*SET_NODE_LIST_TITLE": SetNodeListTitleParser(),
            "*SET_SHELL_LIST": SetShellListParser(),
            "*SET_SHELL_LIST_TITLE": SetShellListTitleParser(),
            "*SET_PART_LIST": SetPartListParser(),
            "*SET_PART_LIST_TITLE": SetPartListTitleParser(),
            "*SET_PART_LIST_GENERATE": SetPartListGenerateParser(),
            "*DATABASE_HISTORY_NODE": DatabaseHistoryNodeParser(),
            "*DATABASE_HISTORY_NODE_TITLE": DatabaseHistoryNodeTitleParser(),
            "*DEFINE_CURVE": DefineCurveParser(),
            "*DEFINE_CURVE_TITLE": DefineCurveTitleParser(),
            "*DEFINE_TABLE": DefineTableParser(),
            "*DEFINE_TABLE_TITLE": DefineTableTitleParser(),
            "*DEFINE_TABLE_2D": DefineTable2DParser(),
            "*DEFINE_TABLE_2D_TITLE": DefineTable2DTitleParser(),
            "*INITIAL_VELOCITY_GENERATION": InitialVelocityGenerationParser(),
            "*INITIAL_VELOCITY_GENERATION_TITLE": InitialVelocityGenerationTitleParser(),
            "*BOUNDARY_PRESCRIBED_MOTION_RIGID": BoundaryPrescribedMotionRigidParser(),
            "*TITLE": TitleParser(),
            "*DATABASE_DEFORC": DatabaseDeforcParser(),
            "*DATABASE_JNTFORC": DatabaseJntforcParser(),
            "*DATABASE_FORMAT": DatabaseFormatParser(),
            "*CONTROL_SHELL": ControlShellParser(),
            "*DATABASE_ABSTAT": DatabaseAbstatParser(),
            "*DATABASE_SWFORC": DatabaseSwforcParser(),
            "*DATABASE_RWFORC": DatabaseRwforcParser(),
            "*DATABASE_SLEOUT": DatabaseSleoutParser(),
            "*DATABASE_ELOUT": DatabaseEloutParser(),
            "*DATABASE_MATSUM": DatabaseMatsumParser(),
            "*DATABASE_NODOUT": DatabaseNodoutParser(),
            "*DATABASE_BINARY_INTFOR": DatabaseBinaryIntforParser(),
            "*CONTROL_DYNAMIC_RELAXATION": ControlDynamicRelaxationParser(),
            "*END": EndParser(),
        }

        self.parse_keywords_2 = {
            "*ELEMENT_SHELL": ElementShellParser(),
            "*ELEMENT_SOLID": ElementSolidParser(),
            "*PART": PartParser(),
            "*PART_INERTIA": PartInertiaParser(),
            "*MAT_ELASTIC": MatElasticParser(),
            "*MAT_ELASTIC_TITLE": MatElasticTitleParser(),
            "*MAT_RIGID": MatRigidParser(),
            "*MAT_RIGID_TITLE": MatRigidTitleParser(),
            "*MAT_PIECEWISE_LINEAR_PLASTICITY_LOG_INTERPOLATION": MatPiecewiseLinearPlasticityLogInterpolationParser(),
            "*MAT_PIECEWISE_LINEAR_PLASTICITY_LOG_INTERPOLATION_TITLE": MatPiecewiseLinearPlasticityLogInterpolationTitleParser(),
            "*MAT_MODIFIED_PIECEWISE_LINEAR_PLASTICITY": MatModifiedPiecewiseLinearPlasticityParser(),
            "*MAT_MODIFIED_PIECEWISE_LINEAR_PLASTICITY_TITLE": MatModifiedPiecewiseLinearPlasticityTitleParser(),
            "*MAT_BARLAT_YLD2000": MatBarlatYld2000Parser(),
            "*MAT_BARLAT_YLD2000_TITLE": MatBarlatYld2000TitleParser(),
            "*MAT_ADD_EROSION": MatAddErosionParser(),
            "*MAT_ADD_EROSION_TITLE": MatAddErosionTitleParser(),
            "*CONSTRAINED_EXTRA_NODES_SET": ConstrainedExtraNodesSetParser(),
            "*CONSTRAINED_EXTRA_NODES_SET_TITLE": ConstrainedExtraNodesSetTitleParser(),
            "*CONSTRAINED_NODAL_RIGID_BODY": ConstrainedNodalRigidBodyParser(),
            "*CONSTRAINED_NODAL_RIGID_BODY_TITLE": ConstrainedNodalRigidBodyTitleParser(),
            "*DATABASE_CROSS_SECTION_PLANE_ID": DatabaseCrossSectionPlaneIDParser(),
            "*CONTACT_AUTOMATIC_SURFACE_TO_SURFACE_ID": ContactAutomaticSurfaceToSurfaceIDParser(),
            "*CONTACT_AUTOMATIC_SURFACE_TO_SURFACE_ID_TITLE": ContactAutomaticSurfaceToSurfaceIDTitleParser(),
            "*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID": ContactAutomaticSingleSurfaceIDParser(),
            "*CONTACT_AUTOMATIC_SINGLE_SURFACE_ID_TITLE": ContactAutomaticSingleSurfaceIDTitleParser(),
        }
        self.translate_keywords = {}
        self.not_support_keywords = set()

        self.current_parser = None

    def reset(self):
        self.current_parser = None
        self.not_support_keywords.clear()

    def parse_data(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        version = kwargs.get("version", args[1] if len(args) > 1 else None)
        parse_keywords = kwargs.get("parse_keywords", args[2] if len(args) > 2 else None)

        if file_path:
            with open(file=file_path, mode="r", encoding="utf-8", errors="ignore") as f:
                try:
                    for line in f:

                        if not line or line.startswith("$"):
                            continue

                        if line.startswith("*"):
                            dyna_keyword = line.split()[0].strip().upper()

                            if dyna_keyword in parse_keywords:
                                self.current_parser = parse_keywords[dyna_keyword]
                                self.current_parser.reset()
                                continue
                            else:
                                if dyna_keyword in self.parse_keywords_initial:
                                    self.current_parser = None
                                    continue

                                elif dyna_keyword in self.parse_keywords_1:
                                    self.current_parser = None
                                    continue

                                elif dyna_keyword in self.parse_keywords_2:
                                    self.current_parser = None
                                    continue

                                else:
                                    self.not_support_keywords.add(dyna_keyword)
                                    self.current_parser = None
                                    continue

                        elif line.strip().strip("-") == "BEGIN PGP MESSAGE":
                            dyna_keyword = "BEGIN PGP MESSAGE"

                            if dyna_keyword in parse_keywords:
                                self.current_parser = parse_keywords[dyna_keyword]
                                continue
                            else:
                                self.current_parser = None
                                continue

                        elif line.strip().strip("-") == "END PGP MESSAGE":
                            self.current_parser = None
                            continue

                        else:
                            if self.current_parser is not None:
                                self.current_parser.parse(line_raw=line, version=version)

                except Exception as e:
                    raise e

        else:
            self.logger.error(f"LS-DYNA PARSER ERROR: file_path cannot be empty\n")

    def parse(self, *args, **kwargs):
        file_path = kwargs.get("file_path", args[0] if len(args) > 0 else None)
        version = kwargs.get("version", args[1] if len(args) > 1 else None)

        self.parse_data(file_path=file_path, version=version, parse_keywords=self.parse_keywords_initial)
        self.parse_data(file_path=file_path, version=version, parse_keywords=self.parse_keywords_1)
        self.parse_data(file_path=file_path, version=version, parse_keywords=self.parse_keywords_2)

        # if file_path:
        #     with open(file=file_path, mode="r", encoding="utf-8", errors="ignore") as f:
        #         try:
        #             for line in f:
        #
        #                 if not line or line.startswith("$"):
        #                     continue
        #
        #                 if line.startswith("*"):
        #                     dyna_keyword = line.split()[0].strip().upper()
        #
        #                     if dyna_keyword in self.parse_keywords:
        #                         self.current_parser = self.parse_keywords[dyna_keyword]
        #                         self.current_parser.reset()
        #                         continue
        #                     else:
        #                         if dyna_keyword in self.parse_keywords_initial:
        #                             continue
        #                         else:
        #                             self.not_support_keywords.add(dyna_keyword)
        #                             self.current_parser = None
        #                             continue
        #
        #                 elif line.strip().strip("-") == "BEGIN PGP MESSAGE":
        #                     dyna_keyword = "BEGIN PGP MESSAGE"
        #
        #                     if dyna_keyword in self.parse_keywords:
        #                         self.current_parser = self.parse_keywords[dyna_keyword]
        #                         continue
        #
        #                 elif line.strip().strip("-") == "END PGP MESSAGE":
        #                     self.current_parser = None
        #                     continue
        #
        #                 else:
        #                     if self.current_parser is not None:
        #                         self.current_parser.parse(line_raw=line, version=version)
        #
        #         except Exception as e:
        #             raise e

        for not_support_keyword in self.not_support_keywords:
            self.logger.warning(f"Ls-Dyna not support keywords: {not_support_keyword}")

    def translate(self, file_path):
        print(f"lsdyna translate")
