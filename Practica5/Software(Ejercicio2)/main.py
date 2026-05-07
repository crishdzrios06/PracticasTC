import flet as ft

from automatas.afd import AFD
from automatas.afnd import AFND
from automatas.afnd_lambda import AFNDLambda

from automatas.conversion import (
    convertir_afnd_a_afd,
    eliminar_lambda
)

from automatas.minimizacion import minimizar_afd
from automatas.afd_to_er import afd_a_er

from automatas.simulador_visual import SimuladorVisual

from extras.operaciones import (
    subcadenas,
    prefijos,
    sufijos,
    kleene
)

from extras.validadores import validar as validar_regex

from utils.renderizador import RenderizadorAutomata
from utils.jff_reader import leer_jff
from utils.validators import validar_afd


def main(page: ft.Page):

    # ==================================================
    # CONFIGURACIÓN
    # ==================================================

    page.title = "Simulador de Autómatas"
    page.theme_mode = "dark"

    page.window_width = 1500
    page.window_height = 920

    page.padding = 0
    page.spacing = 0

    # ==================================================
    # COMPONENTES GLOBALES
    # ==================================================

    resultado = ft.Text(size=18)

    consola = ft.Column(
        scroll="auto",
        expand=True
    )

    imagen = ft.Image(
        src="assets/automata.png",
        width=850,
        height=500,
        fit="contain"
    )

    contenido = ft.Container(
        expand=True,
        padding=20
    )

    # ==================================================
    # INPUTS
    # ==================================================

    tipo = ft.Dropdown(
        label="Tipo de autómata",
        options=[
            ft.dropdown.Option("AFD"),
            ft.dropdown.Option("AFND"),
            ft.dropdown.Option("AFND-λ")
        ],
        value="AFD"
    )

    estados = ft.TextField(
        label="Estados",
        hint_text="q0,q1,q2"
    )

    alfabeto = ft.TextField(
        label="Alfabeto",
        hint_text="0,1"
    )

    inicial = ft.TextField(
        label="Estado inicial"
    )

    finales = ft.TextField(
        label="Estados finales"
    )

    transiciones = ft.TextField(
        label="Transiciones",
        multiline=True,
        min_lines=10
    )

    cadena = ft.TextField(
        label="Cadena"
    )

    ruta = ft.TextField(
        label="Ruta archivo .jff"
    )

    regex_input = ft.TextField(
        label="Texto a validar"
    )

    # ==================================================
    # PARSER
    # ==================================================

    def parsear():

        est = set(
            e.strip()
            for e in estados.value.split(",")
            if e.strip()
        )

        alf = set(
            a.strip()
            for a in alfabeto.value.split(",")
            if a.strip()
        )

        fin = set(
            f.strip()
            for f in finales.value.split(",")
            if f.strip()
        )

        trans = {}

        for r in transiciones.value.split(";"):

            if not r.strip():
                continue

            izq, der = r.split("->")

            origen, simbolo = izq.split(",")

            trans[
                (
                    origen.strip(),
                    simbolo.strip()
                )
            ] = der.strip()

        return est, alf, fin, trans

    # ==================================================
    # VISUALIZAR
    # ==================================================

    def generar_visual(e):

        try:

            est, alf, fin, trans = parsear()

            errores = validar_afd(
                est,
                alf,
                inicial.value,
                fin
            )

            if errores:

                resultado.value = "\n".join(errores)

                page.update()

                return

            ruta_img = RenderizadorAutomata.generar_afd(
                est,
                inicial.value,
                fin,
                trans
            )

            imagen.src = ruta_img
            imagen.update()

            resultado.value = (
                "Diagrama generado correctamente."
            )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # SIMULAR
    # ==================================================

    def simular(e):

        try:

            est, alf, fin, trans = parsear()

            consola.controls.clear()

            # ================= AFD =================

            if tipo.value == "AFD":

                afd = AFD(
                    est,
                    alf,
                    inicial.value,
                    fin,
                    trans
                )

                simulador = SimuladorVisual(afd)

                aceptada, pasos = simulador.recorrer(
                    cadena.value
                )

                for paso in pasos:

                    texto = (
                        f"Símbolo: {paso['simbolo']} "
                        f"| Estado: {paso['estado']}"
                    )

                    consola.controls.append(
                        ft.Text(texto)
                    )

                resultado.value = (
                    "Cadena ACEPTADA"
                    if aceptada
                    else "Cadena RECHAZADA"
                )

            else:

                resultado.value = (
                    "La simulación visual actual "
                    "solo está disponible para AFD."
                )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # MINIMIZAR
    # ==================================================

    def minimizar(e):

        try:

            est, alf, fin, trans = parsear()

            afd = AFD(
                est,
                alf,
                inicial.value,
                fin,
                trans
            )

            est2, ini2, fin2, trans2, tabla = minimizar_afd(
                afd
            )

            resultado.value = (
                f"AFD mínimo generado.\n"
                f"Estados: {est2}"
            )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # AFND -> AFD
    # ==================================================

    def convertir(e):

        try:

            est, alf, fin, trans = parsear()

            afnd = AFND(
                est,
                alf,
                inicial.value,
                fin,
                trans
            )

            estados_afd, ini, fin_afd, trans_afd = (
                convertir_afnd_a_afd(afnd)
            )

            resultado.value = (
                "Conversión completada correctamente."
            )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # ELIMINAR λ
    # ==================================================

    def eliminar_lambda_ui(e):

        try:

            est, alf, fin, trans = parsear()

            afndl = AFNDLambda(
                est,
                alf,
                inicial.value,
                fin,
                trans
            )

            eliminar_lambda(afndl)

            resultado.value = (
                "Transiciones λ eliminadas."
            )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # AFD -> ER
    # ==================================================

    def convertir_er(e):

        try:

            est, alf, fin, trans = parsear()

            afd = AFD(
                est,
                alf,
                inicial.value,
                fin,
                trans
            )

            er = afd_a_er(afd)

            resultado.value = (
                f"Expresión regular:\n{er}"
            )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # JFF
    # ==================================================

    def cargar_jff(e):

        try:

            est, alf, ini, fin, trans = leer_jff(
                ruta.value
            )

            estados.value = ",".join(est)
            alfabeto.value = ",".join(alf)

            inicial.value = ini

            finales.value = ",".join(fin)

            reglas = []

            for (o, s), d in trans.items():

                if isinstance(d, list):

                    reglas.append(
                        f"{o},{s}->{d[0]}"
                    )

                else:

                    reglas.append(
                        f"{o},{s}->{d}"
                    )

            transiciones.value = ";".join(reglas)

            resultado.value = (
                "Archivo JFLAP cargado."
            )

        except Exception as ex:

            resultado.value = f"Error: {ex}"

        page.update()

    # ==================================================
    # VALIDADORES
    # ==================================================

    def validar_email(e):

        ok = validar_regex(
            "email",
            regex_input.value
        )

        resultado.value = (
            "Correo válido"
            if ok
            else "Correo inválido"
        )

        page.update()

    def validar_telefono(e):

        ok = validar_regex(
            "telefono",
            regex_input.value
        )

        resultado.value = (
            "Teléfono válido"
            if ok
            else "Teléfono inválido"
        )

        page.update()

    def validar_password(e):

        ok = validar_regex(
            "password",
            regex_input.value
        )

        resultado.value = (
            "Contraseña válida"
            if ok
            else "Contraseña inválida"
        )

        page.update()

    # ==================================================
    # EXTRAS
    # ==================================================

    def ver_prefijos(e):

        resultado.value = str(
            prefijos(cadena.value)
        )

        page.update()

    def ver_sufijos(e):

        resultado.value = str(
            sufijos(cadena.value)
        )

        page.update()

    def ver_subcadenas(e):

        resultado.value = str(
            subcadenas(cadena.value)
        )

        page.update()

    def ver_kleene(e):

        resultado.value = str(
            kleene(
                alfabeto.value.split(",")
            )
        )

        page.update()

    # ==================================================
    # PANTALLAS
    # ==================================================

    def vista_inicio():

        contenido.content = ft.Column([

            ft.Text(
                "Simulador de Autómatas",
                size=34,
                weight="bold"
            ),

            ft.Text(
                "Desarrollo de prácticas - "
                "Teoría de la Computación."
                " - 4CM4 HERNANDEZ RIOS "
                "CRISTIAN SEBASTIAN"
            ),

            ft.Divider(),

            ft.Text(
                "Seleccione una herramienta "
                "desde el menú lateral."
            )

        ])

        page.update()

    def vista_automatas():

        contenido.content = ft.Row([

            ft.Container(

                content=ft.Column([

                    tipo,
                    estados,
                    alfabeto,
                    inicial,
                    finales,
                    transiciones,
                    ruta,

                    ft.ElevatedButton(
                        "Cargar JFF",
                        on_click=cargar_jff
                    ),

                    ft.ElevatedButton(
                        "Generar Diagrama",
                        on_click=generar_visual
                    ),

                    cadena,

                    ft.ElevatedButton(
                        "Simular",
                        on_click=simular
                    ),

                    ft.ElevatedButton(
                        "Minimizar AFD",
                        on_click=minimizar
                    ),

                    ft.ElevatedButton(
                        "AFND → AFD",
                        on_click=convertir
                    ),

                    ft.ElevatedButton(
                        "Eliminar λ",
                        on_click=eliminar_lambda_ui
                    ),

                    ft.ElevatedButton(
                        "AFD → ER",
                        on_click=convertir_er
                    ),

                    resultado

                ],
                scroll="auto"),

                width=420,
                padding=20,
                bgcolor="#1f1f1f"

            ),

            ft.Container(

                content=ft.Column([

                    ft.Text(
                        "Visualización",
                        size=28,
                        weight="bold"
                    ),

                    imagen,

                    ft.Divider(),

                    ft.Text(
                        "Consola",
                        size=22,
                        weight="bold"
                    ),

                    ft.Container(
                        content=consola,
                        bgcolor="#111111",
                        padding=10,
                        border_radius=10,
                        height=250
                    )

                ]),

                expand=True,
                padding=20

            )

        ],
        expand=True)

        page.update()

    def vista_validadores():

        contenido.content = ft.Column([

            ft.Text(
                "Validadores Regex",
                size=30,
                weight="bold"
            ),

            regex_input,

            ft.Row([

                ft.ElevatedButton(
                    "Validar Email",
                    on_click=validar_email
                ),

                ft.ElevatedButton(
                    "Validar Teléfono",
                    on_click=validar_telefono
                ),

                ft.ElevatedButton(
                    "Validar Contraseña",
                    on_click=validar_password
                )

            ]),

            resultado

        ])

        page.update()

    def vista_extras():

        contenido.content = ft.Column([

            ft.Text(
                "Operaciones Extra",
                size=30,
                weight="bold"
            ),

            cadena,

            ft.Row([

                ft.ElevatedButton(
                    "Prefijos",
                    on_click=ver_prefijos
                ),

                ft.ElevatedButton(
                    "Sufijos",
                    on_click=ver_sufijos
                ),

                ft.ElevatedButton(
                    "Subcadenas",
                    on_click=ver_subcadenas
                ),

                ft.ElevatedButton(
                    "Kleene",
                    on_click=ver_kleene
                )

            ]),

            resultado

        ])

        page.update()

    # ==================================================
    # SIDEBAR
    # ==================================================

    sidebar = ft.Container(

        content=ft.Column([

            ft.Text(
                "MENÚ",
                size=28,
                weight="bold"
            ),

            ft.ElevatedButton(
                "Inicio",
                on_click=lambda e: vista_inicio()
            ),

            ft.ElevatedButton(
                "Autómatas",
                on_click=lambda e: vista_automatas()
            ),

            ft.ElevatedButton(
                "Validadores",
                on_click=lambda e: vista_validadores()
            ),

            ft.ElevatedButton(
                "Extras",
                on_click=lambda e: vista_extras()
            )

        ]),

        width=240,
        padding=20,
        bgcolor="#181818"
    )

    # ==================================================
    # LAYOUT FINAL
    # ==================================================

    page.add(

        ft.Row([

            sidebar,
            contenido

        ],
        expand=True)

    )

    vista_inicio()


ft.app(target=main)