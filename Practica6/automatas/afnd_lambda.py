"""
AFND-λ - Autómata Finito No Determinista con Transiciones Lambda
=====================================================================
"""

from automatas.afnd import AFND


LAMBDA = "λ"


class AFNDLambda(AFND):

    def lambda_clausura(self, estados):
        """λ-clausura: todos los estados alcanzables solo con λ."""
        stack = list(estados)
        clausura = set(estados)

        while stack:
            estado = stack.pop()

            if (estado, LAMBDA) in self.transiciones:
                destinos = self.transiciones[(estado, LAMBDA)]

                if not isinstance(destinos, (list, set)):
                    destinos = [destinos]

                for d in destinos:
                    if d not in clausura:
                        clausura.add(d)
                        stack.append(d)

        return clausura

    def validar(self, cadena):
        actuales = self.lambda_clausura({self.inicial})
        recorrido = [actuales.copy()]

        for c in cadena:
            nuevos = set()

            for estado in actuales:
                if (estado, c) in self.transiciones:
                    destinos = self.transiciones[(estado, c)]

                    if not isinstance(destinos, (list, set)):
                        destinos = [destinos]

                    nuevos.update(destinos)

            actuales = self.lambda_clausura(nuevos)
            recorrido.append(actuales.copy())

        aceptada = any(e in self.finales for e in actuales)
        return aceptada, recorrido

    def simular_paso_a_paso(self, cadena):
        actuales = self.lambda_clausura({self.inicial})

        pasos = [{
            "paso": 0,
            "estados": sorted(actuales),
            "simbolo": "Inicio + λ-clausura",
            "leido": "",
            "restante": cadena
        }]

        for i, c in enumerate(cadena):
            nuevos = set()

            for estado in actuales:
                if (estado, c) in self.transiciones:
                    destinos = self.transiciones[(estado, c)]

                    if not isinstance(destinos, (list, set)):
                        destinos = [destinos]

                    nuevos.update(destinos)

            actuales = self.lambda_clausura(nuevos)

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
