from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.node import Node


class NodeParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        uid_raw = line_raw[0:8].strip()
        x_raw = line_raw[8:24].strip()
        y_raw = line_raw[24:40].strip()
        z_raw = line_raw[40:56].strip()

        uid = self.dataframe.parameter[uid_raw[1:]].value if uid_raw.startswith("&") else int(uid_raw)
        x = self.dataframe.parameter[x_raw[1:]].value if x_raw.startswith("&") else float(x_raw)
        y = self.dataframe.parameter[y_raw[1:]].value if y_raw.startswith("&") else float(y_raw)
        z = self.dataframe.parameter[z_raw[1:]].value if z_raw.startswith("&") else float(z_raw)

        self.dataframe.node[uid] = Node(uid=uid, x=x, y=y, z=z)
        self.dataframe.node_tensor.append([uid, x, y, z])
        self.dataframe.storge_node_id.append(uid)

        self.reset()

