"""
CLI Commands Cit Clientes Registros Send Messages
"""
from datetime import datetime
from typing import Any

from config.settings import LIMIT

from .request_api import get_cit_clientes_recuperaciones


def resend_cit_clientes_recuperaciones(
    authorization_header: dict,
) -> Any:
    """Reenviar los mensajes de las recuperaciones"""

    # Comparar las fechas de expiracion con la de hoy
    ahora = datetime.now()

    # Inicializar el listado donde se acumulan los mensajes enviados
    enviados = []

    # Comenzar con offset cero
    offset = 0

    # Consultar por primera vez las recuperaciones pendientes
    cit_clientes_recuperaciones = get_cit_clientes_recuperaciones(
        authorization_header=authorization_header,
        recuperado=False,
        offset=offset,
    )
    total = cit_clientes_recuperaciones["total"]

    # Bucle
    while offset < total:

        # Bucle para procesar resultados de la consulta
        for item in cit_clientes_recuperaciones["items"]:

            # Si ya expiró, no se envía y de da de baja
            expiracion = datetime.strptime(item["expiracion"], "%Y-%m-%dT%H:%M:%S.%f")
            if expiracion < ahora:
                # delete_cit_cliente_recuperacion(authorization_header: dict, id=item["expiracion"], )
                continue

            # Acumular
            enviados.append(item)

        # Siguiente consulta
        offset += LIMIT

        # Consultar las recuperaciones pendientes
        cit_clientes_recuperaciones = get_cit_clientes_recuperaciones(
            authorization_header=authorization_header,
            recuperado=False,
            offset=offset,
        )

        # Si ya no hay items, salir del bucle
        if len(cit_clientes_recuperaciones["items"]) == 0:
            break

    # Entregar
    return {"items": enviados, "total": len(enviados)}
