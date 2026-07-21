from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.element_shell import ElementShell


class ElementShellParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        uid_raw = line_raw[0:8].strip()
        pid_raw = line_raw[8:16].strip()
        n1_raw = line_raw[16:24].strip()
        n2_raw = line_raw[24:32].strip()
        n3_raw = line_raw[32:40].strip()
        n4_raw = line_raw[40:48].strip()

        uid = self.dataframe.parameter[uid_raw[1:]].value if uid_raw.startswith("&") else int(uid_raw)
        pid = self.dataframe.parameter[pid_raw[1:]].value if pid_raw.startswith("&") else int(pid_raw)
        n1 = self.dataframe.parameter[n1_raw[1:]].value if n1_raw.startswith("&") else int(n1_raw)
        n2 = self.dataframe.parameter[n2_raw[1:]].value if n2_raw.startswith("&") else int(n2_raw)
        n3 = self.dataframe.parameter[n3_raw[1:]].value if n3_raw.startswith("&") else int(n3_raw)
        n4 = self.dataframe.parameter[n4_raw[1:]].value if n4_raw.startswith("&") else int(n4_raw)

        self.dataframe.element_shell[uid] = ElementShell(uid=uid,
                                                         pid=pid,
                                                         n1=n1,
                                                         n2=n2,
                                                         n3=n3,
                                                         n4=n4)
        self.dataframe.element_shell_tensor.append([uid, pid, n1, n2, n3, n4])

        self.dataframe.storge_part_element.setdefault(pid, [])
        self.dataframe.storge_part_element[pid].append(self.dataframe.element_shell[uid])

        self.dataframe.storge_part_node_xyz.setdefault(pid, set())
        self.dataframe.storge_part_node_xyz[pid].add(self.dataframe.node[n1].xyz)
        self.dataframe.storge_part_node_xyz[pid].add(self.dataframe.node[n2].xyz)
        self.dataframe.storge_part_node_xyz[pid].add(self.dataframe.node[n3].xyz)
        self.dataframe.storge_part_node_xyz[pid].add(self.dataframe.node[n4].xyz)

        self.dataframe.storge_part_node_id.setdefault(pid, set())
        self.dataframe.storge_part_node_id[pid].add(self.dataframe.node[n1].uid)
        self.dataframe.storge_part_node_id[pid].add(self.dataframe.node[n2].uid)
        self.dataframe.storge_part_node_id[pid].add(self.dataframe.node[n3].uid)
        self.dataframe.storge_part_node_id[pid].add(self.dataframe.node[n4].uid)

        self.reset()
