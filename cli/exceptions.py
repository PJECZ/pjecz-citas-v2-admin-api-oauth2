"""
CLI Exceptions
"""


class CLIError(Exception):
    """Base class for CLI exceptions"""


class CLIConfigurationError(CLIError):
    """Excepcion porque falta o falla la configuracion"""


class CLIAuthenticationError(CLIError):
    """Excepcion porque falla la autenticacion"""


class CLIConnectionError(CLIError):
    """Excepcion porque falla la comunicacion"""


class CLIStatusCodeError(CLIError):
    """Excepcion porque falla el status code"""


class CLIResponseError(CLIError):
    """Excepcion porque falla la operacion"""
