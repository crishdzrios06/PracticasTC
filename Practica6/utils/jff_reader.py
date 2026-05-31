"""
Lector de archivos JFLAP (.jff) - extendido para soportar PDA.
"""

import xml.etree.ElementTree as ET


def _texto(elem, default=""):
    if elem is None or elem.text is None:
        return default
    return elem.text


def detectar_tipo(ruta):
    """Devuelve el tipo declarado en <type> dentro del .jff."""
    tree = ET.parse(ruta)
    root = tree.getroot()
    tipo_elem = root.find("type")
    if tipo_elem is not None:
        return _texto(tipo_elem, "fa").strip().lower()
    return "fa"


def leer_jff(ruta):
    """
    Lector genérico para autómatas finitos (fa).
    Devuelve (estados, alfabeto, inicial, finales, transiciones).

    transiciones: dict[(estado, simbolo)] = list[estado]
    """
    tree = ET.parse(ruta)
    root = tree.getroot()

    estados = {}
    inicial = None
    finales = set()
    trans = {}
    alfabeto = set()

    for s in root.iter("state"):
        sid = s.get("id")
        nombre_attr = s.get("name")
        nombre = nombre_attr if nombre_attr else f"q{sid}"
        estados[sid] = nombre

        if s.find("initial") is not None:
            inicial = nombre
        if s.find("final") is not None:
            finales.add(nombre)

    for t in root.iter("transition"):
        o_id = _texto(t.find("from"))
        d_id = _texto(t.find("to"))
        o = estados[o_id]
        d = estados[d_id]
        simbolo = _texto(t.find("read"), "")

        if simbolo == "":
            simbolo = "λ"

        alfabeto.add(simbolo)

        if (o, simbolo) not in trans:
            trans[(o, simbolo)] = []
        trans[(o, simbolo)].append(d)

    return set(estados.values()), alfabeto, inicial, finales, trans


def leer_jff_pda(ruta):
    """
    Lector específico para PDA (tipo "pda").
    Devuelve un diccionario con todos los componentes.

    transiciones: dict[(estado, simbolo_entrada, simbolo_pila)]
                  = list[(nuevo_estado, cadena_apilar)]
    """
    tree = ET.parse(ruta)
    root = tree.getroot()

    estados = {}
    inicial = None
    finales = set()
    alfabeto_entrada = set()
    alfabeto_pila = set()
    transiciones = {}

    for s in root.iter("state"):
        sid = s.get("id")
        nombre_attr = s.get("name")
        nombre = nombre_attr if nombre_attr else f"q{sid}"
        estados[sid] = nombre

        if s.find("initial") is not None:
            inicial = nombre
        if s.find("final") is not None:
            finales.add(nombre)

    for t in root.iter("transition"):
        o_id = _texto(t.find("from"))
        d_id = _texto(t.find("to"))
        o = estados[o_id]
        d = estados[d_id]

        leer = _texto(t.find("read"), "")
        pop = _texto(t.find("pop"), "")
        push = _texto(t.find("push"), "")

        if leer == "":
            leer = "λ"
        else:
            alfabeto_entrada.add(leer)

        if pop:
            alfabeto_pila.add(pop)

        for c in push:
            alfabeto_pila.add(c)

        clave = (o, leer, pop)
        if clave not in transiciones:
            transiciones[clave] = []
        transiciones[clave].append((d, push))

    # Símbolo inicial de pila: por convención Z en JFLAP
    simbolo_inicial_pila = "Z"
    if "Z" not in alfabeto_pila:
        # Intentar inferir: el símbolo de pop más común en
        # transiciones desde el estado inicial
        for (e, _, pop), _destinos in transiciones.items():
            if e == inicial and pop:
                simbolo_inicial_pila = pop
                break
    alfabeto_pila.add(simbolo_inicial_pila)

    return {
        "estados": set(estados.values()),
        "alfabeto_entrada": alfabeto_entrada,
        "alfabeto_pila": alfabeto_pila,
        "inicial": inicial,
        "simbolo_inicial_pila": simbolo_inicial_pila,
        "finales": finales,
        "transiciones": transiciones
    }
