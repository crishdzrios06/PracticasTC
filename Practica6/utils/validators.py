"""
Validadores estructurales para autómatas.
"""


def validar_afd(estados, alfabeto, inicial, finales):
    errores = []

    if not estados:
        errores.append("El conjunto de estados está vacío.")

    if not alfabeto:
        errores.append("El alfabeto está vacío.")

    if not inicial:
        errores.append("Falta el estado inicial.")
    elif inicial not in estados:
        errores.append(
            f"El estado inicial '{inicial}' no pertenece al "
            f"conjunto de estados."
        )

    for estado in finales:
        if estado not in estados:
            errores.append(
                f"Estado final inválido: '{estado}' no existe."
            )

    return errores


def es_afd_completo(estados, alfabeto, transiciones):
    """
    Verifica que un AFD tenga transición definida para cada
    (estado, símbolo).
    """
    faltantes = []
    for e in estados:
        for s in alfabeto:
            if (e, s) not in transiciones:
                faltantes.append((e, s))
    return len(faltantes) == 0, faltantes
