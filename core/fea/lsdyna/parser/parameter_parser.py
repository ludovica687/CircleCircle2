from circlecircle2.core.fea.parser import Parser
from circlecircle2.core.fea.lsdyna.keywords.parameter import Parameter


class ParameterParser(Parser):
    def __init__(self):
        super().__init__()

        self.version = {
            "12.0": self._12p0,
            "13.0": self._12p0,
        }

    def _12p0(self, line_raw):
        parameter_tag = line_raw[0]
        name = line_raw[1:11].strip()
        value = line_raw[11:21]

        if parameter_tag.upper() == "R":
            self.dataframe.parameter[name] = Parameter(parameter_tag, name, float(value))

        elif parameter_tag.upper() == "I":
            self.dataframe.parameter[name] = Parameter(parameter_tag, name, int(value))

        elif parameter_tag.upper() == "C":
            self.dataframe.parameter[name] = Parameter(parameter_tag, name, value)

