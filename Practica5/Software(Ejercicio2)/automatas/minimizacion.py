def eliminar_inaccesibles(afd):
    visitados = set()
    stack = [afd.inicial]

    while stack:
        estado = stack.pop()
        if estado not in visitados:
            visitados.add(estado)

            for c in afd.alfabeto:
                if (estado, c) in afd.transiciones:
                    stack.append(afd.transiciones[(estado, c)])

    return visitados


def minimizar_afd(afd):
    accesibles = eliminar_inaccesibles(afd)

    estados = list(accesibles)
    tabla = {}

    # Paso 1
    for i in range(len(estados)):
        for j in range(i):
            p, q = estados[i], estados[j]
            tabla[(p, q)] = ((p in afd.finales) != (q in afd.finales))

    cambio = True

    # Paso 2
    while cambio:
        cambio = False

        for (p, q) in tabla:
            if tabla[(p, q)]:
                continue

            for s in afd.alfabeto:
                p1 = afd.transiciones.get((p, s))
                q1 = afd.transiciones.get((q, s))

                if p1 and q1:
                    key = tuple(sorted([p1, q1]))
                    if key in tabla and tabla[key]:
                        tabla[(p, q)] = True
                        cambio = True
                        break

    # Paso 3: agrupar
    grupos = []
    usados = set()

    for estado in estados:
        if estado in usados:
            continue

        grupo = {estado}

        for otro in estados:
            if otro != estado:
                key = tuple(sorted([estado, otro]))
                if key in tabla and not tabla[key]:
                    grupo.add(otro)

        usados.update(grupo)
        grupos.append(grupo)

    # Paso 4: construir nuevo AFD
    nuevo_estados = [frozenset(g) for g in grupos]
    nuevo_inicial = next(g for g in nuevo_estados if afd.inicial in g)
    nuevo_finales = {g for g in nuevo_estados if any(e in afd.finales for e in g)}

    nuevo_trans = {}

    for g in nuevo_estados:
        representante = list(g)[0]

        for s in afd.alfabeto:
            if (representante, s) in afd.transiciones:
                destino = afd.transiciones[(representante, s)]

                for grupo_dest in nuevo_estados:
                    if destino in grupo_dest:
                        nuevo_trans[(g, s)] = grupo_dest

    return nuevo_estados, nuevo_inicial, nuevo_finales, nuevo_trans, tabla