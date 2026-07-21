from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.database_history_node import DatabaseHistoryNode


class DatabaseHistoryNodeParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        if self.line_number == 0:
            if 1 in self.dataframe.database_history_node:
                current_object = self.dataframe.database_history_node[1]
            else:
                self.dataframe.database_history_node[1] = DatabaseHistoryNode(uid=1)

            data_list = line_raw.split()

            current_object = self.dataframe.database_history_node[1]

            current_object.ids.extend(data_list)

            self.line_number = 1

            return

        if self.line_number != 0:
            data_list = line_raw.split()

            current_object = self.dataframe.database_history_node[1]

            current_object.ids.extend(data_list)

            return
