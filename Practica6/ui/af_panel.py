"""
Panel para Autómatas Finitos (AFD, AFND, AFND-λ).
"""

import os
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

from utils.jff_reader import leer_jff, detectar_tipo
from utils.jff_writer import (
    escribir_jff_fa,
    escribir_json_fa,
    escribir_xml_fa
)
from utils.renderizador import generar_fa
from utils.validators import validar_afd

from ui.tema import COLORES, TAMS
from ui.components import (
    boton_primario, boton_secundario, boton_peligro,
    campo_texto, caja_resultado
)


def construir_panel_af(page: ft.Page):

    estado = {
        "tipo": "AFD",
        "estados": set(),
        "alfabeto": set(),
        "inicial": "",
        "finales": set(),
        "transiciones": {},
    }

    # ---------- Campos ----------
    f_tipo = ft.Dropdown(
        label="Tipo de autómata",
        options=[
            ft.dropdown.Option("AFD"),
            ft.dropdown.Option("AFND"),
            ft.dropdown.Option("AFND-λ"),
        ],
        value="AFD",
        border_color=COLORES["border"],
        focused_border_color=COLORES["primary"],
        bgcolor=COLORES["surface_alt"],
        label_style=ft.TextStyle(color=COLORES["text_dim"], size=12),
        text_style=ft.TextStyle(color=COLORES["text"], size=14)
    )

    f_estados = campo_texto("Estados", "q0, q1, q2")
    f_alfabeto = campo_texto("Alfabeto", "0, 1")
    f_inicial = campo_texto("Estado inicial", "q0")
    f_finales = campo_texto("Estados finales", "q2")
    f_transiciones = campo_texto(
        "Transiciones",
        "q0, 0 -> q1; q1, 1 -> q2;\n(o una por línea)",
        multilinea=True
    )
    f_cadena = campo_texto("Cadena a validar", "0011")

    txt_resultado = ft.Text("", size=14, color=COLORES["text"])

    # No creamos ft.Image() vacío porque en Flet 0.25+ `src` es obligatorio.
    # El Image se construye dentro de actualizar_imagen() con el path real.
    contenedor_img = ft.Container(
        content=ft.Text(
            "Genere un diagrama para visualizar el autómata.",
            color=COLORES["text_dim"],
            italic=True
        ),
        bgcolor="#FAFAFA",
        border_radius=10,
        padding=12,
        border=ft.border.all(1, COLORES["border"]),
        alignment=ft.Alignment(0, 0),
        height=420
    )

    consola = ft.Column(scroll="auto", spacing=2)
    contenedor_consola = ft.Container(
        content=consola,
        bgcolor=COLORES["bg"],
        border_radius=8,
        padding=10,
        height=180,
        border=ft.border.all(1, COLORES["border"])
    )

    archivo_picker = ft.FilePicker()
    guardar_picker = ft.FilePicker()
    page.overlay.append(archivo_picker)
    page.overlay.append(guardar_picker)

    # ---------- Helpers ----------
    def mostrar(msg, color=None):
        txt_resultado.value = msg
        txt_resultado.color = color or COLORES["text"]
        page.update()

    def log(msg, color=None):
        consola.controls.append(
            ft.Text(
                msg,
                size=12,
                color=color or COLORES["text"],
                font_family="Courier New",
                selectable=True
            )
        )
        consola.update()

    def parsear():
        est = {
            e.strip()
            for e in f_estados.value.split(",")
            if e.strip()
        }
        alf = {
            a.strip()
            for a in f_alfabeto.value.split(",")
            if a.strip()
        }
        fin = {
            e.strip()
            for e in f_finales.value.split(",")
            if e.strip()
        }

        trans = {}
        crudo = (f_transiciones.value or "")\
            .replace("\n", ";").replace("\r", ";")

        for regla in crudo.split(";"):
            regla = regla.strip()
            if not regla:
                continue
            if "->" not in regla:
                raise ValueError(f"Falta '->' en: {regla!r}")
            izq, der = regla.split("->", 1)
            partes = [p.strip() for p in izq.split(",")]
            if len(partes) != 2:
                raise ValueError(
                    f"Formato 'estado, simbolo' en: {regla!r}"
                )
            o, s = partes
            destinos = [d.strip() for d in der.split(",") if d.strip()]

            if (o, s) in trans:
                if isinstance(trans[(o, s)], list):
                    trans[(o, s)].extend(destinos)
                else:
                    trans[(o, s)] = [trans[(o, s)]] + destinos
            else:
                if f_tipo.value == "AFD":
                    trans[(o, s)] = destinos[0]
                else:
                    trans[(o, s)] = destinos

        return est, alf, fin, trans

    def actualizar_imagen(ruta):
        try:
            # Leemos el PNG como base64 y se lo pasamos a Flet directamente.
            # Este método no depende de paths, assets_dir, ni nada externo
            # y funciona consistentemente en todas las versiones de Flet.
            import base64
            with open(ruta, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            nueva_img = ft.Image(
                src_base64=b64,
                width=720,
                height=400,
                fit="contain"
            )
            contenedor_img.content = nueva_img
            contenedor_img.update()
        except Exception as ex:
            mostrar(f"Error mostrando imagen: {ex}", COLORES["error"])

    # ---------- Handlers ----------
    def on_generar(e):
        try:
            est, alf, fin, trans = parsear()
            errores = validar_afd(est, alf, f_inicial.value, fin)
            if errores:
                mostrar(
                    "Errores:\n• " + "\n• ".join(errores),
                    COLORES["error"]
                )
                return

            ruta = generar_fa(
                est,
                f_inicial.value,
                fin,
                trans,
                nombre_archivo="af_diagram"
            )
            actualizar_imagen(ruta)
            mostrar(
                "Diagrama generado correctamente.",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_simular(e):
        try:
            est, alf, fin, trans = parsear()
            consola.controls.clear()
            log(
                f"=== Simulando ({f_tipo.value}) ===",
                COLORES["accent"]
            )
            log(f"Cadena: {f_cadena.value!r}")
            log("─" * 50, COLORES["text_dim"])

            if f_tipo.value == "AFD":
                afd = AFD(est, alf, f_inicial.value, fin, trans)
                aceptada, pasos = afd.simular_paso_a_paso(
                    f_cadena.value or ""
                )
                for p in pasos:
                    color = (
                        COLORES["success"]
                        if p.get("ok", True)
                        else COLORES["error"]
                    )
                    log(
                        f"Paso {p['paso']:>2} | "
                        f"símbolo: {p['simbolo']:>6} | "
                        f"estado: {p['estado']}",
                        color
                    )
            elif f_tipo.value == "AFND":
                afnd = AFND(est, alf, f_inicial.value, fin, trans)
                aceptada, pasos = afnd.simular_paso_a_paso(
                    f_cadena.value or ""
                )
                for p in pasos:
                    log(
                        f"Paso {p['paso']:>2} | "
                        f"símbolo: {p['simbolo']:>6} | "
                        f"estados: {p['estados']}"
                    )
            else:  # AFND-λ
                afndl = AFNDLambda(
                    est, alf, f_inicial.value, fin, trans
                )
                aceptada, pasos = afndl.simular_paso_a_paso(
                    f_cadena.value or ""
                )
                for p in pasos:
                    log(
                        f"Paso {p['paso']:>2} | "
                        f"símbolo: {p['simbolo']:>6} | "
                        f"estados: {p['estados']}"
                    )

            log("─" * 50, COLORES["text_dim"])
            if aceptada:
                log(
                    "✓ CADENA ACEPTADA",
                    COLORES["success"]
                )
                mostrar("Cadena ACEPTADA", COLORES["success"])
            else:
                log(
                    "✗ CADENA RECHAZADA",
                    COLORES["error"]
                )
                mostrar("Cadena RECHAZADA", COLORES["error"])
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_minimizar(e):
        try:
            est, alf, fin, trans = parsear()
            afd = AFD(est, alf, f_inicial.value, fin, trans)

            nuevos, ini, finales_n, trans_n, _ = minimizar_afd(afd)

            consola.controls.clear()
            log("=== Minimización de AFD ===", COLORES["accent"])
            log(f"Estados originales: {len(est)}")
            log(f"Estados minimizados: {len(nuevos)}")
            log("Grupos de estados equivalentes:")
            for g in nuevos:
                log(f"  • {set(g)}")
            mostrar(
                f"AFD minimizado: {len(est)} → {len(nuevos)} estados",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_convertir_afnd_afd(e):
        try:
            est, alf, fin, trans = parsear()
            afnd = AFND(est, alf, f_inicial.value, fin, trans)
            nuevos, ini, finales_n, trans_n = (
                convertir_afnd_a_afd(afnd)
            )

            consola.controls.clear()
            log("=== AFND → AFD ===", COLORES["accent"])
            log(f"Estados resultantes: {len(nuevos)}")
            for s in nuevos:
                marca = " (final)" if s in finales_n else ""
                log(f"  {set(s)}{marca}")
            log("Transiciones:")
            for (o, s), d in trans_n.items():
                log(f"  δ({set(o)}, {s}) = {set(d)}")
            mostrar(
                f"Conversión completada: "
                f"{len(nuevos)} estados resultantes",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_eliminar_lambda(e):
        try:
            est, alf, fin, trans = parsear()
            afndl = AFNDLambda(
                est, alf, f_inicial.value, fin, trans
            )
            (
                estados_n, alf_n, ini_n,
                finales_n, trans_n
            ) = eliminar_lambda(afndl)

            consola.controls.clear()
            log("=== Eliminación de λ ===", COLORES["accent"])
            log(f"Estados: {estados_n}")
            log(f"Alfabeto: {alf_n}")
            log(f"Finales: {finales_n}")
            log("Transiciones (sin λ):")
            for k, v in trans_n.items():
                log(f"  δ{k} = {v}")
            mostrar(
                "Transiciones λ eliminadas.",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_afd_to_er(e):
        try:
            est, alf, fin, trans = parsear()
            afd = AFD(est, alf, f_inicial.value, fin, trans)
            pasos, er = afd_a_er(afd)

            consola.controls.clear()
            log("=== AFD → ER ===", COLORES["accent"])
            for p in pasos:
                log(p)
            log("─" * 50, COLORES["text_dim"])
            log(f"ER = {er}", COLORES["warning"])
            mostrar(f"Expresión regular: {er}", COLORES["success"])
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_cargar_jff_resultado(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        ruta = e.files[0].path
        try:
            tipo = detectar_tipo(ruta)
            if tipo not in ("fa", ""):
                mostrar(
                    f"El archivo es de tipo '{tipo}', no es un AF. "
                    f"Use el panel del PDA si corresponde.",
                    COLORES["warning"]
                )
                return

            est, alf, ini, fin, trans = leer_jff(ruta)

            f_estados.value = ", ".join(sorted(est))
            f_alfabeto.value = ", ".join(sorted(alf))
            f_inicial.value = ini or ""
            f_finales.value = ", ".join(sorted(fin))

            reglas = []
            tiene_lambda = False
            tiene_multiple = False
            for (o, s), destinos in trans.items():
                if s == "λ":
                    tiene_lambda = True
                if len(destinos) > 1:
                    tiene_multiple = True
                for d in destinos:
                    reglas.append(f"{o}, {s} -> {d}")

            f_transiciones.value = "\n".join(reglas)

            # Sugerir tipo
            if tiene_lambda:
                f_tipo.value = "AFND-λ"
            elif tiene_multiple:
                f_tipo.value = "AFND"
            else:
                f_tipo.value = "AFD"

            for w in [
                f_estados, f_alfabeto, f_inicial, f_finales,
                f_transiciones, f_tipo
            ]:
                w.update()

            mostrar(
                f"Archivo cargado: {os.path.basename(ruta)} "
                f"(tipo sugerido: {f_tipo.value})",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error al cargar: {ex}", COLORES["error"])

    archivo_picker.on_result = on_cargar_jff_resultado

    def on_guardar_resultado(e: ft.FilePickerResultEvent):
        if not e.path:
            return
        ruta = e.path
        try:
            est, alf, fin, trans = parsear()
            base, ext = os.path.splitext(ruta)
            if not ext:
                # guardar en los tres formatos
                escribir_jff_fa(
                    base + ".jff", est,
                    f_inicial.value, fin, trans
                )
                escribir_json_fa(
                    base + ".json", est, alf,
                    f_inicial.value, fin, trans
                )
                escribir_xml_fa(
                    base + ".xml", est, alf,
                    f_inicial.value, fin, trans
                )
                mostrar(
                    f"Guardado en .jff, .json y .xml:\n{base}.*",
                    COLORES["success"]
                )
            elif ext.lower() == ".jff":
                escribir_jff_fa(
                    ruta, est, f_inicial.value, fin, trans
                )
                mostrar(
                    f"Guardado: {ruta}",
                    COLORES["success"]
                )
            elif ext.lower() == ".json":
                escribir_json_fa(
                    ruta, est, alf, f_inicial.value, fin, trans
                )
                mostrar(
                    f"Guardado: {ruta}",
                    COLORES["success"]
                )
            elif ext.lower() == ".xml":
                escribir_xml_fa(
                    ruta, est, alf, f_inicial.value, fin, trans
                )
                mostrar(
                    f"Guardado: {ruta}",
                    COLORES["success"]
                )
            else:
                mostrar(
                    f"Extensión no soportada: {ext}",
                    COLORES["error"]
                )
        except Exception as ex:
            mostrar(f"Error al guardar: {ex}", COLORES["error"])

    guardar_picker.on_result = on_guardar_resultado

    def on_btn_cargar(e):
        archivo_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jff", "xml"]
        )

    def on_btn_guardar(e):
        guardar_picker.save_file(
            file_name="mi_automata",
            allowed_extensions=["jff", "json", "xml"]
        )

    def on_limpiar(e):
        for w in [
            f_estados, f_alfabeto, f_inicial, f_finales,
            f_transiciones, f_cadena
        ]:
            w.value = ""
            w.update()
        consola.controls.clear()
        consola.update()
        contenedor_img.content = ft.Text(
            "Genere un diagrama para visualizar el autómata.",
            color=COLORES["text_dim"],
            italic=True
        )
        contenedor_img.update()
        mostrar("Formulario limpiado.", COLORES["info"])

    # ---------- Layout ----------
    col_izq = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "DEFINICIÓN",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                f_tipo,
                f_estados,
                f_alfabeto,
                f_inicial,
                f_finales,
                f_transiciones,
                ft.Row(
                    controls=[
                        boton_primario(
                            "Generar diagrama",
                            on_generar,
                            icono=ft.Icons.AUTO_GRAPH
                        ),
                        boton_secundario(
                            "Cargar .jff",
                            on_btn_cargar,
                            icono=ft.Icons.FOLDER_OPEN
                        )
                    ],
                    spacing=8,
                    wrap=True
                ),
                boton_secundario(
                    "Guardar (.jff / .json / .xml)",
                    on_btn_guardar,
                    icono=ft.Icons.SAVE
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                f_cadena,
                ft.Row(
                    controls=[
                        boton_primario(
                            "Simular",
                            on_simular,
                            icono=ft.Icons.PLAY_ARROW
                        ),
                    ],
                    spacing=8
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                ft.Text(
                    "Operaciones",
                    weight="bold",
                    color=COLORES["text_strong"],
                    size=13
                ),
                ft.Row(
                    controls=[
                        boton_secundario(
                            "Minimizar AFD", on_minimizar
                        ),
                        boton_secundario(
                            "AFND → AFD", on_convertir_afnd_afd
                        ),
                    ],
                    spacing=8,
                    wrap=True
                ),
                ft.Row(
                    controls=[
                        boton_secundario(
                            "Eliminar λ", on_eliminar_lambda
                        ),
                        boton_secundario(
                            "AFD → ER", on_afd_to_er
                        ),
                    ],
                    spacing=8,
                    wrap=True
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                boton_peligro(
                    "Limpiar todo",
                    on_limpiar,
                    icono=ft.Icons.DELETE_SWEEP
                )
            ],
            scroll="auto",
            spacing=10
        ),
        width=440,
        padding=18,
        bgcolor=COLORES["surface"],
        border_radius=12,
        border=ft.border.all(1, COLORES["border"])
    )

    col_der = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "VISUALIZACIÓN",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                contenedor_img,
                ft.Divider(height=1, color=COLORES["border"]),
                ft.Text(
                    "Consola",
                    weight="bold",
                    color=COLORES["text_strong"],
                    size=14
                ),
                contenedor_consola,
                ft.Divider(height=1, color=COLORES["border"]),
                ft.Text(
                    "Mensajes",
                    weight="bold",
                    color=COLORES["text_strong"],
                    size=14
                ),
                caja_resultado(txt_resultado)
            ],
            scroll="auto",
            spacing=10
        ),
        expand=True,
        padding=18,
        bgcolor=COLORES["surface"],
        border_radius=12,
        border=ft.border.all(1, COLORES["border"])
    )

    return ft.Row(
        controls=[col_izq, col_der],
        spacing=12,
        expand=True
    )
