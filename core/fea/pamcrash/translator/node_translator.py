from circlecircle2.core.fea.translator import Translator


class NodeTranslator(Translator):
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
            raise Exception(f"PAMCRASH NodeTranslator ERROR: {e}") from e

    def _2020(self):
        node_dict = self.dataframe.node

        if len(node_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("NODE", [])

            output_storge.append(
                f"$#         IDNOD               X               Y               Z\n"
            )

            for nid, node in node_dict.items():
                x = node.x
                y = node.y
                z = node.z

                output_storge.append(f"NODE  /{nid:>9}{x:>16}{y:>16}{z:>16}\n")
