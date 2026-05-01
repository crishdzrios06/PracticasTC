# Ejercicio 1: Investigación Exhaustiva sobre Expresiones Regulares

## Introducción

Las expresiones regulares constituyen una herramienta fundamental en la teoría de la computación y en la práctica del desarrollo de software moderno. Su relevancia radica en que permiten describir lenguajes formales mediante patrones, facilitando tanto su análisis matemático como su implementación computacional.

El estudio de las expresiones regulares está estrechamente relacionado con los lenguajes regulares y los autómatas finitos, formando un triángulo conceptual clave dentro de la teoría de lenguajes formales. Estas herramientas permiten modelar sistemas de reconocimiento de patrones con memoria finita, lo cual es esencial en áreas como compiladores, validación de datos y procesamiento de texto.

---

## 1. Lenguajes Regulares

### 1.1 Definición formal

Sea Σ un alfabeto finito. Un lenguaje L ⊆ Σ* es regular si puede definirse recursivamente a partir de:

* El lenguaje vacío ∅
* La cadena vacía ε
* Símbolos individuales del alfabeto
* Operaciones de unión, concatenación y cerradura de Kleene

Equivalentemente, un lenguaje es regular si puede ser reconocido por un autómata finito o descrito mediante una expresión regular.

---

### 1.2 Interpretación conceptual

Los lenguajes regulares representan la clase más simple dentro de los lenguajes formales, ya que no requieren memoria adicional para su reconocimiento, lo cual implica que pueden ser procesados mediante máquinas de estados finitos.

---

### 1.3 Diagrama conceptual: Lenguaje Regular

```
Lenguaje Regular
│
├── Definido por:
│   ├── Expresión regular
│   ├── Autómata finito
│   └── Gramática regular
│
├── Propiedades:
│   ├── Cerrado bajo unión
│   ├── Cerrado bajo concatenación
│   └── Cerrado bajo Kleene (*)
│
└── Ubicación:
    └── Jerarquía de Chomsky (Tipo 3)
```

---

## 2. Expresiones Regulares

### 2.1 Definición formal

Una expresión regular es una construcción algebraica que describe un lenguaje mediante patrones formales definidos sobre un alfabeto, utilizando operadores como unión, concatenación y cerradura de Kleene.

---

### 2.2 Componentes básicos

* Símbolos del alfabeto
* Operador de unión (|)
* Concatenación implícita
* Cerradura de Kleene (*)
* Agrupación mediante paréntesis

---

### 2.3 Diagrama conceptual: Expresión Regular

```
Expresión Regular
│
├── Elementos básicos
│   ├── Símbolos (a, b, 0, 1)
│   ├── ε (cadena vacía)
│   └── ∅ (lenguaje vacío)
│
├── Operadores
│   ├── Unión (R | S)
│   ├── Concatenación (RS)
│   └── Kleene (R*)
│
└── Resultado
    └── Lenguaje regular
```

---

## 3. Operaciones Fundamentales

### 3.1 Unión

Permite representar la alternativa entre lenguajes.

Ejemplo:
R = a | b → {a, b}

---

### 3.2 Concatenación

Permite construir cadenas combinando elementos.

Ejemplo:
R = ab → {ab}

---

### 3.3 Cerradura de Kleene

Permite generar repeticiones infinitas.

Ejemplo:
R = a* → {ε, a, aa, aaa, ...}

---

### 3.4 Diagrama conceptual: Operaciones

```
Operaciones sobre lenguajes
│
├── Unión
│   └── L1 ∪ L2
│
├── Concatenación
│   └── L1L2
│
└── Kleene
    └── L*
```

---

## 4. Jerarquía de Chomsky

La jerarquía de Chomsky clasifica los lenguajes según su poder computacional:

```
Tipo 0 → Lenguajes recursivamente enumerables
Tipo 1 → Sensibles al contexto
Tipo 2 → Libres de contexto
Tipo 3 → Regulares
```

Los lenguajes regulares ocupan el nivel más bajo, lo cual implica menor complejidad pero mayor eficiencia computacional.

---

## 5. Teorema de Kleene

El Teorema de Kleene establece la equivalencia entre:

* Expresiones regulares
* Autómatas finitos

Esto implica que cualquier lenguaje reconocido por un autómata finito puede representarse mediante una expresión regular y viceversa.

---

### 5.1 Diagrama conceptual: Equivalencia

```
Expresiones Regulares
          ⇅
   (Teorema de Kleene)
          ⇅
Autómatas Finitos
```

---

## 6. Aplicaciones Prácticas

### 6.1 Procesamiento de texto

Ejemplo:
\d+ → detecta números

Uso:

* Búsqueda en documentos
* Filtrado de información

---

### 6.2 Análisis léxico

Ejemplo:
[a-zA-Z_][a-zA-Z0-9_]*

Uso:

* Identificación de variables en compiladores

---

### 6.3 Validación de correos electrónicos

Ejemplo:
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-z]{2,}$

Función:

* Verifica estructura válida de correo

---

### 6.4 Validación de números telefónicos

Ejemplo:
^\d{10}$

---

### 6.5 Validación de contraseñas

Ejemplo:
^(?=.*[A-Z])(?=.*[0-9]).{8,}$

---

### 6.6 Automatización y sistemas

Uso en herramientas como:

* grep
* sed
* scripts de automatización

Las expresiones regulares son ampliamente utilizadas en herramientas de procesamiento de texto y sistemas Unix.

---

## 7. Funcionamiento Interno

Las expresiones regulares pueden interpretarse como autómatas finitos que recorren una cadena símbolo por símbolo, verificando si cumple con el patrón definido.

Este proceso se basa en transiciones entre estados, lo que permite modelar el reconocimiento de patrones de manera formal.

---

## Conclusión

Las expresiones regulares representan una herramienta esencial tanto en la teoría como en la práctica de la computación. Su capacidad para describir lenguajes formales, junto con su equivalencia con autómatas finitos, las convierte en un elemento clave en múltiples áreas de la informática.

Además, su aplicabilidad en contextos reales como validación de datos, compiladores y procesamiento de texto demuestra su relevancia en la computación moderna.

---

## Bibliografía (Formato APA)

Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.

Sipser, M. (2012). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.

Kozen, D. C. (1997). *Automata and Computability*. Springer.

Salomaa, A. (1981). *Jewels of Formal Language Theory*. Computer Science Press.

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson.

---

[1]: https://en.wikipedia.org/wiki/Regular_language?utm_source=chatgpt.com "Regular language"
[2]: https://es.wikipedia.org/wiki/Lenguaje_regular?utm_source=chatgpt.com "Lenguaje regular"
[3]: https://es.wikipedia.org/wiki/Expresi%C3%B3n_regular?utm_source=chatgpt.com "Expresión regular"
[4]: https://es.eitca.org/la-seguridad-cibern%C3%A9tica/eitc-es-fundamentos-de-la-teor%C3%ADa-de-la-complejidad-computacional-cctf/idiomas-regulares/expresiones-regulares/Son-lenguajes-regulares-equivalentes-a-m%C3%A1quinas-de-estados-finitos.-a/?utm_source=chatgpt.com "¿Son los lenguajes regulares equivalentes a las máquinas de estados finitos? - Academia EITCA"
