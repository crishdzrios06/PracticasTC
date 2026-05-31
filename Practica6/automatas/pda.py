"""
PDA (Pushdown Automaton / Autómata de Pila)
============================================
Definición formal: M = (Q, Σ, Γ, δ, q0, Z0, F)

  Q  : conjunto finito de estados
  Σ  : alfabeto de entrada
  Γ  : alfabeto de la pila
  δ  : función de transición   Q × (Σ ∪ {λ}) × Γ → P(Q × Γ*)
  q0 : estado inicial
  Z0 : símbolo inicial de la pila
  F  : conjunto de estados finales (de aceptación)

Formato interno de transiciones:
  transiciones[(estado, simbolo_entrada, simbolo_pila)] = [
        (nuevo_estado, cadena_apilar),
        ...
  ]

  - simbolo_entrada puede ser "λ" para consumir vacío
  - cadena_apilar es un string; el carácter izquierdo queda en el tope
  - cadena_apilar "" significa solo desapilar (pop) sin apilar nada
"""

from copy import deepcopy


LAMBDA = "λ"


class PDA:

    def __init__(
        self,
        estados,
        alfabeto_entrada,
        alfabeto_pila,
        inicial,
        simbolo_inicial_pila,
        finales,
        transiciones,
        modo_aceptacion="estado_final"
    ):
        """
        modo_aceptacion: "estado_final" o "pila_vacia"
        """

        self.estados = set(estados)
        self.alfabeto_entrada = set(alfabeto_entrada)
        self.alfabeto_pila = set(alfabeto_pila)
        self.inicial = inicial
        self.simbolo_inicial_pila = simbolo_inicial_pila
        self.finales = set(finales)
        self.transiciones = transiciones
        self.modo_aceptacion = modo_aceptacion

    # ------------------------------------------------------------------
    # Validación estructural
    # ------------------------------------------------------------------

    def validar_estructura(self):
        errores = []

        if self.inicial not in self.estados:
            errores.append(
                f"El estado inicial '{self.inicial}' "
                f"no existe en el conjunto de estados."
            )

        for f in self.finales:
            if f not in self.estados:
                errores.append(
                    f"El estado final '{f}' no existe."
                )

        if self.simbolo_inicial_pila not in self.alfabeto_pila:
            errores.append(
                f"El símbolo inicial de pila "
                f"'{self.simbolo_inicial_pila}' "
                f"no está en el alfabeto de pila."
            )

        for (q, a, x), destinos in self.transiciones.items():

            if q not in self.estados:
                errores.append(
                    f"Transición con estado origen desconocido: {q}"
                )

            if a != LAMBDA and a not in self.alfabeto_entrada:
                errores.append(
                    f"Transición con símbolo de entrada "
                    f"desconocido: {a}"
                )

            if x not in self.alfabeto_pila:
                errores.append(
                    f"Transición con símbolo de pila "
                    f"desconocido: {x}"
                )

            for (p, cadena) in destinos:

                if p not in self.estados:
                    errores.append(
                        f"Transición destino con estado "
                        f"desconocido: {p}"
                    )

                for c in cadena:
                    if c not in self.alfabeto_pila:
                        errores.append(
                            f"Carácter '{c}' a apilar no está "
                            f"en el alfabeto de pila."
                        )

        return errores

    # ------------------------------------------------------------------
    # Simulación
    # ------------------------------------------------------------------

    def simular(self, cadena, max_pasos=2000):
        """
        Simula la ejecución del PDA sobre la cadena de entrada.
        Devuelve (aceptada, traza_principal, todas_las_trazas)

        Usa exploración en anchura (BFS) sobre las configuraciones
        para manejar el no determinismo. Cada configuración es
        (estado, posicion_entrada, pila_tuple, traza).
        """

        pila_inicial = (self.simbolo_inicial_pila,)

        traza_inicial = [{
            "paso": 0,
            "estado": self.inicial,
            "leido": "",
            "restante": cadena,
            "pila": list(pila_inicial),
            "accion": "Inicio",
            "regla": None
        }]

        configuracion_inicial = (
            self.inicial,
            0,
            pila_inicial,
            traza_inicial
        )

        cola = [configuracion_inicial]
        visitadas = set()
        trazas_aceptacion = []
        traza_mas_larga = traza_inicial
        pasos_globales = 0

        while cola and pasos_globales < max_pasos:

            pasos_globales += 1
            estado, pos, pila, traza = cola.pop(0)

            firma = (estado, pos, pila)
            if firma in visitadas:
                continue
            visitadas.add(firma)

            if len(traza) > len(traza_mas_larga):
                traza_mas_larga = traza

            # Verificar aceptación
            if pos == len(cadena):
                if self._es_aceptacion(estado, pila):
                    trazas_aceptacion.append(traza)
                    continue

            # Expandir transiciones
            tope = pila[0] if pila else None

            siguiente_simbolo = (
                cadena[pos] if pos < len(cadena) else None
            )

            sucesores = []

            # 1) Transiciones que consumen símbolo
            if siguiente_simbolo is not None and tope is not None:
                clave = (estado, siguiente_simbolo, tope)
                if clave in self.transiciones:
                    for (np, push) in self.transiciones[clave]:
                        nueva_pila = self._aplicar_pila(
                            pila, push
                        )
                        sucesores.append((
                            np,
                            pos + 1,
                            nueva_pila,
                            siguiente_simbolo,
                            push
                        ))

            # 2) Transiciones lambda
            if tope is not None:
                clave = (estado, LAMBDA, tope)
                if clave in self.transiciones:
                    for (np, push) in self.transiciones[clave]:
                        nueva_pila = self._aplicar_pila(
                            pila, push
                        )
                        sucesores.append((
                            np,
                            pos,
                            nueva_pila,
                            LAMBDA,
                            push
                        ))

            for (np, npos, npila, simbolo_leido, push) in sucesores:

                accion = self._describir_accion(tope, push)

                nuevo_paso = {
                    "paso": len(traza),
                    "estado": np,
                    "leido": (
                        simbolo_leido
                        if simbolo_leido != LAMBDA
                        else "λ"
                    ),
                    "restante": cadena[npos:],
                    "pila": list(npila),
                    "accion": accion,
                    "regla": (
                        f"δ({estado}, {simbolo_leido}, {tope}) "
                        f"= ({np}, {push if push else 'ε'})"
                    )
                }

                nueva_traza = traza + [nuevo_paso]

                cola.append((np, npos, npila, nueva_traza))

        aceptada = len(trazas_aceptacion) > 0

        traza_principal = (
            trazas_aceptacion[0]
            if aceptada
            else traza_mas_larga
        )

        return aceptada, traza_principal, trazas_aceptacion

    # ------------------------------------------------------------------
    # Operaciones auxiliares
    # ------------------------------------------------------------------

    def _aplicar_pila(self, pila, cadena_push):
        """
        Aplica una operación de pila:
        1) Pop del tope
        2) Push de cada carácter de cadena_push, de derecha a izquierda
           para que el primer carácter quede en el tope.

        pila: tupla con el tope al inicio (índice 0)
        """
        if not pila:
            return tuple(reversed(cadena_push))

        # Pop el tope
        nueva = list(pila[1:])

        # Push (carácter izquierdo queda en el tope)
        for c in reversed(cadena_push):
            nueva.insert(0, c)

        return tuple(nueva)

    def _describir_accion(self, tope, push):
        if not push:
            return f"pop({tope})"
        if len(push) == 1 and push == tope:
            return f"nop (reemplaza {tope} por {push})"
        return f"pop({tope}) + push({push})"

    def _es_aceptacion(self, estado, pila):
        if self.modo_aceptacion == "estado_final":
            return estado in self.finales

        if self.modo_aceptacion == "pila_vacia":
            return len(pila) == 0

        return False

    # ------------------------------------------------------------------
    # Utilidad: copia
    # ------------------------------------------------------------------

    def copiar(self):
        return PDA(
            set(self.estados),
            set(self.alfabeto_entrada),
            set(self.alfabeto_pila),
            self.inicial,
            self.simbolo_inicial_pila,
            set(self.finales),
            deepcopy(self.transiciones),
            self.modo_aceptacion
        )
