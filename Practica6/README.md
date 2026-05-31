# Simulador de Autómatas — v2.0 (Práctica 6 · PDA)

**Instituto Politécnico Nacional · ESCOM**
**Teoría de la Computación · Grupo 4CM4**
**Alumno: HERNÁNDEZ RÍOS CRISTIAN SEBASTIÁN**

Aplicación de escritorio en Python + Flet que permite **construir, visualizar
y simular autómatas** de cuatro tipos:

- **AFD** — Autómata Finito Determinista
- **AFND** — Autómata Finito No Determinista
- **AFND-λ** — AFND con transiciones lambda
- **PDA** — Autómata de Pila (Pushdown Automaton)

Además incluye operaciones sobre lenguajes formales, conversión entre tipos,
minimización, traducción AFD → Expresión Regular y un panel de validadores
regex de uso cotidiano.

> Esta versión es un **remaster completo** del software entregado en las
> prácticas 1–5. Se rediseñó la interfaz, se corrigieron varios bugs y se
> añadió el módulo de **Autómatas de Pila** para cumplir con el Ejercicio 2
> de la Práctica 6.

---

## Vista general

| Módulo | Qué hace |
|---|---|
| **Autómatas Finitos** | Carga `.jff` (JFLAP) o JSON, define manualmente AFD/AFND/AFND-λ, simula cadenas paso a paso, convierte AFND → AFD, elimina λ-transiciones, minimiza un AFD y traduce AFD → ER. |
| **Autómatas de Pila** | Define un PDA, lo carga desde `.jff` JFLAP, lo simula paso a paso mostrando **estado actual** y **configuración completa de la pila** en cada transición, con cinta de entrada visible y traza tabular. |
| **Lenguajes y Regex** | Operaciones sobre cadenas (subcadenas, prefijos, sufijos), operaciones sobre lenguajes (unión, intersección, diferencia, concatenación, potencia, Kleene, reflexión) y validadores regex (email, teléfono, password, URL, fecha). |

---

## Requisitos del sistema

### 1. Python 3.10 o superior

Verifica con:

```bash
python --version
```

Si necesitas instalarlo: <https://www.python.org/downloads/>
(en Windows marca la casilla **"Add Python to PATH"** durante la instalación).

### 2. Graphviz instalado en el sistema operativo

El paquete `graphviz` de pip es solo el wrapper de Python. Para generar las
imágenes de los autómatas se necesita el ejecutable `dot` instalado a nivel
de sistema.

**Windows** — Descarga el instalador desde <https://graphviz.org/download/>
y marca la opción "Add Graphviz to the system PATH" durante la instalación.

**macOS:**
```bash
brew install graphviz
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install graphviz
```

**Verifica la instalación:**
```bash
dot -V
```
Debe mostrar algo como `dot - graphviz version 9.x`.

---

## Instalación

```bash
# 1) Clona o descarga el repositorio
git clone <url-de-tu-repo>
cd Simulador_Automatas

# 2) (Recomendado) Crea un entorno virtual
python -m venv venv

# Actívalo:
#   Windows:   venv\Scripts\activate
#   Mac/Linux: source venv/bin/activate

# 3) Instala las dependencias
pip install -r requirements.txt
```

---

## Cómo ejecutar

Desde la raíz del proyecto, con el entorno virtual activado:

```bash
python main.py
```

Se abrirá una ventana de escritorio de 1520×940 px con la interfaz de
navegación lateral.

---

## Estructura del proyecto

```
Simulador_Automatas/
├── main.py                 # Punto de entrada · navegación principal
├── requirements.txt
├── README.md
├── .gitignore
├── assets/                 # Imágenes generadas en tiempo de ejecución
├── automatas/              # Núcleo de los autómatas
│   ├── afd.py
│   ├── afnd.py
│   ├── afnd_lambda.py
│   ├── pda.py              # ← Nuevo · Autómata de Pila
│   ├── conversion.py       # AFND → AFD, eliminar λ
│   ├── minimizacion.py     # Algoritmo de clases de equivalencia
│   ├── afd_to_er.py        # AFD → Expresión Regular
│   └── simulador_visual.py # Recorrido paso a paso con resaltado
├── utils/                  # Utilidades de I/O y renderizado
│   ├── jff_reader.py       # Lectura de archivos JFLAP (.jff)
│   ├── jff_writer.py       # Escritura .jff y .json
│   ├── renderizador.py     # Graphviz para AF y PDA
│   ├── json_manager.py
│   ├── parser_pda.py       # Parser textual de transiciones PDA
│   └── validators.py
├── extras/
│   ├── operaciones.py      # Operaciones de cadenas/lenguajes
│   └── validadores.py      # Regexes predefinidos
├── ui/                     # Interfaz Flet
│   ├── tema.py             # Paleta y dimensiones
│   ├── components.py       # Componentes reutilizables
│   ├── stack_widget.py     # Visualizador vertical de la pila
│   ├── pda_panel.py        # Panel del módulo PDA
│   ├── af_panel.py         # Panel de AFD/AFND/AFND-λ
│   └── extras_panel.py
└── ejemplos/               # Archivos .jff de ejemplo
    ├── pda_anbn.jff        # L = { aⁿbⁿ | n ≥ 1 }
    ├── pda_balanceados.jff # paréntesis balanceados
    └── pda_wcwR.jff        # L = { wcwᴿ | w ∈ {a,b}* }
```

---

## Módulo de Autómatas de Pila (Práctica 6)

### Definición formal

Un **PDA** es una 7-tupla `M = (Q, Σ, Γ, δ, q₀, Z₀, F)` donde:

| | |
|---|---|
| `Q`  | conjunto finito de estados |
| `Σ`  | alfabeto de entrada |
| `Γ`  | alfabeto de la pila |
| `δ`  | función de transición `Q × (Σ ∪ {λ}) × Γ → 𝒫(Q × Γ*)` |
| `q₀` | estado inicial |
| `Z₀` | símbolo inicial de la pila |
| `F`  | conjunto de estados finales |

### Formato de transiciones

En el panel "Autómatas de Pila", las transiciones se escriben como:

```
estado_origen, símbolo_entrada, símbolo_pila -> estado_destino, cadena_a_apilar
```

Reglas:

- Separa varias transiciones con `;` o con saltos de línea.
- Para una **transición λ** (no consume entrada) usa `λ`, `lambda` o `\`.
- Para **solo desapilar** (no apila nada) deja la cadena después de `->` vacía, o escribe `ε`/`epsilon`.
- El **carácter más a la izquierda** de la cadena a apilar queda en el **tope** de la pila.

**Ejemplo (L = aⁿbⁿ):**

```
q0, a, Z -> q0, AZ
q0, a, A -> q0, AA
q0, b, A -> q1, ε
q1, b, A -> q1, ε
q1, λ, Z -> q2, Z
```

### Visualización durante la simulación

Mientras la simulación avanza paso a paso, el panel muestra:

1. **Diagrama del PDA** con el estado actual resaltado en amarillo.
2. **Pila** en una columna vertical lateral (tope arriba, en color naranja).
3. **Cinta de entrada** con el carácter actual resaltado.
4. **Tabla de traza** con: paso, estado, símbolo leído, restante, contenido de la pila, acción y regla aplicada.
5. Controles `⏮ ◀ ▶ ⏭` para navegar pasos.

### Archivos `.jff` de ejemplo incluidos

| Archivo | Lenguaje | Cadenas que acepta | Cadenas que rechaza |
|---|---|---|---|
| `pda_anbn.jff` | `{ aⁿbⁿ \| n ≥ 1 }` | `ab`, `aabb`, `aaabbb`, `aaaabbbb` | `aab`, `abb`, `abab`, `aabbb` |
| `pda_balanceados.jff` | paréntesis balanceados | `()`, `(())`, `()()`, `((()))`, `(()(()))`, cadena vacía | `(`, `())`, `(()` |
| `pda_wcwR.jff` | `{ wcwᴿ \| w ∈ {a,b}* }` | `c`, `aca`, `bcb`, `abcba`, `aabcbaa` | `ab`, `abcab`, `abccba` |

Todos abren correctamente tanto en este simulador como en **JFLAP**, y
están en `ejemplos/`.

---

## Flujo típico de uso

### Para autómatas finitos

1. Abre **Autómatas Finitos** en la barra lateral.
2. Pulsa **Cargar .jff** y selecciona el archivo (o escribe la definición a mano).
3. El tipo se detecta automáticamente. Pulsa **Generar diagrama**.
4. Escribe una cadena y pulsa **Simular** para validarla con traza paso a paso.
5. Usa los botones de la barra de acciones para minimizar, convertir o traducir a ER.

### Para autómatas de pila

1. Abre **Autómatas de Pila**.
2. Carga un `.jff` o pulsa uno de los 3 botones de ejemplo (aⁿbⁿ, balanceados, wcwᴿ).
3. Pulsa **Construir** para validar la definición y dibujar el diagrama.
4. Escribe una cadena y pulsa **Simular**.
5. Usa `⏮ ◀ ▶ ⏭` para avanzar paso a paso viendo cómo cambia la pila.

---

## Cambios respecto a la versión 1 (prácticas 1–5)

- 🆕 **Módulo PDA completo** con simulación visual de la pila.
- 🎨 **Tema oscuro** rediseñado con paleta indigo/púrpura/cian.
- 🧭 Navegación con `NavigationRail` en lugar del sidebar manual.
- 📁 **FilePicker nativo** de Flet para cargar/guardar archivos.
- 💾 Soporte de **guardar** autómatas como `.jff` o `.json`.
- 🐞 Corregidos los bugs de la versión anterior:
  - `simulador_visual.py` accedía a `estado_inicial` y `estados_finales` que no existían en `AFD`.
  - `afd_a_er` tenía firma incompatible con la llamada en `main.py`.
  - `validadores.py` devolvía una tupla `(bool, patrón, mensaje)` pero `main.py` la trataba como booleano.

---

## Notas para desarrolladores

- El proyecto **no requiere base de datos** ni servidor: es 100 % local.
- Las imágenes de los diagramas se generan en `assets/` y se sobrescriben cada vez.
- El motor del PDA usa **búsqueda en anchura (BFS)** sobre el espacio de configuraciones para manejar el no determinismo correctamente. Tiene un tope de `max_pasos=2000` para evitar loops infinitos en autómatas mal diseñados.
- La representación interna de la pila es una **tupla con el tope en el índice 0**.

---

## Créditos

- **Alumno:** HERNÁNDEZ RÍOS CRISTIAN SEBASTIÁN
- **Grupo:** 4CM4
- **Profesor:** Equipo de Teoría de la Computación · ESCOM IPN
- **Período:** 2026-2

Software desarrollado como entregable de las prácticas de la unidad de
aprendizaje **Teoría de la Computación**.
