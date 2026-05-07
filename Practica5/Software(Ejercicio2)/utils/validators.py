def validar_afd(estados, alfabeto, inicial, finales):

    errores = []

    if inicial not in estados:
        errores.append(
            "El estado inicial no existe."
        )

    for estado in finales:

        if estado not in estados:

            errores.append(
                f"Estado final inválido: {estado}"
            )

    return errores