"""
Operaciones básicas sobre cadenas y lenguajes.
"""

from itertools import product


def subcadenas(c):
    """Devuelve todas las subcadenas posibles."""
    return sorted({
        c[i:j]
        for i in range(len(c))
        for j in range(i + 1, len(c) + 1)
    })


def prefijos(c):
    """Devuelve todos los prefijos (incluida la cadena vacía)."""
    return sorted({c[:i] for i in range(len(c) + 1)})


def sufijos(c):
    """Devuelve todos los sufijos (incluida la cadena vacía)."""
    return sorted({c[i:] for i in range(len(c) + 1)})


def kleene(alfabeto, n=3):
    """Cerradura de Kleene Σ* hasta longitud n (incluye ε)."""
    res = [""]
    for i in range(1, n + 1):
        for p in product(alfabeto, repeat=i):
            res.append("".join(p))
    return res


def kleene_positiva(alfabeto, n=3):
    """Cerradura positiva Σ+ hasta longitud n (no incluye ε)."""
    res = []
    for i in range(1, n + 1):
        for p in product(alfabeto, repeat=i):
            res.append("".join(p))
    return res


def concatenar_lenguajes(L1, L2):
    """Concatenación de lenguajes."""
    return sorted({a + b for a in L1 for b in L2})


def union_lenguajes(L1, L2):
    """Unión de lenguajes."""
    return sorted(set(L1) | set(L2))


def interseccion_lenguajes(L1, L2):
    """Intersección de lenguajes."""
    return sorted(set(L1) & set(L2))


def diferencia_lenguajes(L1, L2):
    """Diferencia L1 - L2."""
    return sorted(set(L1) - set(L2))


def potencia_lenguaje(L, n):
    """Potencia L^n."""
    if n == 0:
        return [""]

    res = L[:]
    for _ in range(n - 1):
        res = concatenar_lenguajes(res, L)
    return res


def reflexion_lenguaje(L):
    """Reflexión (inversión) de cada cadena."""
    return sorted({c[::-1] for c in L})
