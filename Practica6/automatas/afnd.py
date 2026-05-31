"""
AFND - Autómata Finito No Determinista
=========================================
"""


class AFND:

    def __init__(
        self,
        estados,
        alfabeto,
        inicial,
        finales,
        transiciones
    ):
        self.estados = set(estados)
        self.alfabeto = set(alfabeto)
        self.inicial = inicial
        self.finales = set(finales)
        self.transiciones = transiciones

    def validar(self, cadena):
        actuales = {self.inicial}
        recorrido = [actuales.copy()]

        for c in cadena:
            nuevos = set()

            for estado in actuales:
                if (estado, c) in self.transiciones:
                    destinos = self.transiciones[(estado, c)]

                    if isinstance(destinos, (list, set)):
                        nuevos.update(destinos)
                    else:
                        nuevos.add(destinos)

            actuales = nuevos
            recorrido.append(actuales.copy())

        aceptada = any(e in self.finales for e in actuales)
        return aceptada, recorrido

    def simular_paso_a_paso(self, cadena):
        actuales = {self.inicial}

        pasos = [{
            "paso": 0,
            "estados": sorted(actuales),
            "simbolo": "Inicio",
            "leido": "",
            "restante": cadena
        }]

        for i, c in enumerate(cadena):
            nuevos = set()

            for estado in actuales:
                if (estado, c) in self.transiciones:
                    destinos = self.transiciones[(estado, c)]

                    if isinstance(destinos, (list, set)):
                        nuevos.update(destinos)
                    else:
                        nuevos.add(destinos)

            actuales = nuevos

            pasos.append({
                "paso": i + 1,
                "estados": sorted(actuales),
                "simbolo": c,
                "leido": cadena[:i + 1],
                "restante": cadena[i + 1:]
            })

            if not actuales:
                return False, pasos

        aceptada = any(e in self.finales for e in actuales)
        return aceptada, pasos
