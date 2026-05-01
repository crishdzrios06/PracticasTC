import re

regexes = {
    "email": r"^[\w\.-]+@[\w\.-]+\.\w+$",
    "telefono": r"^\d{10}$",
    "password": r"^(?=.*[A-Z])(?=.*\d).{8,}$"
}

def validar(tipo, texto):
    patron = regexes[tipo]
    if re.match(patron, texto):
        return True, patron, "Válido"
    else:
        return False, patron, "No válido"