from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.database_history_node import DatabaseHistoryNode


class DatabaseHistoryNodeTitleParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

        self.current_name = None

    def _12p0(self, line_raw):
        if self.line_number == 0:
            name = line_raw.strip()

            self.dataframe.database_history_node[name] = DatabaseHistoryNode(uid=1, name=name)

            self.current_name = name

            self.line_number = 1

            return

        if self.line_number == 1:

            data_list = line_raw.split()

            current_object = self.dataframe.database_history_node[self.current_name]

            current_object.ids.extend(data_list)

            self.line_number = 2

            return

        if self.line_number != 0 and self.line_number != 1:
            data_list = line_raw.split()

            current_object = self.dataframe.database_history_node[self.current_name]

            current_object.ids.extend(data_list)

            return
