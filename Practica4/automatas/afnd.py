class AFND:
    def __init__(self, estados, alfabeto, inicial, finales, transiciones):
        self.estados = estados
        self.alfabeto = alfabeto
        self.inicial = inicial
        self.finales = finales
        self.transiciones = transiciones

    def validar(self, cadena):
        actuales = {self.inicial}
        recorrido = [actuales.copy()]

        for c in cadena:
            nuevos = set()
            for estado in actuales:
                if (estado, c) in self.transiciones:
                    nuevos.update(self.transiciones[(estado, c)])
            actuales = nuevos
            recorrido.append(actuales.copy())

        return any(e in self.finales for e in actuales), recorrido