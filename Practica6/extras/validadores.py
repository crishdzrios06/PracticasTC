"""
Validadores con expresiones regulares.
"""

import re


REGEXES = {
    "email": (
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        "Correo electrónico"
    ),
    "telefono": (
        r"^\d{10}$",
        "Teléfono (10 dígitos)"
    ),
    "password": (
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$",
        "Contraseña: 8+ chars, mayúscula, minúscula y dígito"
    ),
    "url": (
        r"^https?:\/\/(www\.)?"
        r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\."
        r"[a-zA-Z0-9()]{1,6}\b"
        r"([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$",
        "URL"
    ),
    "fecha": (
        r"^(0[1-9]|[12]\d|3[01])/"
        r"(0[1-9]|1[0-2])/"
        r"(\d{4})$",
        "Fecha DD/MM/AAAA"
    )
}


def validar(tipo, texto):
    """
    Devuelve (es_valido, patron, mensaje).
    """
    if tipo not in REGEXES:
        return False, "", f"Tipo '{tipo}' desconocido."

    patron, descripcion = REGEXES[tipo]

    if re.match(patron, texto or ""):
        return True, patron, f"{descripcion}: válido ✓"

    return False, patron, f"{descripcion}: NO válido ✗"


def listar_validadores():
    return [
        (clave, descripcion)
        for clave, (_, descripcion) in REGEXES.items()
    ]
