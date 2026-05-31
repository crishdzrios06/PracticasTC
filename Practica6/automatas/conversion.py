"""
Conversiones entre tipos de autómatas
========================================
"""


LAMBDA = "λ"


def convertir_afnd_a_afd(afnd):
    """Algoritmo de subconjuntos."""

    inicial = frozenset([afnd.inicial])
    estados = {inicial}
    trans = {}
    finales = set()
    pendientes = [inicial]

    while pendientes:
        actual = pendientes.pop()

        for simbolo in afnd.alfabeto:
            if simbolo == LAMBDA:
                continue

            nuevo = set()

            for e in actual:
                if (e, simbolo) in afnd.transiciones:
                    destinos = afnd.transiciones[(e, simbolo)]

                    if not isinstance(destinos, (list, set)):
                        destinos = [destinos]

                    nuevo.update(destinos)

            nuevo = frozenset(nuevo)

            if nuevo:
                trans[(actual, simbolo)] = nuevo

                if nuevo not in estados:
                    estados.add(nuevo)
                    pendientes.append(nuevo)

    for e in estados:
        if any(x in afnd.finales for x in e):
            finales.add(e)

    return estados, inicial, finales, trans


def eliminar_lambda(afndl):
    """
    Convierte un AFND-λ en un AFND estándar (sin transiciones λ).
    """
    nuevas_trans = {}

    for estado in afndl.estados:
        clausura = afndl.lambda_clausura({estado})

        for simbolo in afndl.alfabeto:
            if simbolo == LAMBDA:
                continue

            destinos = set()

            for e in clausura:
                if (e, simbolo) in afndl.transiciones:
                    dest = afndl.transiciones[(e, simbolo)]

                    if not isinstance(dest, (list, set)):
                        dest = [dest]

                    for d in dest:
                        destinos.update(
                            afndl.lambda_clausura({d})
                        )

            if destinos:
                nuevas_trans[(estado, simbolo)] = list(destinos)

    nuevos_finales = set()

    for estado in afndl.estados:
        clausura = afndl.lambda_clausura({estado})
        if any(e in afndl.finales for e in clausura):
            nuevos_finales.add(estado)

    return (
        afndl.estados,
        afndl.alfabeto - {LAMBDA},
        afndl.inicial,
        nuevos_finales,
        nuevas_trans
    )
