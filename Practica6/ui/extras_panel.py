"""
Panel de Operaciones sobre lenguajes y Validadores regex.
"""

import flet as ft

from extras.operaciones import (
    subcadenas, prefijos, sufijos,
    kleene, kleene_positiva,
    concatenar_lenguajes, union_lenguajes,
    interseccion_lenguajes, diferencia_lenguajes,
    potencia_lenguaje, reflexion_lenguaje
)
from extras.validadores import validar, listar_validadores

from ui.tema import COLORES, TAMS
from ui.components import (
    boton_primario, boton_secundario,
    campo_texto, caja_resultado
)


def construir_panel_extras(page: ft.Page):

    # ---------- Operaciones sobre cadenas ----------
    f_cadena = campo_texto("Cadena", "abc")
    f_alfabeto = campo_texto("Alfabeto Σ", "a, b")
    f_long = campo_texto("Longitud máxima (Σ*)", "3")
    f_l1 = campo_texto("Lenguaje L1", "a, ab")
    f_l2 = campo_texto("Lenguaje L2", "ba, b")
    f_n = campo_texto("Potencia n", "2")

    txt_resultado = ft.Text("", size=13, color=COLORES["text"])
    txt_lista = ft.Text(
        "",
        size=12,
        color=COLORES["text"],
        font_family="Courier New",
        selectable=True
    )

    def mostrar(msg, lista=None, color=None):
        txt_resultado.value = msg
        txt_resultado.color = color or COLORES["text"]
        if lista is not None:
            txt_lista.value = str(lista)
        page.update()

    def lista_lenguaje(s):
        return [
            x.strip()
            for x in s.split(",")
            if x.strip()
        ] or [""]

    # Handlers de cadenas
    def on_prefijos(e):
        r = prefijos(f_cadena.value or "")
        mostrar(
            f"Prefijos de '{f_cadena.value}' "
            f"({len(r)}):", r
        )

    def on_sufijos(e):
        r = sufijos(f_cadena.value or "")
        mostrar(
            f"Sufijos de '{f_cadena.value}' "
            f"({len(r)}):", r
        )

    def on_subcadenas(e):
        r = subcadenas(f_cadena.value or "")
        mostrar(
            f"Subcadenas de '{f_cadena.value}' "
            f"({len(r)}):", r
        )

    def on_kleene(e):
        alf = lista_lenguaje(f_alfabeto.value)
        try:
            n = int(f_long.value or "3")
        except ValueError:
            n = 3
        r = kleene(alf, n)
        mostrar(
            f"Σ* (hasta longitud {n}): {len(r)} cadenas",
            r
        )

    def on_kleene_pos(e):
        alf = lista_lenguaje(f_alfabeto.value)
        try:
            n = int(f_long.value or "3")
        except ValueError:
            n = 3
        r = kleene_positiva(alf, n)
        mostrar(
            f"Σ⁺ (hasta longitud {n}): {len(r)} cadenas",
            r
        )

    def on_concat(e):
        r = concatenar_lenguajes(
            lista_lenguaje(f_l1.value),
            lista_lenguaje(f_l2.value)
        )
        mostrar(f"L1 · L2 ({len(r)}):", r)

    def on_union(e):
        r = union_lenguajes(
            lista_lenguaje(f_l1.value),
            lista_lenguaje(f_l2.value)
        )
        mostrar(f"L1 ∪ L2 ({len(r)}):", r)

    def on_interseccion(e):
        r = interseccion_lenguajes(
            lista_lenguaje(f_l1.value),
            lista_lenguaje(f_l2.value)
        )
        mostrar(f"L1 ∩ L2 ({len(r)}):", r)

    def on_diferencia(e):
        r = diferencia_lenguajes(
            lista_lenguaje(f_l1.value),
            lista_lenguaje(f_l2.value)
        )
        mostrar(f"L1 − L2 ({len(r)}):", r)

    def on_potencia(e):
        try:
            n = int(f_n.value or "2")
        except ValueError:
            n = 2
        r = potencia_lenguaje(lista_lenguaje(f_l1.value), n)
        mostrar(f"L1^{n} ({len(r)}):", r)

    def on_reflexion(e):
        r = reflexion_lenguaje(lista_lenguaje(f_l1.value))
        mostrar(f"L1ᴿ ({len(r)}):", r)

    # ---------- Validadores ----------
    f_regex_input = campo_texto(
        "Texto a validar",
        "ejemplo@correo.com"
    )

    txt_resultado_regex = ft.Text(
        "",
        size=14,
        color=COLORES["text"]
    )

    def hacer_validador(tipo):
        def handler(e):
            ok, patron, msg = validar(tipo, f_regex_input.value)
            color = COLORES["success"] if ok else COLORES["error"]
            txt_resultado_regex.value = (
                f"{msg}\nPatrón: {patron}"
            )
            txt_resultado_regex.color = color
            page.update()
        return handler

    botones_regex = [
        boton_secundario(
            descripcion,
            hacer_validador(clave)
        )
        for clave, descripcion in listar_validadores()
    ]

    # ---------- Layout ----------
    col_operaciones = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "OPERACIONES SOBRE CADENAS",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                f_cadena,
                ft.Row(
                    controls=[
                        boton_secundario("Prefijos", on_prefijos),
                        boton_secundario("Sufijos", on_sufijos),
                        boton_secundario(
                            "Subcadenas", on_subcadenas
                        ),
                    ],
                    spacing=8,
                    wrap=True
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                f_alfabeto,
                f_long,
                ft.Row(
                    controls=[
                        boton_secundario("Σ* (Kleene)", on_kleene),
                        boton_secundario(
                            "Σ⁺ (Positiva)", on_kleene_pos
                        ),
                    ],
                    spacing=8,
                    wrap=True
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                ft.Text(
                    "OPERACIONES SOBRE LENGUAJES",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                f_l1,
                f_l2,
                ft.Row(
                    controls=[
                        boton_secundario("L1·L2", on_concat),
                        boton_secundario("L1 ∪ L2", on_union),
                        boton_secundario(
                            "L1 ∩ L2", on_interseccion
                        ),
                        boton_secundario(
                            "L1 − L2", on_diferencia
                        ),
                        boton_secundario("L1ᴿ", on_reflexion),
                    ],
                    spacing=8,
                    wrap=True
                ),
                f_n,
                boton_secundario("Lⁿ (potencia)", on_potencia),
            ],
            scroll="auto",
            spacing=10
        ),
        width=440,
        padding=18,
        bgcolor=COLORES["surface"],
        border_radius=12,
        border=ft.border.all(1, COLORES["border"])
    )

    col_resultado = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "RESULTADOS",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                caja_resultado(txt_resultado),
                ft.Container(
                    content=ft.Column(
                        controls=[txt_lista],
                        scroll="auto"
                    ),
                    bgcolor=COLORES["bg"],
                    padding=12,
                    border_radius=8,
                    border=ft.border.all(1, COLORES["border"]),
                    height=300
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                ft.Text(
                    "VALIDADORES (Expresiones Regulares)",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                f_regex_input,
                ft.Row(
                    controls=botones_regex,
                    spacing=8,
                    wrap=True
                ),
                caja_resultado(txt_resultado_regex)
            ],
            scroll="auto",
            spacing=10
        ),
        expand=True,
        padding=18,
        bgcolor=COLORES["surface"],
        border_radius=12,
        border=ft.border.all(1, COLORES["border"])
    )

    return ft.Row(
        controls=[col_operaciones, col_resultado],
        spacing=12,
        expand=True
    )
