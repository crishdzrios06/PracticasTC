import json


def guardar_json(nombre, datos):

    with open(nombre, "w", encoding="utf-8") as archivo:

        json.dump(
            datos,
            archivo,
            indent=4
        )


def cargar_json(nombre):

    with open(nombre, "r", encoding="utf-8") as archivo:

        return json.load(archivo)