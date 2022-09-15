"""
Exceptions
"""


class CitasAnyError(Exception):
    """Base exception class"""


class CitasAlreadyExistsError(CitasAnyError):
    """Excepción ya existe"""


class CitasAuthenticationError(CitasAnyError):
    """Excepción por que fallo la autentificacion"""


class CitasEmptyError(CitasAnyError):
    """Excepción por que no hay resultados"""


class CitasIsDeletedError(CitasAnyError):
    """Excepción esta eliminado"""


class CitasNotExistsError(CitasAnyError):
    """Excepción no existe"""


class CitasNotValidParamError(CitasAnyError):
    """Excepción porque un parámetro es inválido"""


class CitasOutOfRangeParamError(CitasAnyError):
    """Excepción porque un parámetro esta fuera de rango"""
