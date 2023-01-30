"""
Exceptions
"""


class CitasAnyError(Exception):
    """Base exception class"""


class CitasAlreadyExistsError(CitasAnyError):
    """Excepción porque ya existe"""


class CitasAuthenticationError(CitasAnyError):
    """Excepción porque fallo la autentificacion"""


class CitasConnectionError(CitasAnyError):
    """Excepción porque no se pudo conectar"""


class CitasEmptyError(CitasAnyError):
    """Excepción porque no hay resultados"""


class CitasIsDeletedError(CitasAnyError):
    """Excepción porque esta eliminado"""


class CitasMissingConfigurationError(CitasAnyError):
    """Excepción porque falta configuración"""


class CitasNotExistsError(CitasAnyError):
    """Excepción porque no existe"""


class CitasNotValidAnswerError(CitasAnyError):
    """Excepción porque la respuesta no es válida"""


class CitasNotValidParamError(CitasAnyError):
    """Excepción porque un parámetro es inválido"""


class CitasOutOfRangeParamError(CitasAnyError):
    """Excepción porque un parámetro esta fuera de rango"""


class CitasRequestError(CitasAnyError):
    """Excepción porque falló el request"""


class CitasTimeoutError(CitasAnyError):
    """Excepción porque se agoto el tiempo de espera"""


class CitasUnknownError(CitasAnyError):
    """Excepción porque hubo un error desconocido"""


class CitasEncryptError(CitasAnyError):
    """Excepción porque hubo un error al encriptar el XML"""


class CitasGetURLFromXMLEncryptedError(CitasAnyError):
    """Excepción porque hubo un error al obtener al URL del XML ecriptado"""


class CitasDesencryptError(CitasAnyError):
    """Excepción porque hubo error al desencriptar el XML"""


class CitasBankResponseInvalidError(CitasAnyError):
    """Excepción porque la respuesta del banco no es válida"""


class CitasXMLReadError(CitasAnyError):
    """Excepción porque no se puede interpretar correctamente el XML desecriptado"""
