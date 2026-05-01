import flet as ft

from automatas.afd import AFD
from automatas.afnd import AFND
from automatas.afnd_lambda import AFNDLambda
from automatas.conversion import convertir_afnd_a_afd, eliminar_lambda
from automatas.minimizacion import minimizar_afd

from utils.jff_reader import leer_jff
from extras.operaciones import subcadenas, prefijos, sufijos, kleene

from automatas.afd_to_er import afd_a_er
from extras.validadores import validar as validar_regex


def main(page: ft.Page):
    page.title = "Simulador de Automatas"
    page.scroll = "auto"
    page.horizontal_alignment = "center"

    # ================= COMPONENTES =================
    tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("AFD"),
            ft.dropdown.Option("AFND"),
            ft.dropdown.Option("AFND-λ"),
        ],
        value="AFD"
    )

    estados = ft.TextField(label="Estados (q0,q1)")
    alfabeto = ft.TextField(label="Alfabeto (0,1)")
    inicial = ft.TextField(label="Inicial")
    finales = ft.TextField(label="Finales")
    transiciones = ft.TextField(label="Transiciones", multiline=True)

    ruta = ft.TextField(label="Ruta .jff")
    cadena = ft.TextField(label="Cadena")

    entrada_regex = ft.TextField(label="Texto a validar")
    tipo_regex = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("email"),
            ft.dropdown.Option("telefono"),
            ft.dropdown.Option("password"),
        ],
        value="email"
    )

    resultado = ft.Text()
    resultado_regex = ft.Text()
    tabla = ft.Column()
    salida = ft.Text()

    contenido = ft.Column(horizontal_alignment="center", spacing=20)

    # ================= UTIL =================
    def limpiar():
        contenido.controls.clear()

    def card(titulo, controls):
        return ft.Container(
            content=ft.Column(
                [ft.Text(titulo, size=20, weight="bold")] + controls,
                spacing=10
            ),
            padding=20,
            border_radius=10,
            bgcolor="#f5f5f5",
            width=500
        )

    def parsear():
        est = set(estados.value.split(","))
        alf = set(alfabeto.value.split(","))
        fin = set(finales.value.split(","))

        trans = {}
        for r in transiciones.value.split(";"):
            if not r.strip():
                continue
            izq, der = r.split("->")
            s, c = izq.split(",")
            trans[(s.strip(), c.strip())] = [d.strip() for d in der.split(",")]

        return est, alf, fin, trans

    # ================= FUNCIONES =================
    def validar(e):
        try:
            est, alf, fin, trans = parsear()
            t = {k: v[0] for k, v in trans.items()}
            afd = AFD(est, alf, inicial.value, fin, t)

            ok, rec, _ = afd.validar(cadena.value)

            tabla.controls = [
                ft.Text("Paso " + str(i) + ": " + str(r))
                for i, r in enumerate(rec)
            ]

            resultado.value = "ACEPTADA" if ok else "RECHAZADA"

        except Exception as ex:
            resultado.value = "Error: " + str(ex)

        page.update()

    def cargar(e):
        try:
            est, alf, ini, fin, trans = leer_jff(ruta.value)

            estados.value = ",".join(est)
            alfabeto.value = ",".join(alf)
            inicial.value = ini
            finales.value = ",".join(fin)

            reglas = []
            for (o, s), d in trans.items():
                reglas.append(o + "," + s + "->" + ",".join(d))

            transiciones.value = " ; ".join(reglas)
            resultado.value = "Archivo cargado"

        except Exception as ex:
            resultado.value = "Error: " + str(ex)

        page.update()

    def convertir_er(e):
        try:
            est, _, fin, trans = parsear()
            t = {k: v[0] for k, v in trans.items()}

            pasos, er = afd_a_er(est, inicial.value, fin, t)

            tabla.controls = [ft.Text(p) for p in pasos]
            salida.value = er

        except Exception as ex:
            salida.value = "Error: " + str(ex)

        page.update()

    def validar_regex_ui(e):
        ok, patron, msg = validar_regex(tipo_regex.value, entrada_regex.value)

        resultado_regex.value = msg + "\nRegex: " + patron
        if not ok:
            resultado_regex.value += "\nSugerencia: revisa el formato"

        page.update()

    def ver_sub(e):
        salida.value = str(subcadenas(cadena.value))
        page.update()

    def ver_pref(e):
        salida.value = str(prefijos(cadena.value))
        page.update()

    def ver_suf(e):
        salida.value = str(sufijos(cadena.value))
        page.update()

    def ver_kleene(e):
        salida.value = str(kleene(alfabeto.value.split(",")))
        page.update()

    # ================= VISTAS =================
    def vista_menu(e=None):
        limpiar()
        contenido.controls.extend([
            ft.Text("Simulador de Autómatas", size=30, weight="bold"),

            ft.ElevatedButton("Autómatas", width=250, on_click=vista_automatas),
            ft.ElevatedButton("Validadores", width=250, on_click=vista_validadores),
            ft.ElevatedButton("Extras", width=250, on_click=vista_extras),
        ])
        page.update()

    def vista_automatas(e):
        limpiar()
        contenido.controls.append(
            card("Autómatas", [
                tipo, estados, alfabeto, inicial, finales, transiciones,
                ft.Row([ruta, ft.ElevatedButton("Cargar", on_click=cargar)]),
                cadena,
                ft.Row([
                    ft.ElevatedButton("Validar", on_click=validar),
                    ft.ElevatedButton("AFD → ER", on_click=convertir_er),
                ]),
                resultado,
                tabla,
                salida,
                ft.ElevatedButton("Volver", on_click=vista_menu)
            ])
        )
        page.update()

    def vista_validadores(e):
        limpiar()
        contenido.controls.append(
            card("Validadores", [
                tipo_regex,
                entrada_regex,
                ft.ElevatedButton("Validar", on_click=validar_regex_ui),
                resultado_regex,
                ft.ElevatedButton("Volver", on_click=vista_menu)
            ])
        )
        page.update()

    def vista_extras(e):
        limpiar()
        contenido.controls.append(
            card("Extras", [
                cadena,
                ft.Row([
                    ft.ElevatedButton("Subcadenas", on_click=ver_sub),
                    ft.ElevatedButton("Prefijos", on_click=ver_pref),
                    ft.ElevatedButton("Sufijos", on_click=ver_suf),
                    ft.ElevatedButton("Kleene", on_click=ver_kleene),
                ]),
                salida,
                ft.ElevatedButton("Volver", on_click=vista_menu)
            ])
        )
        page.update()

    # ================= INICIO =================
    vista_menu()
    page.add(contenido)


ft.app(target=main)
