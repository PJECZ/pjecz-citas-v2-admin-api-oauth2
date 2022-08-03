"""
CLI Exceptions
"""


class CLIAnyError(Exception):
    """Base class for CLI exceptions"""


class CLIConfigurationError(CLIAnyError):
    """Excepcion porque falta o falla la configuracion"""


class CLIAuthenticationError(CLIAnyError):
    """Excepcion porque falla la autenticacion"""


class CLIConnectionError(CLIAnyError):
    """Excepcion porque falla la comunicacion"""


class CLIStatusCodeError(CLIAnyError):
    """Excepcion porque falla el status code"""


class CLIResponseError(CLIAnyError):
    """Excepcion porque falla la operacion"""
