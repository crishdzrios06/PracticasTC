import flet as ft


def crear_sidebar(controles):

    return ft.Container(

        content=ft.Column(
            controls=controles,
            scroll="auto"
        ),

        width=380,
        padding=20,
        bgcolor="#1e1e1e"
    )