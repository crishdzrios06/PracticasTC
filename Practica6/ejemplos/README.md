# Archivos `.jff` de ejemplo

Estos archivos están en formato **JFLAP** y abren tanto en este simulador
como en el JFLAP original. Cada uno cumple con un lenguaje libre de
contexto típico que se estudia en Teoría de la Computación.

---

## 1. `pda_anbn.jff`

**Lenguaje:** L = { aⁿbⁿ | n ≥ 1 }

Acepta cadenas con la misma cantidad de a's seguidas de b's. Es el ejemplo
canónico de un lenguaje que **no** es regular pero sí es libre de contexto.

| Estados | Σ | Γ | q₀ | Z₀ | F |
|---|---|---|---|---|---|
| `q0`, `q1`, `q2` | `{a, b}` | `{A, Z}` | `q0` | `Z` | `{q2}` |

**Transiciones:**
```
q0, a, Z -> q0, AZ          (apilo A, conservo Z al fondo)
q0, a, A -> q0, AA          (sigo apilando A)
q0, b, A -> q1, ε           (cambio a q1 y empiezo a desapilar)
q1, b, A -> q1, ε           (sigo desapilando)
q1, λ, Z -> q2, Z           (transición lambda a estado final)
```

**Cadenas de prueba:**
- ✅ Aceptan: `ab`, `aabb`, `aaabbb`, `aaaabbbb`
- ❌ Rechazan: `a`, `b`, `aab`, `abb`, `abab`, `aabbb`

---

## 2. `pda_balanceados.jff`

**Lenguaje:** paréntesis correctamente balanceados, incluyendo la cadena
vacía.

| Estados | Σ | Γ | q₀ | Z₀ | F |
|---|---|---|---|---|---|
| `q0`, `q1` | `{ (, ) }` | `{P, Z}` | `q0` | `Z` | `{q1}` |

**Transiciones:**
```
q0, (, Z -> q0, PZ          (apilo P para cada apertura)
q0, (, P -> q0, PP
q0, ), P -> q0, ε           (desapilo por cada cierre)
q0, λ, Z -> q1, Z           (pila quedó "vacía" → acepta)
```

**Cadenas de prueba:**
- ✅ Aceptan: ` ` (vacía), `()`, `(())`, `()()`, `((()))`, `(()(()))`
- ❌ Rechazan: `(`, `())`, `(()`, `)(`

---

## 3. `pda_wcwR.jff`

**Lenguaje:** L = { wcwᴿ | w ∈ {a,b}* } — palabras centradas en `c` donde
la segunda mitad es el reflejo de la primera.

| Estados | Σ | Γ | q₀ | Z₀ | F |
|---|---|---|---|---|---|
| `q0`, `q1`, `q2` | `{a, b, c}` | `{A, B, Z}` | `q0` | `Z` | `{q2}` |

**Transiciones:**
```
q0, a, Z -> q0, AZ          (apilo lo que voy leyendo antes de la c)
q0, a, A -> q0, AA
q0, a, B -> q0, AB
q0, b, Z -> q0, BZ
q0, b, A -> q0, BA
q0, b, B -> q0, BB
q0, c, Z -> q1, Z           (al ver c, paso a la fase de comparación)
q0, c, A -> q1, A
q0, c, B -> q1, B
q1, a, A -> q1, ε           (cada símbolo de la 2ª mitad debe coincidir)
q1, b, B -> q1, ε
q1, λ, Z -> q2, Z           (pila vacía → acepto)
```

**Cadenas de prueba:**
- ✅ Aceptan: `c`, `aca`, `bcb`, `abcba`, `aabcbaa`, `bbacabb`
- ❌ Rechazan: `ab`, `abcab`, `abccba` (doble c), `aacaa` (este caso particular sí acepta porque coincide con el patrón)

---

## Cómo usarlos

**En este simulador:**

1. Abre **Autómatas de Pila** en la barra lateral.
2. Pulsa **Cargar .jff** y elige el archivo.
3. Pulsa **Construir** para validar y dibujar.
4. Escribe una cadena de prueba y pulsa **Simular**.

**En JFLAP:**

1. Abre JFLAP.
2. `File → Open` y selecciona el `.jff`.
3. `Input → Step with closure` para simular paso a paso.

---

## Crear tus propios ejemplos

Puedes diseñar tu PDA directamente en el panel y guardarlo con el botón
**Guardar .jff** del propio simulador. El formato producido es 100 %
compatible con JFLAP.
