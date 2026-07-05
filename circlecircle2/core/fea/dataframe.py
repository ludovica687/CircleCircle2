class DataFrame:
    """
    base data storge for fea
    typically used for fea keywords files
    """

    def __init__(self):
        self.solver = None

        self.storge = {
            "keyword": {},
            "parameter": {},
            "node": {},
            "element_shell": {},
            "element_solid": {},
            "part": {},
            "material": {},
            "section_shell": {},
            "section_solid": {},
            "section_beam": {},
            "end": {},
        }

        self.storge_tensor = {
            "node_ids": [],
            "node_xyz": [],
            "element_shell": [],
            "element_solid": [],
            "element_solid_surface": [],
            "part": [],
        }

        self.output_storge = {}

    def reset(self):
        self.solver = None

        for sub_dict in self.storge.values():
            sub_dict.clear()

        self.output_storge.clear()

    # for fea parser
    @property
    def keyword(self):
        return self.storge["keyword"]

    @property
    def parameter(self):
        return self.storge["parameter"]

    @property
    def node(self):
        return self.storge["node"]

    @property
    def element_shell(self):
        return self.storge["element_shell"]

    @property
    def element_solid(self):
        return self.storge["element_solid"]

    @property
    def part(self):
        return self.storge["part"]

    @property
    def material(self):
        return self.storge["material"]

    @property
    def section_shell(self):
        return self.storge["section_shell"]

    @property
    def section_solid(self):
        return self.storge["section_solid"]

    @property
    def section_beam(self):
        return self.storge["section_beam"]

    @property
    def end(self):
        return self.storge["end"]

    # for nn model data
    # tensor
    @property
    def node_id_tensor(self):
        return self.storge_tensor["node_ids"]

    @property
    def node_xyz_tensor(self):
        return self.storge_tensor["node_xyz"]

    @property
    def element_shell_tensor(self):
        return self.storge_tensor["element_shell"]

    @property
    def element_solid_tensor(self):
        return self.storge_tensor["element_solid"]

    @property
    def element_solid_surface_tensor(self):
        """
        format: [[-1, pid, n1, n2, n3, n4], [-1, pid, n1, n2, n3, n4], [-1, pid, n1, n2, n3, n4], ...]
        """
        return self.storge_tensor["element_solid_surface"]

    @property
    def part_tensor(self):
        return self.storge_tensor["part"]

    @property
    def part_name_mapping(self):
        m_dict = {}

        for pid, part in self.storge["part"].items():
            m_dict[pid] = part.name.lower()

        return m_dict


dataframe = DataFrame()
