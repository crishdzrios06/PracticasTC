import xml.etree.ElementTree as ET

def leer_jff(ruta):
    tree = ET.parse(ruta)
    root = tree.getroot()

    estados = {}
    inicial = None
    finales = set()
    trans = {}
    alfabeto = set()

    for s in root.iter("state"):
        sid = s.get("id")
        nombre = "q" + sid
        estados[sid] = nombre

        if s.find("initial") is not None:
            inicial = nombre
        if s.find("final") is not None:
            finales.add(nombre)

    for t in root.iter("transition"):
        o = estados[t.find("from").text]
        d = estados[t.find("to").text]
        simbolo = t.find("read").text

        if simbolo is None:
            simbolo = "λ"

        alfabeto.add(simbolo)

        if (o, simbolo) not in trans:
            trans[(o, simbolo)] = []

        trans[(o, simbolo)].append(d)

    return set(estados.values()), alfabeto, inicial, finales, trans