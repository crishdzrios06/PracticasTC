"""
Minimización de AFD (algoritmo de las clases de equivalencia)
=================================================================
"""


def eliminar_inaccesibles(afd):
    visitados = set()
    stack = [afd.inicial]

    while stack:
        estado = stack.pop()

        if estado not in visitados:
            visitados.add(estado)

            for c in afd.alfabeto:
                if (estado, c) in afd.transiciones:
                    stack.append(
                        afd.transiciones[(estado, c)]
                    )

    return visitados


def minimizar_afd(afd):
    """
    Devuelve:
      nuevos_estados (lista de frozenset),
      nuevo_inicial (frozenset),
      nuevos_finales (set de frozenset),
      nuevas_trans (dict),
      tabla_distinguibles (dict)
    """

    accesibles = eliminar_inaccesibles(afd)
    estados = list(accesibles)

    if not estados:
        return [], None, set(), {}, {}

    tabla = {}

    # Paso 1: pares distinguibles inicialmente (final vs no final)
    for i in range(len(estados)):
        for j in range(i):
            p, q = estados[i], estados[j]
            key = tuple(sorted([p, q]))
            tabla[key] = (
                (p in afd.finales) != (q in afd.finales)
            )

    # Paso 2: propagación
    cambio = True
    while cambio:
        cambio = False

        for (p, q) in list(tabla.keys()):
            if tabla[(p, q)]:
                continue

            for s in afd.alfabeto:
                p1 = afd.transiciones.get((p, s))
                q1 = afd.transiciones.get((q, s))

                if p1 is None and q1 is None:
                    continue

                if (p1 is None) != (q1 is None):
                    tabla[(p, q)] = True
                    cambio = True
                    break

                if p1 == q1:
                    continue

                key = tuple(sorted([p1, q1]))
                if key in tabla and tabla[key]:
                    tabla[(p, q)] = True
                    cambio = True
                    break

    # Paso 3: agrupar equivalentes
    grupos = []
    usados = set()

    for estado in estados:
        if estado in usados:
            continue

        grupo = {estado}

        for otro in estados:
            if otro != estado and otro not in usados:
                key = tuple(sorted([estado, otro]))
                if key in tabla and not tabla[key]:
                    grupo.add(otro)

        usados.update(grupo)
        grupos.append(grupo)

    # Paso 4: construir nuevo AFD
    nuevos_estados = [frozenset(g) for g in grupos]
    nuevo_inicial = next(
        g for g in nuevos_estados if afd.inicial in g
    )
    nuevos_finales = {
        g for g in nuevos_estados
        if any(e in afd.finales for e in g)
    }

    nuevas_trans = {}

    for g in nuevos_estados:
        representante = next(iter(g))

        for s in afd.alfabeto:
            if (representante, s) in afd.transiciones:
                destino = afd.transiciones[(representante, s)]

                for grupo_dest in nuevos_estados:
                    if destino in grupo_dest:
                        nuevas_trans[(g, s)] = grupo_dest
                        break

    return (
        nuevos_estados,
        nuevo_inicial,
        nuevos_finales,
        nuevas_trans,
        tabla
    )
