"""
Renderizador de autómatas con Graphviz.
Genera PNG para AFD, AFND, AFND-λ y PDA.
"""

import os
from graphviz import Digraph


# Carpeta assets ANCLADA a la ubicación del proyecto, no al CWD.
# Esto garantiza que los PNG se generen en el mismo sitio siempre,
# sin importar desde dónde se haya ejecutado python.
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(_PROJECT_ROOT, "assets")


def _asegurar_assets():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)


def _nodo_estado(dot, estado, finales, activos=None):
    activos = activos or set()
    es_final = estado in finales
    es_activo = estado in activos

    shape = "doublecircle" if es_final else "circle"

    if es_activo:
        dot.node(
            str(estado),
            shape=shape,
            style="filled",
            fillcolor="#FFD700",
            color="#1f1f1f",
            fontcolor="black",
            penwidth="2.0"
        )
    else:
        dot.node(
            str(estado),
            shape=shape,
            style="filled",
            fillcolor="#FFFFFF",
            color="#1f1f1f",
            fontcolor="black",
            penwidth="1.2"
        )


# =========================================================
# AFD / AFND / AFND-λ
# =========================================================

def generar_fa(
    estados,
    inicial,
    finales,
    transiciones,
    nombre_archivo="automata",
    estado_activo=None
):
    _asegurar_assets()

    dot = Digraph(format="png")
    dot.attr(rankdir="LR", bgcolor="#FAFAFA")
    dot.attr(
        "graph",
        fontname="Helvetica",
        nodesep="0.5",
        ranksep="0.7"
    )
    dot.attr("node", fontname="Helvetica")
    dot.attr("edge", fontname="Helvetica", fontsize="11")

    activos = {estado_activo} if estado_activo else set()

    for e in estados:
        _nodo_estado(dot, e, finales, activos)

    dot.node("__start__", shape="none", label="")
    dot.edge(
        "__start__",
        str(inicial),
        label="inicio",
        color="#1976D2",
        fontcolor="#1976D2"
    )

    # Agrupar transiciones por par (origen, destino)
    agrupadas = {}
    for (o, s), destinos in transiciones.items():
        if not isinstance(destinos, (list, set)):
            destinos = [destinos]
        for d in destinos:
            key = (str(o), str(d))
            if key not in agrupadas:
                agrupadas[key] = []
            agrupadas[key].append(s if s != "λ" else "λ")

    for (o, d), simbolos in agrupadas.items():
        etiqueta = ", ".join(simbolos)
        dot.edge(
            o,
            d,
            label=etiqueta,
            color="#333333",
            fontcolor="#1f1f1f"
        )

    ruta = os.path.join(ASSETS_DIR, nombre_archivo)
    dot.render(ruta, cleanup=True)
    return ruta + ".png"


# =========================================================
# PDA
# =========================================================

def generar_pda(
    pda,
    nombre_archivo="pda",
    estado_activo=None
):
    _asegurar_assets()

    dot = Digraph(format="png")
    dot.attr(rankdir="LR", bgcolor="#FAFAFA")
    dot.attr(
        "graph",
        fontname="Helvetica",
        nodesep="0.6",
        ranksep="0.9"
    )
    dot.attr("node", fontname="Helvetica")
    dot.attr("edge", fontname="Helvetica", fontsize="10")

    activos = {estado_activo} if estado_activo else set()

    for e in pda.estados:
        _nodo_estado(dot, e, pda.finales, activos)

    dot.node("__start__", shape="none", label="")
    dot.edge(
        "__start__",
        str(pda.inicial),
        label="inicio",
        color="#1976D2",
        fontcolor="#1976D2"
    )

    # Agrupar transiciones por (origen, destino)
    agrupadas = {}
    for (q, a, x), destinos in pda.transiciones.items():
        for (p, push) in destinos:
            key = (str(q), str(p))
            if key not in agrupadas:
                agrupadas[key] = []
            push_str = push if push else "ε"
            simb_str = a if a != "λ" else "λ"
            agrupadas[key].append(f"{simb_str}, {x} / {push_str}")

    for (o, d), etiquetas in agrupadas.items():
        etiqueta = "\\n".join(etiquetas)
        dot.edge(
            o,
            d,
            label=etiqueta,
            color="#333333",
            fontcolor="#0D47A1"
        )

    ruta = os.path.join(ASSETS_DIR, nombre_archivo)
    dot.render(ruta, cleanup=True)
    return ruta + ".png"
