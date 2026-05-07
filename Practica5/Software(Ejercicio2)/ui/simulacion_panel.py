import flet as ft


def crear_panel_simulacion(resultado):

    return ft.Container(

        content=ft.Column([

            ft.Text(
                "Resultado",
                size=20,
                weight="bold"
            ),

            resultado

        ]),

        padding=10
    )