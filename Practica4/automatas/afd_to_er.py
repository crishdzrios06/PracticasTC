import copy

def afd_a_er(estados, inicial, finales, transiciones):
    estados = list(estados)
    pasos = []

    # Convertir transiciones a formato regex
    R = {}
    for (o, s), d in transiciones.items():
        R[(o, d)] = s if (o, d) not in R else f"{R[(o, d)]}|{s}"

    estados_intermedios = [e for e in estados if e != inicial and e not in finales]

    for k in estados_intermedios:
        pasos.append(f"Eliminando estado: {k}")

        nuevas_R = copy.deepcopy(R)

        for i in estados:
            for j in estados:
                if (i, k) in R and (k, j) in R:
                    rik = R[(i, k)]
                    rkk = R.get((k, k), "")
                    rkj = R[(k, j)]

                    loop = f"({rkk})*" if rkk else ""
                    nueva = f"{rik}{loop}{rkj}"

                    if (i, j) in nuevas_R:
                        nuevas_R[(i, j)] += f"|{nueva}"
                    else:
                        nuevas_R[(i, j)] = nueva

        # eliminar transiciones con k
        R = { (i,j):v for (i,j),v in nuevas_R.items() if i != k and j != k }

    # construir ER final
    expresiones = []
    for f in finales:
        if (inicial, f) in R:
            expresiones.append(R[(inicial, f)])

    er_final = "|".join(expresiones)

    return pasos, er_final