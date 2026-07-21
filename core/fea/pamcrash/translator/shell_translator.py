from circlecircle2.core.fea.translator import Translator


class ShellTranslator(Translator):
    def __init__(self):
        super().__init__()

        self.version = {
            "2020": self._2020,
        }

    def translate(self, version):
        try:
            if version in self.version:
                self.version[version]()

        except Exception as e:
            raise Exception(f"PAMCRASH ShellTranslator ERROR: {e}") from e

    def _2020(self):
        element_shell_dict = self.dataframe.element_shell

        if len(element_shell_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("SHELL", [])

            for eid, element in element_shell_dict.items():
                pid = element.pid
                n1 = element.n1
                n2 = element.n2
                n3 = element.n3
                n4 = element.n4

                output_storge.append(
                    f"SHELL /{eid:>9}{pid:>8}{n1:>8}{n2:>8}{n3:>8}{n4:>8}\n"
                )
