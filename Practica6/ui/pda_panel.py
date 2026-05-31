"""
Panel completo del simulador de Autómatas de Pila (PDA).
Práctica 6 - Teoría de la Computación.

Características:
  - Definición manual del PDA
  - Importación de archivos .jff
  - Visualización gráfica con Graphviz
  - Simulación paso a paso con animación
  - Visualización de la pila en tiempo real
  - Tabla con la traza completa
  - Exportación a .jff y .json
"""

import os
import flet as ft

from automatas.pda import PDA
from utils.jff_reader import leer_jff_pda
from utils.jff_writer import escribir_jff_pda, escribir_json_pda
from utils.renderizador import generar_pda
from utils.parser_pda import (
    parsear_transiciones_pda,
    serializar_transiciones_pda
)

from ui.tema import COLORES, TAMS
from ui.components import (
    card, badge, boton_primario, boton_secundario,
    boton_peligro, campo_texto, caja_resultado,
    tabla_pasos_pda
)
from ui.stack_widget import crear_widget_pila


def construir_panel_pda(page: ft.Page):
    """Devuelve el contenedor con todo el panel del PDA."""

    # ==================================================================
    # Estado interno del panel
    # ==================================================================
    estado = {
        "pda": None,
        "traza": [],
        "trazas_aceptadoras": [],
        "indice_paso": 0,
        "imagen_estado_actual": None,
    }

    # ==================================================================
    # Campos de definición
    # ==================================================================
    f_estados = campo_texto(
        "Estados (separados por comas)",
        "q0, q1, q2"
    )

    f_alfabeto_entrada = campo_texto(
        "Alfabeto de entrada Σ",
        "a, b"
    )

    f_alfabeto_pila = campo_texto(
        "Alfabeto de pila Γ",
        "A, Z"
    )

    f_inicial = campo_texto(
        "Estado inicial q₀",
        "q0"
    )

    f_simbolo_pila = campo_texto(
        "Símbolo inicial de pila Z₀",
        "Z"
    )

    f_finales = campo_texto(
        "Estados finales F (separados por comas)",
        "q2"
    )

    f_modo_aceptacion = ft.Dropdown(
        label="Modo de aceptación",
        options=[
            ft.dropdown.Option("estado_final", "Por estado final"),
            ft.dropdown.Option("pila_vacia", "Por pila vacía"),
        ],
        value="estado_final",
        border_color=COLORES["border"],
        focused_border_color=COLORES["primary"],
        bgcolor=COLORES["surface_alt"],
        label_style=ft.TextStyle(color=COLORES["text_dim"], size=12),
        text_style=ft.TextStyle(color=COLORES["text"], size=14)
    )

    f_transiciones = campo_texto(
        "Transiciones δ",
        (
            "Formato (una por línea o separadas por ;):\n"
            "  q0, a, Z -> q0, AZ\n"
            "  q0, a, A -> q0, AA\n"
            "  q0, b, A -> q1, ε\n"
            "  q1, b, A -> q1, ε\n"
            "  q1, λ, Z -> q2, Z"
        ),
        multilinea=True
    )

    f_cadena = campo_texto(
        "Cadena de entrada a simular",
        "aaabbb"
    )

    # ==================================================================
    # Salida visual
    # ==================================================================
    txt_resultado = ft.Text(
        "",
        size=14,
        color=COLORES["text"],
        selectable=True
    )

    # No creamos ft.Image() vacío porque en Flet 0.25+ `src` es obligatorio.
    # El Image se construye dentro de actualizar_imagen() con el path real.
    contenedor_imagen = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Genera o carga un PDA para ver el diagrama.",
                    color=COLORES["text_dim"],
                    italic=True
                )
            ],
            alignment="center",
            horizontal_alignment="center"
        ),
        bgcolor="#FAFAFA",
        border_radius=10,
        padding=12,
        border=ft.border.all(1, COLORES["border"]),
        alignment=ft.Alignment(0, 0),
        height=400
    )

    contenedor_pila = ft.Container(
        content=crear_widget_pila([])
    )

    txt_info_paso = ft.Text(
        "Sin simulación activa.",
        size=13,
        color=COLORES["text_dim"]
    )

    txt_paso_num = ft.Text(
        "Paso 0 / 0",
        size=13,
        weight="bold",
        color=COLORES["text_strong"]
    )

    badge_estado_actual = ft.Container(
        content=ft.Text("—", weight="bold", color="#FFFFFF"),
        bgcolor=COLORES["surface_alt"],
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20
    )

    cinta_entrada = ft.Row(controls=[], spacing=2)

    contenedor_tabla = ft.Container(
        content=ft.Text(
            "Aún sin traza.",
            color=COLORES["text_dim"]
        ),
        padding=8
    )

    badge_aceptacion = ft.Container(visible=False)

    # ==================================================================
    # FilePicker para cargar .jff
    # ==================================================================
    archivo_picker = ft.FilePicker()
    archivo_picker_guardar = ft.FilePicker()
    archivo_picker_guardar_json = ft.FilePicker()

    page.overlay.append(archivo_picker)
    page.overlay.append(archivo_picker_guardar)
    page.overlay.append(archivo_picker_guardar_json)

    # ==================================================================
    # Helpers
    # ==================================================================

    def mostrar(msg, color=None):
        txt_resultado.value = msg
        txt_resultado.color = color or COLORES["text"]
        page.update()

    def construir_pda_desde_campos():
        """Lee los campos y construye un objeto PDA."""

        estados_set = {
            e.strip()
            for e in f_estados.value.split(",")
            if e.strip()
        }
        alf_ent = {
            a.strip()
            for a in f_alfabeto_entrada.value.split(",")
            if a.strip()
        }
        alf_pila = {
            a.strip()
            for a in f_alfabeto_pila.value.split(",")
            if a.strip()
        }
        finales_set = {
            e.strip()
            for e in f_finales.value.split(",")
            if e.strip()
        }

        transiciones = parsear_transiciones_pda(
            f_transiciones.value or ""
        )

        pda = PDA(
            estados=estados_set,
            alfabeto_entrada=alf_ent,
            alfabeto_pila=alf_pila,
            inicial=(f_inicial.value or "").strip(),
            simbolo_inicial_pila=(
                (f_simbolo_pila.value or "").strip()
            ),
            finales=finales_set,
            transiciones=transiciones,
            modo_aceptacion=f_modo_aceptacion.value
        )

        return pda

    def renderizar_diagrama(estado_activo=None):
        if estado["pda"] is None:
            return
        try:
            ruta = generar_pda(
                estado["pda"],
                nombre_archivo="pda_diagram",
                estado_activo=estado_activo
            )
            # PNG como base64 — método universal que no depende
            # de paths ni de assets_dir, funciona en cualquier versión de Flet.
            import base64
            with open(ruta, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            nueva_img = ft.Image(
                src_base64=b64,
                width=720,
                height=380,
                fit="contain"
            )
            contenedor_imagen.content = nueva_img
            contenedor_imagen.update()
        except Exception as e:
            mostrar(
                f"Error al renderizar el diagrama: {e}",
                COLORES["error"]
            )

    def actualizar_cinta(leido, restante):
        """Cinta de entrada visual."""
        controles = []
        for c in leido:
            controles.append(
                ft.Container(
                    content=ft.Text(
                        c, size=14,
                        color="#000000",
                        weight="bold"
                    ),
                    bgcolor=COLORES["success"],
                    width=26, height=26,
                    alignment=ft.Alignment(0, 0),
                    border_radius=4
                )
            )
        for c in restante:
            controles.append(
                ft.Container(
                    content=ft.Text(
                        c, size=14,
                        color=COLORES["text"],
                        weight="bold"
                    ),
                    bgcolor=COLORES["surface_alt"],
                    width=26, height=26,
                    alignment=ft.Alignment(0, 0),
                    border_radius=4,
                    border=ft.border.all(1, COLORES["border"])
                )
            )
        if not controles:
            controles.append(
                ft.Text(
                    "(cadena vacía)",
                    color=COLORES["text_dim"],
                    italic=True
                )
            )
        cinta_entrada.controls = controles
        cinta_entrada.update()

    def aplicar_paso_actual():
        """Refresca toda la vista con el paso actual."""
        traza = estado["traza"]
        if not traza:
            return

        i = estado["indice_paso"]
        i = max(0, min(i, len(traza) - 1))
        estado["indice_paso"] = i

        paso = traza[i]

        # Pila
        contenedor_pila.content = crear_widget_pila(
            paso.get("pila", [])
        )
        contenedor_pila.update()

        # Cinta
        actualizar_cinta(
            paso.get("leido", ""),
            paso.get("restante", "")
        )

        # Texto info
        regla = paso.get("regla") or "—"
        accion = paso.get("accion") or ""
        txt_info_paso.value = (
            f"Acción: {accion}    |    {regla}"
        )
        txt_info_paso.update()

        # Número de paso
        txt_paso_num.value = (
            f"Paso {paso['paso']} / {traza[-1]['paso']}"
        )
        txt_paso_num.update()

        # Estado actual
        es_final = (
            estado["pda"] is not None and
            paso["estado"] in estado["pda"].finales
        )
        badge_estado_actual.content = ft.Text(
            paso["estado"],
            weight="bold",
            color="#000000" if es_final else "#FFFFFF"
        )
        badge_estado_actual.bgcolor = (
            COLORES["warning"] if es_final
            else COLORES["primary"]
        )
        badge_estado_actual.update()

        # Diagrama con estado resaltado
        renderizar_diagrama(estado_activo=paso["estado"])

    # ==================================================================
    # Handlers
    # ==================================================================

    def on_generar_diagrama(e):
        try:
            pda = construir_pda_desde_campos()
            errores = pda.validar_estructura()

            if errores:
                mostrar(
                    "Errores en la definición:\n• " +
                    "\n• ".join(errores),
                    COLORES["error"]
                )
                return

            estado["pda"] = pda
            renderizar_diagrama()
            mostrar(
                f"Diagrama generado. |Q|={len(pda.estados)}, "
                f"|Σ|={len(pda.alfabeto_entrada)}, "
                f"|Γ|={len(pda.alfabeto_pila)}, "
                f"|δ|={sum(len(v) for v in pda.transiciones.values())}",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_simular(e):
        try:
            pda = construir_pda_desde_campos()
            errores = pda.validar_estructura()

            if errores:
                mostrar(
                    "Errores en la definición:\n• " +
                    "\n• ".join(errores),
                    COLORES["error"]
                )
                return

            estado["pda"] = pda

            cadena = f_cadena.value or ""
            aceptada, traza, todas = pda.simular(cadena)

            estado["traza"] = traza
            estado["trazas_aceptadoras"] = todas
            estado["indice_paso"] = 0

            # Tabla con la traza
            contenedor_tabla.content = ft.Column(
                controls=[tabla_pasos_pda(traza)],
                scroll="auto",
                height=260
            )
            contenedor_tabla.update()

            # Badge de resultado
            badge_aceptacion.visible = True
            if aceptada:
                badge_aceptacion.content = ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CHECK_CIRCLE,
                            color="#FFFFFF",
                            size=18
                        ),
                        ft.Text(
                            f"CADENA ACEPTADA  ({len(todas)} "
                            f"camino{'s' if len(todas) != 1 else ''} "
                            f"de aceptación)",
                            weight="bold",
                            color="#FFFFFF"
                        )
                    ],
                    spacing=8,
                    vertical_alignment="center"
                )
                badge_aceptacion.bgcolor = COLORES["success"]
            else:
                badge_aceptacion.content = ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.CANCEL,
                            color="#FFFFFF",
                            size=18
                        ),
                        ft.Text(
                            "CADENA RECHAZADA "
                            "(ningún camino acepta)",
                            weight="bold",
                            color="#FFFFFF"
                        )
                    ],
                    spacing=8,
                    vertical_alignment="center"
                )
                badge_aceptacion.bgcolor = COLORES["error"]
            badge_aceptacion.padding = ft.padding.symmetric(
                horizontal=14, vertical=8
            )
            badge_aceptacion.border_radius = 8
            badge_aceptacion.update()

            aplicar_paso_actual()

            mostrar(
                f"Simulación completada. "
                f"Pasos en la traza: {len(traza)}",
                COLORES["info"]
            )
        except Exception as ex:
            mostrar(f"Error: {ex}", COLORES["error"])

    def on_siguiente_paso(e):
        if not estado["traza"]:
            return
        if estado["indice_paso"] < len(estado["traza"]) - 1:
            estado["indice_paso"] += 1
            aplicar_paso_actual()

    def on_paso_previo(e):
        if not estado["traza"]:
            return
        if estado["indice_paso"] > 0:
            estado["indice_paso"] -= 1
            aplicar_paso_actual()

    def on_primer_paso(e):
        if not estado["traza"]:
            return
        estado["indice_paso"] = 0
        aplicar_paso_actual()

    def on_ultimo_paso(e):
        if not estado["traza"]:
            return
        estado["indice_paso"] = len(estado["traza"]) - 1
        aplicar_paso_actual()

    def on_cargar_jff_resultado(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        ruta = e.files[0].path
        try:
            datos = leer_jff_pda(ruta)

            f_estados.value = ", ".join(sorted(datos["estados"]))
            f_alfabeto_entrada.value = ", ".join(
                sorted(datos["alfabeto_entrada"])
            )
            f_alfabeto_pila.value = ", ".join(
                sorted(datos["alfabeto_pila"])
            )
            f_inicial.value = datos["inicial"] or ""
            f_simbolo_pila.value = datos["simbolo_inicial_pila"]
            f_finales.value = ", ".join(sorted(datos["finales"]))
            f_transiciones.value = serializar_transiciones_pda(
                datos["transiciones"]
            )

            for w in [
                f_estados, f_alfabeto_entrada, f_alfabeto_pila,
                f_inicial, f_simbolo_pila, f_finales,
                f_transiciones
            ]:
                w.update()

            mostrar(
                f"PDA cargado desde:\n{os.path.basename(ruta)}",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(
                f"Error al leer .jff: {ex}",
                COLORES["error"]
            )

    archivo_picker.on_result = on_cargar_jff_resultado

    def on_guardar_jff_resultado(e: ft.FilePickerResultEvent):
        if not e.path:
            return
        ruta = e.path
        if not ruta.endswith(".jff"):
            ruta += ".jff"
        try:
            pda = construir_pda_desde_campos()
            escribir_jff_pda(ruta, pda)
            mostrar(
                f"PDA guardado en:\n{ruta}",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error al guardar: {ex}", COLORES["error"])

    archivo_picker_guardar.on_result = on_guardar_jff_resultado

    def on_guardar_json_resultado(e: ft.FilePickerResultEvent):
        if not e.path:
            return
        ruta = e.path
        if not ruta.endswith(".json"):
            ruta += ".json"
        try:
            pda = construir_pda_desde_campos()
            escribir_json_pda(ruta, pda)
            mostrar(
                f"PDA guardado en:\n{ruta}",
                COLORES["success"]
            )
        except Exception as ex:
            mostrar(f"Error al guardar: {ex}", COLORES["error"])

    archivo_picker_guardar_json.on_result = (
        on_guardar_json_resultado
    )

    def on_btn_cargar(e):
        archivo_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jff", "xml"]
        )

    def on_btn_guardar_jff(e):
        archivo_picker_guardar.save_file(
            file_name="mi_pda.jff",
            allowed_extensions=["jff"]
        )

    def on_btn_guardar_json(e):
        archivo_picker_guardar_json.save_file(
            file_name="mi_pda.json",
            allowed_extensions=["json"]
        )

    # --------- Ejemplos predefinidos ----------

    def cargar_ejemplo_anbn(e):
        f_estados.value = "q0, q1, q2"
        f_alfabeto_entrada.value = "a, b"
        f_alfabeto_pila.value = "A, Z"
        f_inicial.value = "q0"
        f_simbolo_pila.value = "Z"
        f_finales.value = "q2"
        f_transiciones.value = (
            "q0, a, Z -> q0, AZ\n"
            "q0, a, A -> q0, AA\n"
            "q0, b, A -> q1, ε\n"
            "q1, b, A -> q1, ε\n"
            "q1, λ, Z -> q2, Z"
        )
        f_cadena.value = "aaabbb"
        for w in [
            f_estados, f_alfabeto_entrada, f_alfabeto_pila,
            f_inicial, f_simbolo_pila, f_finales,
            f_transiciones, f_cadena
        ]:
            w.update()
        mostrar(
            "Ejemplo cargado: L = {aⁿbⁿ | n ≥ 1}",
            COLORES["info"]
        )

    def cargar_ejemplo_balanceados(e):
        f_estados.value = "q0, q1"
        f_alfabeto_entrada.value = "(, )"
        f_alfabeto_pila.value = "P, Z"
        f_inicial.value = "q0"
        f_simbolo_pila.value = "Z"
        f_finales.value = "q1"
        f_transiciones.value = (
            "q0, (, Z -> q0, PZ\n"
            "q0, (, P -> q0, PP\n"
            "q0, ), P -> q0, ε\n"
            "q0, λ, Z -> q1, Z"
        )
        f_cadena.value = "(())"
        for w in [
            f_estados, f_alfabeto_entrada, f_alfabeto_pila,
            f_inicial, f_simbolo_pila, f_finales,
            f_transiciones, f_cadena
        ]:
            w.update()
        mostrar(
            "Ejemplo cargado: paréntesis balanceados",
            COLORES["info"]
        )

    def cargar_ejemplo_palindromo(e):
        # wcwR sobre {a,b}, con marcador c
        f_estados.value = "q0, q1, q2"
        f_alfabeto_entrada.value = "a, b, c"
        f_alfabeto_pila.value = "A, B, Z"
        f_inicial.value = "q0"
        f_simbolo_pila.value = "Z"
        f_finales.value = "q2"
        f_transiciones.value = (
            "q0, a, Z -> q0, AZ\n"
            "q0, a, A -> q0, AA\n"
            "q0, a, B -> q0, AB\n"
            "q0, b, Z -> q0, BZ\n"
            "q0, b, A -> q0, BA\n"
            "q0, b, B -> q0, BB\n"
            "q0, c, Z -> q1, Z\n"
            "q0, c, A -> q1, A\n"
            "q0, c, B -> q1, B\n"
            "q1, a, A -> q1, ε\n"
            "q1, b, B -> q1, ε\n"
            "q1, λ, Z -> q2, Z"
        )
        f_cadena.value = "abacaba"
        for w in [
            f_estados, f_alfabeto_entrada, f_alfabeto_pila,
            f_inicial, f_simbolo_pila, f_finales,
            f_transiciones, f_cadena
        ]:
            w.update()
        mostrar(
            "Ejemplo cargado: L = {wcwᴿ | w ∈ {a,b}*}",
            COLORES["info"]
        )

    def on_limpiar(e):
        f_estados.value = ""
        f_alfabeto_entrada.value = ""
        f_alfabeto_pila.value = ""
        f_inicial.value = ""
        f_simbolo_pila.value = ""
        f_finales.value = ""
        f_transiciones.value = ""
        f_cadena.value = ""

        estado["pda"] = None
        estado["traza"] = []
        estado["indice_paso"] = 0

        contenedor_pila.content = crear_widget_pila([])
        contenedor_tabla.content = ft.Text(
            "Aún sin traza.",
            color=COLORES["text_dim"]
        )
        contenedor_imagen.content = ft.Text(
            "Genera o carga un PDA para ver el diagrama.",
            color=COLORES["text_dim"],
            italic=True
        )
        badge_aceptacion.visible = False
        cinta_entrada.controls = []
        txt_info_paso.value = "Sin simulación activa."
        txt_paso_num.value = "Paso 0 / 0"
        badge_estado_actual.content = ft.Text(
            "—", weight="bold", color="#FFFFFF"
        )
        badge_estado_actual.bgcolor = COLORES["surface_alt"]

        for w in [
            f_estados, f_alfabeto_entrada, f_alfabeto_pila,
            f_inicial, f_simbolo_pila, f_finales,
            f_transiciones, f_cadena
        ]:
            w.update()

        page.update()
        mostrar("Formulario limpiado.", COLORES["info"])

    # ==================================================================
    # Layout
    # ==================================================================

    # --- columna izquierda (definición) ---
    col_definicion = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "DEFINICIÓN DEL PDA",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Text(
                    "M = (Q, Σ, Γ, δ, q₀, Z₀, F)",
                    italic=True,
                    color=COLORES["text_dim"],
                    size=12
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                f_estados,
                f_alfabeto_entrada,
                f_alfabeto_pila,
                ft.Row(
                    controls=[
                        ft.Container(f_inicial, expand=True),
                        ft.Container(f_simbolo_pila, expand=True),
                    ],
                    spacing=10
                ),
                f_finales,
                f_modo_aceptacion,
                f_transiciones,
                ft.Row(
                    controls=[
                        boton_primario(
                            "Generar diagrama",
                            on_generar_diagrama,
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
                ft.Row(
                    controls=[
                        boton_secundario(
                            "Guardar .jff",
                            on_btn_guardar_jff,
                            icono=ft.Icons.SAVE
                        ),
                        boton_secundario(
                            "Guardar .json",
                            on_btn_guardar_json,
                            icono=ft.Icons.DATA_OBJECT
                        )
                    ],
                    spacing=8,
                    wrap=True
                ),
                ft.Divider(height=1, color=COLORES["border"]),
                ft.Text(
                    "Ejemplos rápidos",
                    weight="bold",
                    color=COLORES["text_strong"],
                    size=13
                ),
                ft.Row(
                    controls=[
                        boton_secundario(
                            "aⁿbⁿ",
                            cargar_ejemplo_anbn
                        ),
                        boton_secundario(
                            "Paréntesis",
                            cargar_ejemplo_balanceados
                        ),
                        boton_secundario(
                            "wcwᴿ",
                            cargar_ejemplo_palindromo
                        ),
                    ],
                    spacing=8,
                    wrap=True
                ),
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

    # --- columna derecha (visualización + simulación) ---
    controles_paso = ft.Row(
        controls=[
            boton_secundario(
                "⏮  Inicio",
                on_primer_paso
            ),
            boton_secundario(
                "◀  Anterior",
                on_paso_previo
            ),
            boton_primario(
                "Siguiente  ▶",
                on_siguiente_paso
            ),
            boton_secundario(
                "Final  ⏭",
                on_ultimo_paso
            ),
        ],
        spacing=8,
        wrap=True
    )

    fila_simulacion = ft.Row(
        controls=[
            f_cadena,
            boton_primario(
                "Simular",
                on_simular,
                icono=ft.Icons.PLAY_ARROW,
                ancho=140
            )
        ],
        spacing=10,
        vertical_alignment="end"
    )

    col_visualizacion = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "VISUALIZACIÓN Y SIMULACIÓN",
                    size=TAMS["subtitulo"],
                    weight="bold",
                    color=COLORES["text_strong"]
                ),
                ft.Divider(height=1, color=COLORES["border"]),

                # Diagrama
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Diagrama del PDA",
                                        weight="bold",
                                        color=COLORES["text_strong"],
                                        size=14
                                    ),
                                    contenedor_imagen
                                ],
                                spacing=8
                            ),
                            expand=True
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Pila",
                                        weight="bold",
                                        color=COLORES["text_strong"],
                                        size=14
                                    ),
                                    contenedor_pila
                                ],
                                spacing=8,
                                horizontal_alignment="center"
                            ),
                            width=150
                        )
                    ],
                    spacing=12,
                    vertical_alignment="start"
                ),

                ft.Divider(height=1, color=COLORES["border"]),

                # Entrada y simulación
                fila_simulacion,

                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Cinta de entrada",
                                weight="bold",
                                size=12,
                                color=COLORES["text_dim"]
                            ),
                            ft.Container(
                                content=cinta_entrada,
                                bgcolor=COLORES["bg"],
                                padding=8,
                                border_radius=6
                            )
                        ],
                        spacing=4
                    )
                ),

                # Estado actual + número de paso
                ft.Row(
                    controls=[
                        ft.Text(
                            "Estado actual:",
                            color=COLORES["text_dim"],
                            size=13
                        ),
                        badge_estado_actual,
                        ft.Container(width=20),
                        txt_paso_num
                    ],
                    spacing=10,
                    vertical_alignment="center"
                ),
                txt_info_paso,

                # Controles paso a paso
                controles_paso,

                badge_aceptacion,

                ft.Divider(height=1, color=COLORES["border"]),

                ft.Text(
                    "Traza de ejecución",
                    weight="bold",
                    color=COLORES["text_strong"],
                    size=14
                ),
                ft.Container(
                    content=contenedor_tabla,
                    bgcolor=COLORES["surface"],
                    border_radius=8,
                    padding=8,
                    border=ft.border.all(
                        1, COLORES["border"]
                    )
                ),

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
        controls=[col_definicion, col_visualizacion],
        spacing=12,
        expand=True
    )
