"""
Safe string
"""
from datetime import date
import re
from unidecode import unidecode

CONTRASENA_REGEXP = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,24}$"
CURP_REGEXP = r"^[A-Z]{4}\d{6}[A-Z]{6}[A-Z0-9]{2}$"
EMAIL_REGEXP = r"^[\w.-]+@[\w.-]+\.\w+$"
TELEFONO_REGEXP = r"^[1-9]\d{9}$"


def safe_clave(input_str, max_len=16):
    """Safe clave"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    new_string = re.sub(r"[^a-zA-Z0-9()-]+", " ", unidecode(input_str))
    removed_multiple_spaces = re.sub(r"\s+", " ", new_string)
    spaces_to_dashes = re.sub(r"\s+", "-", removed_multiple_spaces)
    final = spaces_to_dashes.strip().upper()
    if len(final) > max_len:
        return final[:max_len]
    return final


def safe_curp(input_str, search_fragment=False):
    """Safe CURP"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    removed_spaces = re.sub(r"\s", "", input_str)
    removed_simbols = re.sub(r"[()\[\]:/.-]+", "", removed_spaces)
    final = unidecode(removed_simbols.upper())
    if search_fragment:
        if re.match(r"^[A-Z\d]+$", final) is None:
            return None
        return final
    if re.fullmatch(CURP_REGEXP, final) is None:
        return None
    return final


def safe_email(input_str, search_fragment=False):
    """Safe string"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    final = input_str.lower()
    if search_fragment:
        if re.match(r"^[\w.-]*@*[\w.-]*\.*\w*$", final) is None:
            return None
        return final
    if re.match(EMAIL_REGEXP, final) is None:
        return None
    return final


def safe_expediente(input_str):
    """Safe expediente"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    elementos = re.sub(r"[^0-9]+", "-", input_str).split("-")
    try:
        numero = int(elementos[0])
        ano = int(elementos[1])
    except (IndexError, ValueError) as error:
        raise error
    if numero < 0:
        return None
    if ano < 1950 or ano > date.today().year:
        return None
    return f"{str(numero)}/{str(ano)}"


def safe_string(input_str, max_len=250, to_uppercase=True, do_unidecode=True):
    """Safe string"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    if do_unidecode:
        new_string = re.sub(r"[^a-zA-Z0-9.(),/-]+", " ", unidecode(input_str))
    else:
        new_string = re.sub(r"[^a-záéíóúüñA-ZÁÉÍÓÚÜÑ0-9.(),/-]+", " ", input_str)
    removed_multiple_spaces = re.sub(r"\s+", " ", new_string)
    final = removed_multiple_spaces.strip()
    if to_uppercase:
        final = final.upper()
    if max_len == 0:
        return final
    return (final[:max_len] + "...") if len(final) > max_len else final


def safe_telefono(input_str):
    """Safe telefono"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    solo_numeros = re.sub(r"[^0-9]+", "", unidecode(input_str))
    if re.match(TELEFONO_REGEXP, solo_numeros) is None:
        return None
    return solo_numeros
