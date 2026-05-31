"""
Componentes reutilizables de la UI.
"""

import flet as ft

from ui.tema import COLORES, TAMS


def card(titulo, contenido, icono=None):
    """Tarjeta con título y contenido."""
    header_controls = []
    if icono:
        header_controls.append(
            ft.Icon(icono, color=COLORES["primary"], size=18)
        )
    header_controls.append(
        ft.Text(
            titulo,
            size=TAMS["encabezado"],
            weight="bold",
            color=COLORES["text_strong"]
        )
    )

    header = ft.Row(
        controls=header_controls,
        spacing=8,
        vertical_alignment="center"
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                header,
                ft.Divider(height=1, color=COLORES["border"]),
                contenido
            ],
            spacing=10
        ),
        bgcolor=COLORES["card"],
        border_radius=12,
        padding=16,
        border=ft.border.all(1, COLORES["border"])
    )


def badge(texto, color=None):
    color = color or COLORES["primary"]
    return ft.Container(
        content=ft.Text(
            texto,
            size=11,
            weight="bold",
            color="#FFFFFF"
        ),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        border_radius=12
    )


def boton_primario(texto, on_click, icono=None, ancho=None):
    return ft.ElevatedButton(
        text=texto,
        on_click=on_click,
        icon=icono,
        width=ancho,
        bgcolor=COLORES["primary"],
        color="#FFFFFF",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=16, vertical=12)
        )
    )


def boton_secundario(texto, on_click, icono=None, ancho=None):
    return ft.ElevatedButton(
        text=texto,
        on_click=on_click,
        icon=icono,
        width=ancho,
        bgcolor=COLORES["surface_alt"],
        color=COLORES["text"],
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            side=ft.BorderSide(1, COLORES["border"])
        )
    )


def boton_peligro(texto, on_click, icono=None, ancho=None):
    return ft.ElevatedButton(
        text=texto,
        on_click=on_click,
        icon=icono,
        width=ancho,
        bgcolor=COLORES["error"],
        color="#FFFFFF",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.padding.symmetric(horizontal=14, vertical=10)
        )
    )


def campo_texto(label, hint="", multilinea=False, valor=""):
    return ft.TextField(
        label=label,
        hint_text=hint,
        value=valor,
        multiline=multilinea,
        min_lines=4 if multilinea else 1,
        max_lines=10 if multilinea else 1,
        border_color=COLORES["border"],
        focused_border_color=COLORES["primary"],
        label_style=ft.TextStyle(
            color=COLORES["text_dim"],
            size=12
        ),
        text_style=ft.TextStyle(
            color=COLORES["text"],
            size=14
        ),
        bgcolor=COLORES["surface_alt"]
    )


def caja_resultado(texto_control):
    """Caja para mostrar resultados con estilo consistente."""
    return ft.Container(
        content=texto_control,
        bgcolor=COLORES["surface"],
        border=ft.border.all(1, COLORES["border"]),
        border_radius=8,
        padding=12
    )


def tabla_pasos_pda(traza):
    """Tabla con los pasos de la traza de un PDA."""
    cabeceras = [
        "#", "Estado", "Leído", "Restante", "Pila (tope→base)",
        "Acción", "Regla aplicada"
    ]

    columnas = [
        ft.DataColumn(
            ft.Text(
                h,
                weight="bold",
                size=12,
                color=COLORES["text_strong"]
            )
        )
        for h in cabeceras
    ]

    filas = []

    for paso in traza:
        pila_str = "".join(paso.get("pila", [])) or "ε"
        regla = paso.get("regla") or "—"
        leido = paso.get("leido", "") or "ε"
        restante = paso.get("restante", "") or "ε"

        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(
                            str(paso["paso"]),
                            size=11,
                            color=COLORES["text"]
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            paso["estado"],
                            size=11,
                            color=COLORES["accent"],
                            weight="bold"
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            leido,
                            size=11,
                            color=COLORES["text"]
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            restante,
                            size=11,
                            color=COLORES["text"]
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            pila_str,
                            size=11,
                            color=COLORES["warning"],
                            font_family="Courier New",
                            weight="bold"
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            paso["accion"],
                            size=11,
                            color=COLORES["text_dim"]
                        )
                    ),
                    ft.DataCell(
                        ft.Text(
                            regla,
                            size=10,
                            color=COLORES["text_dim"],
                            font_family="Courier New"
                        )
                    ),
                ]
            )
        )

    return ft.DataTable(
        columns=columnas,
        rows=filas,
        heading_row_color=COLORES["surface_alt"],
        data_row_color={"hovered": COLORES["surface_alt"]},
        border=ft.border.all(1, COLORES["border"]),
        border_radius=8,
        column_spacing=20,
        heading_row_height=36,
        data_row_min_height=32
    )
