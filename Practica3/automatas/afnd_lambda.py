from automatas.afnd import AFND

class AFNDLambda(AFND):

    def lambda_clausura(self, estados):
        stack = list(estados)
        clausura = set(estados)

        while stack:
            estado = stack.pop()
            if (estado, "λ") in self.transiciones:
                for d in self.transiciones[(estado, "λ")]:
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
                    nuevos.update(self.transiciones[(estado, c)])

            actuales = self.lambda_clausura(nuevos)
            recorrido.append(actuales.copy())

        return any(e in self.finales for e in actuales), recorrido