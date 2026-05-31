"""
Conversión de AFD a Expresión Regular
==========================================
Método: eliminación de estados (state elimination).
"""

import copy


def afd_a_er(afd):
    """
    Recibe un objeto AFD y devuelve (pasos, expresion_regular).
    """
    estados = list(afd.estados)
    inicial = afd.inicial
    finales = afd.finales
    transiciones = afd.transiciones

    pasos = []

    # Representación R[(i,j)] = expresion para ir de i a j
    R = {}
    for (o, s), d in transiciones.items():
        # En AFD destino es un único estado
        if isinstance(d, (list, set)):
            d = next(iter(d))

        key = (o, d)
        if key not in R:
            R[key] = s
        else:
            R[key] = f"({R[key]}|{s})"

    # Crear estado inicial y final únicos artificiales
    INI = "__INI__"
    FIN = "__FIN__"

    R[(INI, inicial)] = "ε"

    for f in finales:
        R[(f, FIN)] = "ε"

    estados_extendidos = estados + [INI, FIN]
    estados_intermedios = list(estados)

    pasos.append(
        f"Estado inicial introducido: {INI}, "
        f"estado final único: {FIN}"
    )

    # Eliminar estados intermedios uno a uno
    for k in estados_intermedios:

        pasos.append(f"→ Eliminando estado: {k}")

        nuevas_R = copy.deepcopy(R)

        # rkk: bucle en k
        rkk = R.get((k, k), None)
        loop = ""

        if rkk:
            loop = (
                f"({rkk})*"
                if len(rkk) > 1 or rkk == "ε"
                else f"{rkk}*"
            )

        # Para cada par i,j que no sea k
        for i in estados_extendidos:
            if i == k:
                continue

            for j in estados_extendidos:
                if j == k:
                    continue

                rik = R.get((i, k))
                rkj = R.get((k, j))

                if rik is not None and rkj is not None:

                    rik_s = rik if rik != "ε" else ""
                    rkj_s = rkj if rkj != "ε" else ""

                    nueva = rik_s + loop + rkj_s

                    if not nueva:
                        nueva = "ε"

                    if (i, j) in nuevas_R:
                        existente = nuevas_R[(i, j)]
                        nuevas_R[(i, j)] = (
                            f"({existente}|{nueva})"
                        )
                    else:
                        nuevas_R[(i, j)] = nueva

        # Eliminar todas las transiciones que tocan k
        R = {
            (i, j): v
            for (i, j), v in nuevas_R.items()
            if i != k and j != k
        }

    er_final = R.get((INI, FIN), "∅")

    # Simplificación cosmética
    if er_final == "ε":
        er_final = "ε (cadena vacía)"

    pasos.append(f"Expresión regular final: {er_final}")

    return pasos, er_final
