"""
Escritor de autómatas a formatos .jff (JFLAP), .json y .xml.
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom


def _bonito(elem):
    """Devuelve XML pretty-printed."""
    bruto = ET.tostring(elem, encoding="utf-8")
    return minidom.parseString(bruto).toprettyxml(indent="  ")


# =========================================================
# AFD / AFND / AFND-λ
# =========================================================

def escribir_jff_fa(
    ruta,
    estados,
    inicial,
    finales,
    transiciones
):
    """
    Guarda un AFD/AFND/AFND-λ en formato .jff (JFLAP).
    """
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "fa"
    auto = ET.SubElement(root, "automaton")

    estados_lista = sorted(estados)
    id_map = {e: str(i) for i, e in enumerate(estados_lista)}

    for nombre, i in id_map.items():
        s = ET.SubElement(
            auto,
            "state",
            id=i,
            name=nombre
        )
        ET.SubElement(s, "x").text = str(80 + int(i) * 100)
        ET.SubElement(s, "y").text = "100"

        if nombre == inicial:
            ET.SubElement(s, "initial")
        if nombre in finales:
            ET.SubElement(s, "final")

    for (o, simbolo), destinos in transiciones.items():

        if not isinstance(destinos, (list, set)):
            destinos = [destinos]

        for d in destinos:
            if o not in id_map or d not in id_map:
                continue
            t = ET.SubElement(auto, "transition")
            ET.SubElement(t, "from").text = id_map[o]
            ET.SubElement(t, "to").text = id_map[d]
            read = ET.SubElement(t, "read")
            if simbolo != "λ":
                read.text = simbolo

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(_bonito(root))


def escribir_json_fa(
    ruta,
    estados,
    alfabeto,
    inicial,
    finales,
    transiciones
):
    trans_serial = {}

    for (o, s), d in transiciones.items():
        if isinstance(d, (list, set)):
            d = list(d)
        trans_serial[f"{o},{s}"] = d

    data = {
        "type": "fa",
        "estados": sorted(estados),
        "alfabeto": sorted(alfabeto),
        "inicial": inicial,
        "finales": sorted(finales),
        "transiciones": trans_serial
    }

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def escribir_xml_fa(
    ruta,
    estados,
    alfabeto,
    inicial,
    finales,
    transiciones
):
    root = ET.Element("automaton", type="fa")

    ET.SubElement(root, "alphabet").text = (
        ",".join(sorted(alfabeto))
    )

    estados_xml = ET.SubElement(root, "states")
    for e in sorted(estados):
        s = ET.SubElement(estados_xml, "state", name=e)
        if e == inicial:
            s.set("initial", "true")
        if e in finales:
            s.set("final", "true")

    trans_xml = ET.SubElement(root, "transitions")
    for (o, s), d in transiciones.items():
        if isinstance(d, (list, set)):
            destinos = list(d)
        else:
            destinos = [d]
        for dest in destinos:
            ET.SubElement(
                trans_xml,
                "transition",
                origen=str(o),
                simbolo=s,
                destino=str(dest)
            )

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(_bonito(root))


# =========================================================
# PDA
# =========================================================

def escribir_jff_pda(ruta, pda):
    """
    Guarda un PDA en formato .jff (JFLAP).
    """
    root = ET.Element("structure")
    ET.SubElement(root, "type").text = "pda"
    auto = ET.SubElement(root, "automaton")

    estados_lista = sorted(pda.estados)
    id_map = {e: str(i) for i, e in enumerate(estados_lista)}

    for nombre, i in id_map.items():
        s = ET.SubElement(
            auto,
            "state",
            id=i,
            name=nombre
        )
        ET.SubElement(s, "x").text = str(80 + int(i) * 120)
        ET.SubElement(s, "y").text = "120"

        if nombre == pda.inicial:
            ET.SubElement(s, "initial")
        if nombre in pda.finales:
            ET.SubElement(s, "final")

    for (q, a, x), destinos in pda.transiciones.items():
        for (p, push) in destinos:
            t = ET.SubElement(auto, "transition")
            ET.SubElement(t, "from").text = id_map[q]
            ET.SubElement(t, "to").text = id_map[p]

            read = ET.SubElement(t, "read")
            if a != "λ":
                read.text = a

            pop_e = ET.SubElement(t, "pop")
            pop_e.text = x

            push_e = ET.SubElement(t, "push")
            if push:
                push_e.text = push

    with open(ruta, "w", encoding="utf-8") as f:
        f.write(_bonito(root))


def escribir_json_pda(ruta, pda):
    trans_serial = {}

    for (q, a, x), destinos in pda.transiciones.items():
        clave = f"{q},{a},{x}"
        trans_serial[clave] = [
            [p, push] for (p, push) in destinos
        ]

    data = {
        "type": "pda",
        "estados": sorted(pda.estados),
        "alfabeto_entrada": sorted(pda.alfabeto_entrada),
        "alfabeto_pila": sorted(pda.alfabeto_pila),
        "inicial": pda.inicial,
        "simbolo_inicial_pila": pda.simbolo_inicial_pila,
        "finales": sorted(pda.finales),
        "modo_aceptacion": pda.modo_aceptacion,
        "transiciones": trans_serial
    }

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
