class AFD:
    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = estados
        self.alfabeto = alfabeto
        self.inicial = inicial
        self.finales = finales
        self.transiciones = transiciones

    def validar(self, cadena):
        estado = self.inicial
        recorrido = [estado]

        for c in cadena:
            if c not in self.alfabeto:
                return False, recorrido, f"Símbolo inválido: {c}"

            if (estado, c) not in self.transiciones:
                return False, recorrido, "Transición no definida"

            estado = self.transiciones[(estado, c)]
            recorrido.append(estado)

        return estado in self.finales, recorrido, "OK"