import flet as ft


def crear_consola():

    return ft.Container(

        content=ft.Column(
            scroll="auto"
        ),

        bgcolor="#111111",

        border_radius=10,

        padding=15,

        expand=True
    )