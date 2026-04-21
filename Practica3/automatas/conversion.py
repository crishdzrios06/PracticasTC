def convertir_afnd_a_afd(afnd):
    inicial = frozenset([afnd.inicial])
    estados = {inicial}
    trans = {}
    finales = set()

    pendientes = [inicial]

    while pendientes:
        actual = pendientes.pop()

        for simbolo in afnd.alfabeto:
            if simbolo == "λ":
                continue

            nuevo = set()

            for e in actual:
                if (e, simbolo) in afnd.transiciones:
                    nuevo.update(afnd.transiciones[(e, simbolo)])

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


# 🔥 NUEVO: eliminar lambda
def eliminar_lambda(afndl):
    nuevas_trans = {}

    for estado in afndl.estados:
        clausura = afndl.lambda_clausura({estado})

        for simbolo in afndl.alfabeto:
            if simbolo == "λ":
                continue

            destinos = set()

            for e in clausura:
                if (e, simbolo) in afndl.transiciones:
                    for d in afndl.transiciones[(e, simbolo)]:
                        destinos.update(afndl.lambda_clausura({d}))

            if destinos:
                nuevas_trans[(estado, simbolo)] = list(destinos)

    nuevos_finales = set()

    for estado in afndl.estados:
        clausura = afndl.lambda_clausura({estado})
        if any(e in afndl.finales for e in clausura):
            nuevos_finales.add(estado)

    return afndl.estados, afndl.alfabeto - {"λ"}, afndl.inicial, nuevos_finales, nuevas_trans