"""
Widget de visualización de la pila para el simulador de PDA.
Renderiza la pila como una columna vertical donde el tope está arriba.
"""

import flet as ft

from ui.tema import COLORES, TAMS


def crear_widget_pila(pila, max_visible=12):
    """
    Recibe una lista (el primer elemento es el tope).
    Devuelve un control de Flet que muestra la pila.
    """
    items = []

    # Etiqueta del tope
    items.append(
        ft.Container(
            content=ft.Text(
                "TOPE",
                size=10,
                weight="bold",
                color=COLORES["stack_top"]
            ),
            padding=ft.padding.only(bottom=4),
            alignment=ft.Alignment(0, 0)
        )
    )

    if not pila:
        items.append(
            ft.Container(
                content=ft.Text(
                    "PILA VACÍA",
                    size=12,
                    color=COLORES["text_dim"],
                    italic=True
                ),
                bgcolor=COLORES["stack_base"],
                padding=10,
                border_radius=6,
                width=100,
                alignment=ft.Alignment(0, 0)
            )
        )
    else:
        visible = pila[:max_visible]

        for i, simbolo in enumerate(visible):
            es_tope = (i == 0)

            items.append(
                ft.Container(
                    content=ft.Text(
                        simbolo,
                        size=18 if es_tope else 16,
                        weight="bold",
                        color=(
                            "#000000" if es_tope
                            else COLORES["text"]
                        )
                    ),
                    bgcolor=(
                        COLORES["stack_top"] if es_tope
                        else COLORES["stack_body"]
                    ),
                    padding=8,
                    border_radius=4,
                    width=90,
                    alignment=ft.Alignment(0, 0),
                    border=ft.border.all(
                        2 if es_tope else 1,
                        (
                            "#FFAB00" if es_tope
                            else COLORES["border"]
                        )
                    )
                )
            )

        if len(pila) > max_visible:
            items.append(
                ft.Container(
                    content=ft.Text(
                        f"⋮ +{len(pila) - max_visible} más",
                        size=11,
                        italic=True,
                        color=COLORES["text_dim"]
                    ),
                    padding=4,
                    alignment=ft.Alignment(0, 0)
                )
            )

    # Etiqueta de base
    items.append(
        ft.Container(
            content=ft.Text(
                "BASE",
                size=10,
                weight="bold",
                color=COLORES["text_dim"]
            ),
            padding=ft.padding.only(top=4),
            alignment=ft.Alignment(0, 0)
        )
    )

    items.append(
        ft.Container(
            content=ft.Text(
                f"|pila| = {len(pila)}",
                size=11,
                color=COLORES["text_dim"]
            ),
            padding=ft.padding.only(top=6),
            alignment=ft.Alignment(0, 0)
        )
    )

    return ft.Container(
        content=ft.Column(
            controls=items,
            spacing=2,
            horizontal_alignment="center"
        ),
        bgcolor=COLORES["surface_alt"],
        padding=12,
        border_radius=10,
        border=ft.border.all(1, COLORES["border"]),
        width=130
    )
