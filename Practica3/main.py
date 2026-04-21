import flet as ft

from automatas.afd import AFD
from automatas.afnd import AFND
from automatas.afnd_lambda import AFNDLambda
from automatas.conversion import convertir_afnd_a_afd, eliminar_lambda
from automatas.minimizacion import minimizar_afd

from utils.jff_reader import leer_jff
from extras.operaciones import subcadenas, prefijos, sufijos, kleene


def main(page: ft.Page):
    page.title = "Simulador de Autómatas"
    page.theme_mode = "dark"
    page.scroll = "auto"

    # ===================== INPUTS =====================
    tipo = ft.Dropdown(
        label="Tipo de autómata",
        options=[
            ft.dropdown.Option("AFD"),
            ft.dropdown.Option("AFND"),
            ft.dropdown.Option("AFND-λ"),
        ],
        value="AFD"
    )

    estados = ft.TextField(label="Estados (q0,q1,q2)")
    alfabeto = ft.TextField(label="Alfabeto (0,1,λ)")
    inicial = ft.TextField(label="Estado inicial")
    finales = ft.TextField(label="Estados finales")
    transiciones = ft.TextField(label="Transiciones", multiline=True)

    ruta = ft.TextField(label="Ruta archivo .jff")
    cadena = ft.TextField(label="Cadena")

    resultado = ft.Text()
    tabla = ft.Column()
    salida = ft.Text()

    # ===================== PARSE =====================
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

    # ===================== VALIDAR =====================
    def validar(e):
        try:
            est, alf, fin, trans = parsear()

            if tipo.value == "AFD":
                t = {k: v[0] for k, v in trans.items()}
                afd = AFD(est, alf, inicial.value, fin, t)
                ok, rec, _ = afd.validar(cadena.value)

            elif tipo.value == "AFND":
                afnd = AFND(est, alf, inicial.value, fin, trans)
                ok, rec = afnd.validar(cadena.value)

            else:
                afndl = AFNDLambda(est, alf, inicial.value, fin, trans)
                ok, rec = afndl.validar(cadena.value)

            # 🔥 Tabla paso a paso
            tabla.controls = [
                ft.Text(f"Paso {i}: {r}") for i, r in enumerate(rec)
            ]

            resultado.value = "ACEPTADA" if ok else "RECHAZADA"

        except Exception as ex:
            resultado.value = f"Error: {ex}"

        page.update()

    # ===================== CARGAR JFF =====================
    def cargar(e):
        try:
            est, alf, ini, fin, trans = leer_jff(ruta.value)

            estados.value = ",".join(est)
            alfabeto.value = ",".join(alf)
            inicial.value = ini
            finales.value = ",".join(fin)

            reglas = []
            for (o, s), d in trans.items():
                reglas.append(f"{o},{s}->{','.join(d)}")

            transiciones.value = " ; ".join(reglas)

            resultado.value = "Archivo cargado correctamente"

        except Exception as ex:
            resultado.value = f"Error: {ex}"

        page.update()

    # ===================== ELIMINAR λ =====================
    def eliminar_lambda_ui(e):
        try:
            est, alf, fin, trans = parsear()

            afndl = AFNDLambda(est, alf, inicial.value, fin, trans)
            est2, alf2, ini2, fin2, trans2 = eliminar_lambda(afndl)

            salida.value = f"AFND sin λ:\n{trans2}"

        except Exception as ex:
            salida.value = f"Error: {ex}"

        page.update()

    # ===================== CONVERTIR =====================
    def convertir(e):
        try:
            est, alf, fin, trans = parsear()

            afnd = AFND(est, alf, inicial.value, fin, trans)
            estados_afd, ini, fin_afd, trans_afd = convertir_afnd_a_afd(afnd)

            salida.value = f"AFD generado:\n{estados_afd}"

        except Exception as ex:
            salida.value = f"Error: {ex}"

        page.update()

    # ===================== MINIMIZAR =====================
    def minimizar(e):
        try:
            est, alf, fin, trans = parsear()

            t = {k: v[0] for k, v in trans.items()}
            afd = AFD(est, alf, inicial.value, fin, t)

            est2, ini2, fin2, trans2, tabla_res = minimizar_afd(afd)

            tabla.controls = [
                ft.Text(f"{k} -> {'X' if v else ''}") for k, v in tabla_res.items()
            ]

            salida.value = f"AFD mínimo con {len(est2)} estados:\n{est2}"

        except Exception as ex:
            salida.value = f"Error: {ex}"

        page.update()

    # ===================== EXTRAS =====================
    def ver_sub(e):
        salida.value = "Subcadenas:\n" + str(subcadenas(cadena.value))
        page.update()

    def ver_pref(e):
        salida.value = "Prefijos:\n" + str(prefijos(cadena.value))
        page.update()

    def ver_suf(e):
        salida.value = "Sufijos:\n" + str(sufijos(cadena.value))
        page.update()

    def ver_kleene(e):
        salida.value = "Kleene:\n" + str(kleene(alfabeto.value.split(",")))
        page.update()

    # ===================== UI =====================
    page.add(
        ft.Column([
            ft.Text("Simulador de Autómatas", size=30, weight="bold"),

            ft.Card(content=ft.Container(
                content=ft.Column([
                    tipo,
                    estados,
                    alfabeto,
                    inicial,
                    finales,
                    transiciones
                ]),
                padding=15
            )),

            ft.Row([
                ruta,
                ft.ElevatedButton("Cargar JFF", on_click=cargar)
            ]),

            cadena,

            ft.Row([
                ft.ElevatedButton("Validar", on_click=validar),
                ft.ElevatedButton("Eliminar λ", on_click=eliminar_lambda_ui),
                ft.ElevatedButton("Convertir AFND→AFD", on_click=convertir),
                ft.ElevatedButton("Minimizar AFD", on_click=minimizar),
            ]),

            resultado,

            ft.Divider(),
            ft.Text("Proceso paso a paso"),
            tabla,

            ft.Divider(),
            ft.Text("Extras"),
            ft.Row([
                ft.ElevatedButton("Subcadenas", on_click=ver_sub),
                ft.ElevatedButton("Prefijos", on_click=ver_pref),
                ft.ElevatedButton("Sufijos", on_click=ver_suf),
                ft.ElevatedButton("Kleene", on_click=ver_kleene),
            ]),

            salida
        ])
    )


ft.app(target=main)