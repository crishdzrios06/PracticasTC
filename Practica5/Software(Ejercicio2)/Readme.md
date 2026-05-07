# Simulador de Autómatas Finitos y Expresiones Regulares

**Escuela Superior de Computación (ESCOM)** **Instituto Politécnico Nacional (IPN)**

---

## 1. Información General

* **Institución:** Instituto Politécnico Nacional (IPN)
* **Unidad Académica:** Escuela Superior de Cómputo (ESCOM)
* **Materia:** Teoría de la Computación
* **Grupo:** 4CM4
* **Alumno:** Hernández Ríos Cristian Sebastian
* **Práctica 5:** Uso de la Herramienta JFLAP para Transformar una Gramática a la Forma Normal de Chomsky y Extensión de Software Interactivo para Visualizar Autómatas

---

## 2. Descripción del Proyecto

Este software es una herramienta académica diseñada para el diseño, simulación y transformación de modelos computacionales basados en la jerarquía de Chomsky, específicamente Autómatas Finitos (DFA, NFA, NFA-ε) y Expresiones Regulares (RE). La aplicación permite la manipulación de grafos, la validación de cadenas y la aplicación de algoritmos de optimización de estados.

### Características Principales:
* **Diseño de Autómatas:** Interfaz para definir quintuplas $Q, \Sigma, \delta, q_0, F$.
* **Conversiones:** Implementación del algoritmo de subconjuntos y eliminación de estados.
* **Minimización:** Reducción de estados mediante el algoritmo de Myhill-Nerode.
* **Simulación:** Trazado paso a paso del procesamiento de cadenas.

---

## 3. Arquitectura del Proyecto

El software está diseñado bajo un paradigma modular y una arquitectura de capas que separa la lógica matemática de la computación de la capa de presentación visual. Esta organización garantiza la escalabilidad del sistema, facilita la depuración de los algoritmos de transición y permite un mantenimiento eficiente del código fuente.

### 3.1 Estructura de Directorios

La organización jerárquica del código se detalla a continuación:
```text
Practica5/
└── Software(Ejercicio2)/
    ├── automatas/       # Núcleo lógico: Clases para AFD, AFND y AFND-λ
    ├── ui/              # Capa de presentación: Vistas y componentes de Flet
    ├── utils/           # Herramientas de soporte: Manejo de archivos y JFLAP
    ├── assets/          # Recursos gráficos: Iconos y diagramas generados
    ├── extras/          # Módulos complementarios y extensiones
    ├── main.py          # Punto de entrada y orquestador del programa
    ├── requirements.txt # Registro de dependencias del proyecto
    └── venv/            # Entorno virtual de Python (aislamiento de librerías)
 ```
### 3.2 Descripción de Módulos

El proyecto se divide en componentes especializados para garantizar una separación de responsabilidades clara y un mantenimiento eficiente:

*   **`automatas/`**: Es el núcleo lógico del software. Contiene las implementaciones matemáticas de las quintuplas $Q, \Sigma, \delta, q_0, F$. En este módulo se ejecutan los algoritmos de clausura-$\lambda$, la construcción de subconjuntos para la determinización y el algoritmo de Myhill-Nerode para la minimización de estados.
*   **`ui/`**: Define la capa de presentación. Desarrollada con el framework **Flet**, esta carpeta contiene los archivos que gestionan la ventana principal, los formularios de entrada de datos, los botones de control y la visualización interactiva de resultados.
*   **`utils/`**: Provee herramientas auxiliares para el sistema. Incluye los motores de validación para expresiones regulares (regex), así como los adaptadores encargados de convertir la lógica del autómata en archivos de imagen mediante **pydot**.
*   **`extras/`**: Espacio dedicado a funciones complementarias, como generadores de reportes, utilidades de exportación o extensiones de algoritmos menos frecuentes.
*   **`main.py`**: Es el orquestador principal. Su función es inicializar la aplicación, configurar el entorno de Flet y enlazar las interacciones del usuario con los algoritmos del núcleo lógico.

---

### 3.3 Flujo de Datos del Sistema

El procesamiento de la información dentro del simulador sigue un flujo estructurado para garantizar la integridad de los resultados:

1.  **Captura de Parámetros:** El usuario ingresa los componentes del autómata (alfabeto, estados, transiciones) o carga un archivo externo `.jff` (JFLAP).
2.  **Validación Lógica:** El sistema comprueba que la estructura definida cumpla con los requisitos teóricos del tipo de autómata seleccionado (por ejemplo, que un AFD no tenga transiciones múltiples para el mismo símbolo).
3.  **Ejecución Algorítmica:** Dependiendo de la acción solicitada (Minimizar, Convertir, Eliminar $\lambda$), el software transforma la estructura de datos interna preservando la equivalencia del lenguaje.
4.  **Generación de Diagrama:** Los datos del autómata se traducen al lenguaje de descripción de grafos DOT. **Graphviz** procesa este archivo para generar un renderizado visual (PNG/SVG) que se muestra en la interfaz.
5.  **Simulación de Cadenas:** El usuario ingresa una cadena; el motor de simulación recorre el autómata y devuelve un veredicto de "Aceptada" o "Rechazada", detallando el camino de estados recorrido.

---

## 4. Objetivos del Proyecto

### Objetivo General
Desarrollar una herramienta integral de software que permita la manipulación, conversión y simulación de modelos de computación formal, facilitando el aprendizaje y la experimentación con Autómatas Finitos y Expresiones Regulares.

### Objetivos Específicos
* Implementar algoritmos de conversión entre AFND, AFND-λ y AFD.
* Proveer un motor de minimización de estados basado en el algoritmo de particiones.
* Permitir la visualización gráfica dinámica de los grafos de estados mediante Graphviz.
* Validar la equivalencia entre Expresiones Regulares y Autómatas Finitos.
* Facilitar la interoperabilidad mediante la importación de archivos JFLAP.

---

## 5. Tecnologías Utilizadas

| Tecnología | Propósito |
| :--- | :--- |
| **Python 3.11** | Lenguaje de programación base. |
| **Flet** | Framework para la interfaz gráfica de usuario (GUI) interactiva. |
| **Graphviz** | Motor de renderizado para la visualización de grafos. |
| **visual-automata** | Generación de visualizaciones de transiciones de autómatas. |
| **automata-lib** | Biblioteca de manipulación de estructuras de autómatas. |
| **pydot** | Interfaz de Python para el lenguaje Graphviz DOT. |

---

## 6. Estructura de Directorios

El proyecto se organiza de forma modular para separar la lógica de negocio de la capa de presentación:

* **`automatas/`**: Contiene las clases principales que gestionan la lógica de los AFD, AFND y AFND-λ.
* **`ui/`**: Archivos relacionados con la interfaz gráfica desarrollada en Flet.
* **`utils/`**: Scripts auxiliares para la gestión de archivos y exportación de datos.
* **`extras/`**: Módulos adicionales para funcionalidades secundarias.
* **`assets/`**: Recursos estáticos como iconos, imágenes y logotipos institucionales.
* **`venv/`**: Entorno virtual que contiene las dependencias aisladas del proyecto.
* **`main.py`**: Punto de entrada principal para la ejecución de la aplicación.
* **`requirements.txt`**: Listado de dependencias necesarias para la instalación.

---

## 7. Requisitos Previos

Antes de proceder con la instalación, asegúrese de contar con los siguientes elementos en su sistema:
* **Sistema Operativo:** Windows 10/11, macOS o Distribuciones Linux (Ubuntu 20.04+ recomendado).
* **Python:** Versión 3.11 o superior.
* **Graphviz:** El binario del sistema debe estar instalado independientemente de las librerías de Python.
* **Espacio en disco:** Mínimo 500 MB para entorno y dependencias.

---

## 8. Instalación de Python y Graphviz

Para el correcto funcionamiento del simulador, es imperativo contar con el intérprete de lenguaje y el motor de renderizado de grafos instalados y configurados en las variables de entorno del sistema.

### 8.1 Instalación de Python 3.11
1. Acceda al sitio oficial [python.org](https://www.python.org/downloads/).
2. Descargue la versión estable para su sistema operativo (mínimo 3.11).
3. Al ejecutar el instalador, **debe marcar obligatoriamente** la casilla **"Add Python to PATH"**.
4. Finalice la instalación y reinicie su terminal.

### 8.2 Instalación de Graphviz (Motor de Grafos)
El software utiliza Graphviz para generar las imágenes de los autómatas. No basta con la librería de Python; el binario del sistema es necesario:
*   **Windows:** Descargue el instalador `.exe` desde [Graphviz Download](https://graphviz.org/download/). Durante la instalación, seleccione la opción "Add Graphviz to the system PATH for all users".
*   **macOS (Homebrew):** `brew install graphviz`
*   **Linux (Ubuntu/Debian):** `sudo apt update && sudo apt install graphviz`

### 8.3 Verificación de Instalaciones
Abra una terminal (CMD, PowerShell o Bash) y ejecute los siguientes comandos para confirmar que el sistema reconoce las herramientas:
```bash
# Verificación de Python
python --version

# Verificación de Gestor de Paquetes
pip --version

# Verificación de Motor Graphviz
dot -V

---

## 9. Configuración y Ejecución del Sistema

Para garantizar que el software funcione correctamente con todas sus dependencias aisladas, siga estrictamente el proceso de configuración del entorno virtual y ejecución detallado a continuación.

### 9.1 Preparación del Entorno Virtual (venv)
El uso de un entorno virtual evita conflictos entre las librerías del proyecto y otras versiones instaladas en su sistema.

1.  Abra una terminal o consola de comandos.
2.  Navegue hasta la ruta raíz del software:
    
```bash
    cd Practica5/Software(Ejercicio2)/
    ```
3.  Cree el entorno virtual ejecutando:
    ```bash
    python -m venv venv
    ```

### 9.2 Activación del Entorno
Debe activar el entorno cada vez que desee ejecutar el programa:

*   **En Windows (PowerShell/CMD):**
    ```bash
    .\venv\Scripts\activate
    ```
*   **En Linux o macOS:**
    ```bash
    source venv/bin/activate
    ```

### 9.3 Instalación de Dependencias
Una vez activado el entorno (verá el texto `(venv)` al inicio de su línea de comandos), instale los paquetes requeridos:
```bash
pip install --upgrade pip
pip install -r requirements.txt

## 10. Funcionalidades Detalladas

El simulador integra algoritmos avanzados de la Teoría de la Computación, permitiendo las siguientes operaciones:

### 10.1 Simulación de Cadenas
El motor de simulación permite el procesamiento de cadenas de entrada, mostrando el recorrido a través de los estados.
* **Paso a paso:** Visualización del estado actual y la transición activada por cada símbolo.
* **Validación en lote:** Procesamiento de múltiples cadenas para determinar su pertenencia al lenguaje.

### 10.2 Conversión de Autómatas
El software implementa los algoritmos estándar de transformación:
* **Eliminación de transiciones λ:** Algoritmo de clausura para simplificar AFND-λ a AFND.
* **Subconjuntos (NFA a DFA):** Construcción del conjunto potencia para obtener un autómata determinista equivalente.
* **Conversión a Expresiones Regulares:** Método de eliminación de estados para obtener la ER asociada a un DFA.

### 10.3 Minimización de DFA
Utiliza el algoritmo de **Myhill-Nerode** para identificar estados equivalentes y reducir el autómata a su forma mínima, garantizando la eficiencia en el procesamiento.

### 10.4 Visualización de Grafos
Integración directa con el lenguaje DOT de Graphviz para generar diagramas de alta calidad:
* Nodos con doble círculo para estados de aceptación.
* Flechas dirigidas etiquetadas con los símbolos del alfabeto.
* Nodo de entrada con flecha de inicio.

---

## 11. Ejemplos de Configuración y Ejecución

### Ejemplo de Tabla de Transiciones (AFD)
Representación interna para un autómata que reconoce el lenguaje $L = \{w \mid w \text{ contiene la subcadena } 01\}$:

| Estado Actual | Símbolo (0) | Símbolo (1) | ¿Es Final? |
| :--- | :--- | :--- | :--- |
| **q0** (Inicio) | q1 | q0 | No |
| **q1** | q1 | q2 | No |
| **q2** (Aceptación) | q2 | q2 | Sí |

### Ejemplos de Expresiones Regulares Soportadas
* `(a|b)*abb`: Cadenas sobre {a, b} que terminan en "abb".
* `0(0|1)*0`: Cadenas binarias que inician y terminan con "0".
* `a+b+`: Cadenas con una o más 'a' seguidas de una o más 'b'.

---

## 12. Interfaz Gráfica (GUI)

La interfaz, desarrollada con **Flet**, se divide en tres secciones principales:
1. **Panel de Control (Izquierda):** Configuración de la quintupla, estados, alfabeto y carga de archivos.
2. **Lienzo de Visualización (Centro):** Renderizado dinámico del grafo del autómata actual.
3. **Panel de Pruebas (Derecha):** Entrada de cadenas para validación y consola de resultados de conversión.

---

## 13. Resolución de Problemas Comunes

| Problema | Causa Probable | Solución |
| :--- | :--- | :--- |
| Error `ExecutableNotFound: dot` | Graphviz no está en el PATH. | Reinstalar Graphviz y marcar "Add to PATH" o agregarlo manualmente. |
| Error de importación de Flet | Entorno virtual no activo. | Ejecutar el comando de activación `source venv/bin/activate`. |
| El grafo no se actualiza | Error en la sintaxis de transiciones. | Verificar que no existan símbolos fuera del alfabeto definido. |

---

## 14. Consideraciones Académicas
Este proyecto ha sido desarrollado como evidencia de aprendizaje para la **Práctica 5** de la materia **Teoría de la Computación**. Cumple con los requisitos de implementación de modelos computacionales finitos y el tratamiento de lenguajes regulares.
