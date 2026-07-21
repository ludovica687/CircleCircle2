from circlecircle2.core.fea.translator import Translator


class SolidTranslator(Translator):
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
            raise Exception(f"PAMCRASH SolidTranslator ERROR: {e}") from e

    def _2020(self):
        element_solid_dict = self.dataframe.element_solid

        if len(element_solid_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("SOLID", [])

            for eid, element in element_solid_dict.items():
                pid = element.pid
                n1 = element.n1
                n2 = element.n2
                n3 = element.n3
                n4 = element.n4
                n5 = element.n5
                n6 = element.n6
                n7 = element.n7
                n8 = element.n8

                element_format = element.format

                output_storge.append(f"$#          IDEL   IDPRT\n")
                output_storge.append(
                    f"$#                IDNOD1  IDNOD2  IDNOD3  IDNOD4  IDNOD5  IDNOD6  IDNOD7  IDNOD8\n"
                )

                if element_format == "tetra4":
                    output_storge.append(
                        f"TETR4 /{eid:>9}{pid:>8}{n1:>8}{n2:>8}{n3:>8}{n4:>8}\n")
                else:
                    output_storge.append(f"SOLID / {eid:>8}{pid:>8}\n")
                    output_storge.append(
                        f"                {n1:>8}{n2:>8}{n3:>8}{n4:>8}{n5:>8}{n6:>8}{n7:>8}{n8:>8}\n"
                    )
