# Simulador de Autómatas Finitos

### Prácticas 1, 2 y 3 – Desarrollo Progresivo de Software

---

##  Descripción General

Este proyecto consiste en el desarrollo de un **simulador de autómatas finitos** implementado en Python, el cual fue construido de manera incremental a lo largo de tres prácticas académicas.

El objetivo principal es modelar, simular y analizar distintos tipos de autómatas, integrando funcionalidades teóricas de la materia de **Lenguajes Formales y Autómatas** en una aplicación interactiva con interfaz gráfica.

---

##  Objetivos del Proyecto

* Implementar la simulación de distintos tipos de autómatas:

  * Autómatas Finitos Deterministas (AFD)
  * Autómatas Finitos No Deterministas (AFND)
  * AFND con transiciones λ (lambda)

* Desarrollar algoritmos fundamentales:

  * Conversión de AFND a AFD (método de subconjuntos)
  * Eliminación de transiciones λ
  * Minimización de AFD

* Construir una interfaz gráfica funcional que permita:

  * Ingreso manual de autómatas
  * Carga de archivos `.jff`
  * Visualización del proceso de ejecución

---

##  Desarrollo por Prácticas

---

###  Práctica 1: Fundamentos y Simulación Básica

En esta etapa se implementaron las bases del sistema:

* Definición de estructuras de datos para autómatas
* Simulación de AFD
* Validación de cadenas
* Visualización del recorrido de estados

 Resultado:
Se logró un simulador funcional para autómatas deterministas.

---

###  Práctica 2: Extensión a No Determinismo

Se amplió el sistema para soportar:

* AFND (múltiples transiciones por símbolo)
* AFND con transiciones λ
* Implementación de clausura lambda
* Visualización de conjuntos de estados activos

 Resultado:
El sistema ahora puede manejar no determinismo y transiciones vacías correctamente.

---

###  Práctica 3: Algoritmos Avanzados y Optimización

Se integraron algoritmos más complejos:

#### ✔ Conversión AFND → AFD

* Implementación del método de subconjuntos
* Generación de nuevos estados como conjuntos

#### ✔ Eliminación de transiciones λ

* Transformación de AFND-λ a AFND puro
* Uso de clausura lambda para reconstrucción

#### ✔ Minimización de AFD

* Eliminación de estados inaccesibles
* Tabla de equivalencias
* Construcción del autómata mínimo

#### ✔ Visualización paso a paso

* Representación del procesamiento de cadenas
* Seguimiento de estados en cada iteración

 Resultado:
Se obtuvo un sistema completo capaz de transformar y optimizar autómatas.

---

##  Funcionalidades Principales

* Simulación de AFD, AFND y AFND-λ
* Validación de cadenas
* Conversión entre modelos de autómatas
* Minimización de autómatas deterministas
* Visualización paso a paso del procesamiento
* Carga de archivos `.jff` (compatibles con JFLAP)
* Operaciones adicionales:

  * Subcadenas
  * Prefijos
  * Sufijos
  * Cerradura de Kleene

---

##  Interfaz de Usuario

La aplicación cuenta con una interfaz gráfica desarrollada con **Flet**, que permite:

* Ingresar autómatas manualmente
* Cargar archivos externos
* Ejecutar simulaciones de forma interactiva
* Visualizar resultados de manera clara y organizada

---

##  Estructura del Proyecto

```
SimuladorAutomatas/
│
├── main.py
├── requirements.txt
├── README.md
│
├── automatas/
├── utils/
├── ui/
├── extras/
```

---

##  Ejecución del Proyecto

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la aplicación

```bash
python main.py
```

---

##  Ejemplo de Uso

Entrada:

```
Estados: q0,q1
Alfabeto: 0,1
Inicial: q0
Finales: q1
Transiciones:
q0,1->q1 ; q1,0->q0
```

Cadena:

```
101
```

Salida esperada:

```
ACEPTADA
```

---

##  Fundamento Teórico

Este proyecto se basa en conceptos fundamentales de:

* Teoría de autómatas
* Lenguajes formales
* Computabilidad

Incluyendo:

* Autómatas finitos deterministas y no deterministas
* Clausura lambda
* Equivalencia de autómatas
* Minimización de estados

---

##  Conclusión

El desarrollo progresivo del sistema permitió comprender de manera práctica cómo los conceptos teóricos de los autómatas pueden implementarse en software real.

Se logró integrar múltiples algoritmos y estructuras en una aplicación funcional, demostrando la relación directa entre teoría y práctica en el área de ciencias de la computación.

---

##  Autor

4CV4 HERNÁNDEZ RÍOS CRISTIAN SEBASTIAN
4CV4 LÓPEZ TOLEDO KEVIN ANTONIO

---

##  Notas Finales

* El sistema es extensible y modular
* Puede adaptarse para incluir más tipos de autómatas
* Representa una base sólida para proyectos más avanzados

---
