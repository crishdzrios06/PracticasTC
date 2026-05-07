import flet as ft


def crear_visual_panel(imagen, consola):

    return ft.Container(

        content=ft.Column([

            ft.Text(
                "Visualización",
                size=28,
                weight="bold"
            ),

            imagen,

            ft.Divider(),

            ft.Text(
                "Consola de simulación",
                size=22,
                weight="bold"
            ),

            consola

        ]),

        expand=True,

        padding=20
    )