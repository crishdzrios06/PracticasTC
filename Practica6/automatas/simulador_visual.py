"""
Simulador visual de AFD (bug del original corregido).
"""


class SimuladorVisual:

    def __init__(self, afd):
        self.afd = afd

    def recorrer(self, cadena):
        actual = self.afd.inicial
        pasos = []

        pasos.append({
            "estado": actual,
            "simbolo": "Inicio",
            "ok": True
        })

        for simbolo in cadena:
            clave = (actual, simbolo)

            if clave not in self.afd.transiciones:
                pasos.append({
                    "estado": actual,
                    "simbolo": simbolo,
                    "ok": False,
                    "error": True
                })
                return False, pasos

            actual = self.afd.transiciones[clave]

            pasos.append({
                "estado": actual,
                "simbolo": simbolo,
                "ok": True
            })

        aceptada = actual in self.afd.finales
        return aceptada, pasos
