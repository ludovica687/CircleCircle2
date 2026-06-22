from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.node import Node


class NodeParser(Parser):
    def __init__(self):
        super().__init__()

    def parse(self, line_raw):
        """
        :param line_raw: raw data
        :return: Node Object
        """

        uid_raw = line_raw[0:8].strip()
        x_raw = line_raw[8:24].strip()
        y_raw = line_raw[24:40].strip()
        z_raw = line_raw[40:56].strip()

        uid = uid_raw[1:] if uid_raw.startswith("&") else int(uid_raw)
        x = x_raw[1:] if x_raw.startswith("&") else float(x_raw)
        y = y_raw[1:] if y_raw.startswith("&") else float(y_raw)
        z = z_raw[1:] if z_raw.startswith("&") else float(z_raw)

        self.dataframe._storge["node"][uid] = Node(uid=uid, x=x, y=y, z=z)

