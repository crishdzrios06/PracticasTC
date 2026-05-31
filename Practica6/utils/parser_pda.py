"""
Parser de transiciones para PDA en formato amigable de texto.

Formato esperado por cada línea:
    estado_origen, simbolo_entrada, simbolo_pila -> destino, cadena_push ; ...

Ejemplos:
    q0, a, Z -> q0, AZ
    q0, a, A -> q0, AA
    q0, b, A -> q1, ε
    q1, b, A -> q1, ε
    q1, λ, Z -> q2, Z

Separador entre reglas: ';' o salto de línea.
Símbolo lambda: 'λ', 'lambda' o '\\' (epsilon)
Cadena vacía a apilar: 'ε' o 'epsilon' o vacío
"""


LAMBDAS = {"λ", "lambda", "\\", "epsilon", "ε", ""}


def _norm_simbolo_entrada(s):
    s = s.strip()
    if s.lower() in {"lambda", "epsilon", "ε", "\\"} or s == "λ":
        return "λ"
    return s


def _norm_push(s):
    s = s.strip()
    if s.lower() in {"epsilon", "ε", "lambda", "λ", "\\"} or s == "":
        return ""
    return s


def parsear_transiciones_pda(texto):
    """
    Devuelve un dict[(q, a, x)] = list[(p, push)].
    """
    transiciones = {}

    # Permitir separadores ; y saltos de línea
    crudo = texto.replace("\n", ";").replace("\r", ";")

    for regla in crudo.split(";"):
        regla = regla.strip()
        if not regla:
            continue

        if "->" not in regla:
            raise ValueError(
                f"Falta '->' en regla: {regla!r}"
            )

        izq, der = regla.split("->", 1)

        partes_izq = [p.strip() for p in izq.split(",")]

        if len(partes_izq) != 3:
            raise ValueError(
                f"Lado izquierdo debe ser "
                f"'estado, simbolo, tope_pila' en: {regla!r}"
            )

        q, a, x = partes_izq
        a = _norm_simbolo_entrada(a)

        if not x:
            raise ValueError(
                f"Falta símbolo de pila en regla: {regla!r}"
            )

        partes_der = [p.strip() for p in der.split(",")]

        if len(partes_der) < 1:
            raise ValueError(
                f"Lado derecho debe ser "
                f"'destino, cadena_push' en: {regla!r}"
            )

        if len(partes_der) == 1:
            p_dest = partes_der[0]
            push = ""
        else:
            p_dest = partes_der[0]
            push = _norm_push(",".join(partes_der[1:]))

        clave = (q, a, x)
        if clave not in transiciones:
            transiciones[clave] = []
        transiciones[clave].append((p_dest, push))

    return transiciones


def serializar_transiciones_pda(transiciones):
    """Inverso de parsear: dict → texto formateado."""
    lineas = []
    for (q, a, x), destinos in transiciones.items():
        for (p, push) in destinos:
            push_str = push if push else "ε"
            a_str = a if a != "λ" else "λ"
            lineas.append(f"{q}, {a_str}, {x} -> {p}, {push_str}")
    return "\n".join(lineas)
