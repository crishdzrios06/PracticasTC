"""
======================================================================
 SIMULADOR DE AUTÓMATAS - Teoría de la Computación
======================================================================

  Instituto Politécnico Nacional
  Escuela Superior de Cómputo
  Ingeniería en Sistemas Computacionales
  4CM4 - HERNANDEZ RIOS CRISTIAN SEBASTIAN

  Versión remasterizada (v2) con soporte para:
   - AFD, AFND, AFND-λ
   - PDA (Autómatas de Pila) - Práctica 6
   - Conversiones, minimización, AFD→ER
   - Visualización con Graphviz
   - Importación/exportación .jff, .json, .xml
   - Interfaz con navegación lateral, file pickers y tema oscuro

  Ejecutar:  python main.py
======================================================================
"""

import flet as ft

from ui.tema import COLORES, TAMS
from ui.af_panel import construir_panel_af
from ui.pda_panel import construir_panel_pda
from ui.extras_panel import construir_panel_extras


def main(page: ft.Page):

    # ==================================================================
    # CONFIGURACIÓN GENERAL
    # ==================================================================
    page.title = "Simulador de Autómatas v2"
    page.theme_mode = "dark"
    page.bgcolor = COLORES["bg"]
    page.padding = 0
    page.spacing = 0
    page.window_width = 1520
    page.window_height = 940
    page.window_min_width = 1100
    page.window_min_height = 700

    page.fonts = {
        "Inter": "https://rsms.me/inter/font-files/Inter.var.woff2"
    }

    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=COLORES["primary"],
            secondary=COLORES["secondary"],
            surface=COLORES["surface"],
        ),
        scrollbar_theme=ft.ScrollbarTheme(
            thumb_color=COLORES["primary"],
            track_color=COLORES["surface_alt"]
        )
    )

    # ==================================================================
    # CONTENEDOR DE PÁGINAS
    # ==================================================================
    panel_actual = ft.Container(
        expand=True,
        padding=14,
        bgcolor=COLORES["bg"]
    )

    # Paneles
    panel_inicio = _panel_inicio()
    panel_af = construir_panel_af(page)
    panel_pda = construir_panel_pda(page)
    panel_extras = construir_panel_extras(page)

    paneles = {
        0: panel_inicio,
        1: panel_af,
        2: panel_pda,
        3: panel_extras,
    }

    def cambiar_panel(idx):
        panel_actual.content = paneles[idx]
        page.update()

    # ==================================================================
    # NAVIGATION RAIL
    # ==================================================================
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor=COLORES["surface"],
        indicator_color=COLORES["primary"],
        indicator_shape=ft.RoundedRectangleBorder(radius=10),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Inicio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ACCOUNT_TREE_OUTLINED,
                selected_icon=ft.Icons.ACCOUNT_TREE,
                label="Autómatas\nFinitos"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.LAYERS_OUTLINED,
                selected_icon=ft.Icons.LAYERS,
                label="Autómatas\nde Pila"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FUNCTIONS_OUTLINED,
                selected_icon=ft.Icons.FUNCTIONS,
                label="Lenguajes\ny Regex"
            ),
        ],
        on_change=lambda e: cambiar_panel(e.control.selected_index)
    )

    # ==================================================================
    # HEADER
    # ==================================================================
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(
                    ft.Icons.GRAPHIC_EQ,
                    color=COLORES["primary"],
                    size=28
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "Simulador de Autómatas",
                            size=20,
                            weight="bold",
                            color=COLORES["text_strong"]
                        ),
                        ft.Text(
                            "Teoría de la Computación · ESCOM IPN",
                            size=11,
                            color=COLORES["text_dim"]
                        )
                    ],
                    spacing=0,
                    tight=True
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Text(
                        "v2 · Práctica 6 (PDA)",
                        size=11,
                        weight="bold",
                        color="#FFFFFF"
                    ),
                    bgcolor=COLORES["secondary"],
                    padding=ft.padding.symmetric(
                        horizontal=12, vertical=6
                    ),
                    border_radius=20
                )
            ],
            spacing=12,
            vertical_alignment="center"
        ),
        bgcolor=COLORES["surface"],
        padding=ft.padding.symmetric(horizontal=20, vertical=12),
        border=ft.border.only(
            bottom=ft.BorderSide(1, COLORES["border"])
        )
    )

    # ==================================================================
    # LAYOUT FINAL
    # ==================================================================
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Row(
                    controls=[
                        rail,
                        ft.VerticalDivider(
                            width=1,
                            color=COLORES["border"]
                        ),
                        panel_actual
                    ],
                    expand=True,
                    spacing=0
                )
            ],
            spacing=0,
            expand=True
        )
    )

    # Cargar panel inicial
    cambiar_panel(0)


def _panel_inicio():
    """Pantalla de bienvenida con descripción de cada módulo."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Bienvenido al Simulador",
                                size=34,
                                weight="bold",
                                color=COLORES["text_strong"]
                            ),
                            ft.Text(
                                "Una herramienta interactiva para "
                                "explorar lenguajes formales, "
                                "autómatas finitos y autómatas de "
                                "pila.",
                                size=14,
                                color=COLORES["text_dim"]
                            ),
                            ft.Container(height=8),
                            ft.Row(
                                controls=[
                                    _chip("Práctica 1-5: AF y ER"),
                                    _chip(
                                        "Práctica 6: PDA",
                                        COLORES["secondary"]
                                    ),
                                    _chip(
                                        "JFLAP .jff",
                                        COLORES["accent"]
                                    )
                                ],
                                spacing=8,
                                wrap=True
                            )
                        ],
                        spacing=8
                    ),
                    bgcolor=COLORES["surface"],
                    padding=24,
                    border_radius=12,
                    border=ft.border.all(1, COLORES["border"])
                ),

                ft.Container(height=12),

                ft.Row(
                    controls=[
                        _tarjeta_modulo(
                            ft.Icons.ACCOUNT_TREE,
                            "Autómatas Finitos",
                            "AFD, AFND y AFND-λ\n"
                            "• Definición manual y carga .jff\n"
                            "• Simulación paso a paso\n"
                            "• Conversiones (AFND→AFD, λ→ε)\n"
                            "• Minimización de AFD\n"
                            "• AFD → Expresión Regular",
                            COLORES["primary"]
                        ),
                        _tarjeta_modulo(
                            ft.Icons.LAYERS,
                            "Autómatas de Pila (PDA)",
                            "Práctica 6\n"
                            "• Definición formal completa\n"
                            "• Visualización de la pila en tiempo real\n"
                            "• Animación paso a paso\n"
                            "• Cinta de entrada visual\n"
                            "• Aceptación por estado final / pila vacía",
                            COLORES["secondary"]
                        ),
                        _tarjeta_modulo(
                            ft.Icons.FUNCTIONS,
                            "Lenguajes y Regex",
                            "• Prefijos / Sufijos / Subcadenas\n"
                            "• Cerradura de Kleene Σ* y Σ⁺\n"
                            "• Concatenación, unión, intersección\n"
                            "• Diferencia, potencia, reflexión\n"
                            "• Validadores: email, URL, fecha…",
                            COLORES["accent"]
                        ),
                    ],
                    spacing=12,
                    wrap=True
                ),

                ft.Container(height=12),

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.LIGHTBULB,
                                        color=COLORES["warning"],
                                        size=20
                                    ),
                                    ft.Text(
                                        "Tip rápido",
                                        weight="bold",
                                        color=COLORES["text_strong"]
                                    )
                                ],
                                spacing=8
                            ),
                            ft.Text(
                                "En el panel de Autómatas de Pila "
                                "tienes tres ejemplos listos para "
                                "cargar: aⁿbⁿ, paréntesis "
                                "balanceados, y wcwᴿ. Pulsa el "
                                "botón correspondiente, luego "
                                "\"Generar diagrama\" y \"Simular\".",
                                color=COLORES["text"],
                                size=13
                            )
                        ],
                        spacing=8
                    ),
                    bgcolor=COLORES["surface"],
                    padding=16,
                    border_radius=10,
                    border=ft.border.all(1, COLORES["border"])
                )
            ],
            scroll="auto",
            spacing=0
        ),
        padding=14
    )


def _chip(texto, color=None):
    color = color or COLORES["primary"]
    return ft.Container(
        content=ft.Text(
            texto,
            size=11,
            weight="bold",
            color="#FFFFFF"
        ),
        bgcolor=color,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20
    )


def _tarjeta_modulo(icono, titulo, descripcion, color):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(icono, color=color, size=32),
                    bgcolor=COLORES["surface_alt"],
                    padding=12,
                    border_radius=10
                ),
                ft.Text(
                    titulo,
                    size=18,
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Text(
                    descripcion,
                    size=12,
                    color=COLORES["text_dim"]
                ),
            ],
            spacing=10
        ),
        bgcolor=COLORES["surface"],
        padding=18,
        border_radius=12,
        border=ft.border.all(1, COLORES["border"]),
        width=320,
        height=260
    )


if __name__ == "__main__":
    ft.app(target=main)
