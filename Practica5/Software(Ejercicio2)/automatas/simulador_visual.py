class SimuladorVisual:

    def __init__(self, afd):

        self.afd = afd

    def recorrer(self, cadena):

        actual = self.afd.estado_inicial

        pasos = []

        pasos.append({
            "estado": actual,
            "simbolo": "Inicio"
        })

        for simbolo in cadena:

            clave = (actual, simbolo)

            if clave not in self.afd.transiciones:

                pasos.append({
                    "estado": actual,
                    "simbolo": simbolo,
                    "error": True
                })

                return False, pasos

            actual = self.afd.transiciones[clave]

            pasos.append({
                "estado": actual,
                "simbolo": simbolo
            })

        aceptada = actual in self.afd.estados_finales

        return aceptada, pasos