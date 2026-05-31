"""
AFD - Autómata Finito Determinista
====================================
M = (Q, Σ, δ, q0, F)
"""


class AFD:

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

    # Alias para compatibilidad con código antiguo
    @property
    def estado_inicial(self):
        return self.inicial

    @property
    def estados_finales(self):
        return self.finales

    def validar(self, cadena):
        estado = self.inicial
        recorrido = [estado]

        for c in cadena:

            if c not in self.alfabeto:
                return (
                    False,
                    recorrido,
                    f"Símbolo inválido: {c}"
                )

            if (estado, c) not in self.transiciones:
                return (
                    False,
                    recorrido,
                    f"Transición no definida desde "
                    f"{estado} con '{c}'"
                )

            estado = self.transiciones[(estado, c)]
            recorrido.append(estado)

        return estado in self.finales, recorrido, "OK"

    def simular_paso_a_paso(self, cadena):
        """
        Devuelve una lista de pasos con la traza detallada.
        """
        pasos = [{
            "paso": 0,
            "estado": self.inicial,
            "leido": "",
            "restante": cadena,
            "simbolo": "Inicio",
            "ok": True
        }]

        estado = self.inicial

        for i, c in enumerate(cadena):

            if (estado, c) not in self.transiciones:
                pasos.append({
                    "paso": i + 1,
                    "estado": estado,
                    "leido": cadena[:i + 1],
                    "restante": cadena[i + 1:],
                    "simbolo": c,
                    "ok": False,
                    "error": "Sin transición definida"
                })
                return False, pasos

            estado = self.transiciones[(estado, c)]
            pasos.append({
                "paso": i + 1,
                "estado": estado,
                "leido": cadena[:i + 1],
                "restante": cadena[i + 1:],
                "simbolo": c,
                "ok": True
            })

        aceptada = estado in self.finales
        return aceptada, pasos
