from circlecircle2.core.fea.translator import Translator


class FunctTranslator(Translator):
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
            raise Exception(f"PAMCRASH FunctTranslator ERROR: {e}") from e

    def _2020(self):
        define_curve_dict = self.dataframe.define_curve

        if len(define_curve_dict) > 0:
            output_storge = self.dataframe.output_storge.setdefault("FUNCT", [])

            for curve_id, curve in define_curve_dict.items():
                sfa = curve.sfa
                sfo = curve.sfo
                offa = curve.offa
                offo = curve.offo
                name = curve.name

                a1 = curve.a1
                o1 = curve.o1

                output_storge.append(
                    f"$#         IDFUN  FUNTYP   SCALX   SCALY  SHIFTX  SHIFTY                \n"
                    f"FUNCT /{curve_id: >9}       0{sfa: >8.5f}{sfo: >8.5f}{offa: >8.5f}{offo: >8.5f}                \n"
                    f"$#   TITLE                  \n"
                    f"NAME {name}\n"
                    f"$#                             X               Y\n"
                )

                for i in range(len(a1)):
                    x = a1[i]
                    y = o1[i]

                    output_storge.append(
                        f"                {x: >16.8f}{y: >16.8f}\n"
                    )
