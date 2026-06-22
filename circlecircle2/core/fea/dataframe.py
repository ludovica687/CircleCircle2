class DataFrame:
    """
    base data storge for fea
    typically used for fea keywords files
    """

    def __init__(self):
        self.solver = None

        self._storge = {
            "node": {},
            "element_shell": {},
            "element_solid": {},
            "part": {},
            "material": {}
        }

    def reset(self):
        self.solver = None

        for sub_dict in self._storge.values():
            sub_dict.clear()

    @property
    def node(self):
        return self._storge["node"]

    @property
    def element_shell(self):
        return self._storge["element_shell"]

    @property
    def element_solid(self):
        return self._storge["element_solid"]

    @property
    def part(self):
        return self._storge["part"]

    @property
    def material(self):
        return self._storge["material"]


dataframe = DataFrame()
