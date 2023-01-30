"""
Santander Web Pay Plus
"""
import re
import asyncio
import os
import urllib
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import requests

from lib.AESEncryption import AES128Encryption
from lib.exceptions import (
    CitasConnectionError,
    CitasMissingConfigurationError,
    CitasNotValidAnswerError,
    CitasTimeoutError,
    CitasRequestError,
    CitasUnknownError,
    CitasEncryptError,
    CitasGetURLFromXMLEncryptedError,
    CitasDesencryptError,
    CitasBankResponseInvalidError,
    CitasXMLReadError,
)

XML_ENCRYPT_REGEXP = r"^[a-zA-Z0-9+\/=]{32,}$"

RESPUESTA_EXITO = "approved"
RESPUESTA_DENEGADA = "denied"
RESPUESTA_ERROR = "error"

load_dotenv()
WPP_COMMERCE_ID = os.getenv("WPP_COMMERCE_ID", None)
WPP_COMPANY_ID = os.getenv("WPP_COMPANY_ID", None)
WPP_BRANCH_ID = os.getenv("WPP_BRANCH_ID", None)
WPP_KEY = os.getenv("WPP_KEY", None)
WPP_PASS = os.getenv("WPP_PASS", None)
WPP_TIMEOUT = int(os.getenv("WPP_TIMEOUT", "12"))
WPP_URL = os.getenv("WPP_URL", None)
WPP_USER = os.getenv("WPP_USER", None)


def create_chain_xml(
    pago_id: int,
    amount: float,
    email: str,
    description: str,
    cit_client_id: int,
) -> str:
    """Crear cadena XML"""

    # Validar WPP_COMPANY_ID
    if WPP_COMPANY_ID is None:
        raise CitasMissingConfigurationError("Falta declarar la variable de entorno WPP_COMPANY_ID.")

    # Validar WPP_BRANCH_ID
    if WPP_BRANCH_ID is None:
        raise CitasMissingConfigurationError("Falta declarar la variable de entorno WPP_BRANCH_ID.")

    # Validar WPP_USER
    if WPP_USER is None:
        raise CitasMissingConfigurationError("Falta declarar la variable de entorno WPP_USER.")

    # Validar WPP_PASS
    if WPP_PASS is None:
        raise CitasMissingConfigurationError("Falta declarar la variable de entorno WPP_PASS.")

    # Inicializar XML
    root = ET.Element("P")

    # Inicializar datos de la organización
    business = ET.SubElement(root, "business")
    ET.SubElement(business, "id_company").text = WPP_COMPANY_ID
    ET.SubElement(business, "id_branch").text = WPP_BRANCH_ID
    ET.SubElement(business, "user").text = WPP_USER
    ET.SubElement(business, "pwd").text = WPP_PASS

    # Inicializar datos de la version
    ET.SubElement(root, "version").text = "IntegraWPP"

    # Inicializar datos del cliente y del pago
    url = ET.SubElement(root, "url")
    ET.SubElement(url, "reference").text = str(pago_id)
    ET.SubElement(url, "amount").text = str(amount)
    ET.SubElement(url, "moneda").text = "MXN"
    ET.SubElement(url, "canal").text = "W"
    ET.SubElement(url, "omitir_notif_default").text = "0"
    ET.SubElement(url, "st_correo").text = "1"
    ET.SubElement(url, "mail_cliente").text = email

    # Inicializar datos adicionales
    data = ET.SubElement(url, "datos_adicionales")

    # Inicializar descripción del servicio
    data1 = ET.SubElement(data, "data")
    data1.attrib["id"] = "1"
    data1.attrib["display"] = "true"
    label1 = ET.SubElement(data1, "label")
    label1.text = "Servicio"
    value1 = ET.SubElement(data1, "value")
    value1.text = description

    # Inicializar descripción del cliente
    data2 = ET.SubElement(data, "data")
    data2.attrib["id"] = "2"
    data2.attrib["display"] = "false"
    label2 = ET.SubElement(data2, "label")
    label2.text = "Cliente ID"
    value2 = ET.SubElement(data2, "value")
    value2.text = str(cit_client_id)

    # Entregar cadena XML
    return ET.tostring(root, encoding="unicode")


def encrypt_chain(chain: str) -> str:
    """Cifrar cadena XML"""
    if WPP_KEY is None:
        raise CitasMissingConfigurationError("Falta declarar la variable de entorno WPP_KEY.")
    aes_encryptor = AES128Encryption()
    ciphertext = aes_encryptor.encrypt(chain, WPP_KEY)
    return ciphertext


def decrypt_chain(chain_encrypted: str) -> str:
    """Descifrar cadena XML"""
    if WPP_KEY is None:
        raise CitasMissingConfigurationError("Falta declarar la variable de entorno WPP_KEY.")
    aes_encryptor = AES128Encryption()
    try:
        plaintext = aes_encryptor.decrypt(WPP_KEY, chain_encrypted)
    except Exception as error:
        raise CitasDesencryptError("Error al desencriptar la respuesta del Banco.") from error
    return plaintext


def create_chain_xml_sender(chain: str) -> str:
    """Crear cadena para XML de envío WPP"""

    # Get the commerce ID
    if WPP_COMMERCE_ID is None:
        raise CitasMissingConfigurationError("No se ha definido el WPP_COMMERCE_ID")

    # Get the WPP URL
    if WPP_URL is None:
        raise CitasMissingConfigurationError("No se ha definido el WPP_URL")

    # Pack the chain
    root = ET.Element("pgs")
    ET.SubElement(root, "data0").text = WPP_COMMERCE_ID
    ET.SubElement(root, "data").text = chain
    chain_bytes = ET.tostring(root, encoding="unicode")

    # Prepare the request
    encodedString = urllib.parse.quote(chain_bytes, "utf-8")
    return encodedString


async def send_chain(chain: str) -> str:
    """Enviar cadena a WPP"""

    # Prepare the request
    payload = "xml=" + create_chain_xml_sender(chain)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    # Send the request
    try:
        response = requests.request(
            "POST",
            WPP_URL,
            headers=headers,
            data=payload,
            timeout=WPP_TIMEOUT,
        )
    except requests.exceptions.ConnectionError as error:
        raise CitasConnectionError("Error porque no se pudo conectar a WPP") from error
    except requests.exceptions.Timeout as error:
        raise CitasTimeoutError("Error porque se agoto el tiempo de espera con WPP") from error
    except requests.exceptions.RequestException as error:
        raise CitasRequestError("Error al enviar la cadena a WPP") from error
    except Exception as error:
        raise CitasUnknownError("Error desconocido al enviar la cadena a WPP") from error

    # Entregar
    return response.text


def get_url_from_xml_encrypt(xml_encrypt: str):
    """Extrae la url del xml de respuesta"""

    # Se desencripta el XML enviado por el Banco
    try:
        xml = decrypt_chain(xml_encrypt)
    except Exception as error:
        raise CitasDesencryptError("No se puede desencriptar el XML del Banco") from error

    root = ET.fromstring(xml)
    url = root.find("nb_url").text

    if url is None or url == "":
        # nb_response = root.find("nb_response").text
        raise CitasNotValidAnswerError("Error en XML del Banco. (url vacía).")

    return url


def create_pay_link(
    pago_id: int,
    email: str,
    service_detail: str,
    cit_client_id: int,
    amount: float,
) -> str:
    """Regresa el link para mostrar el formulario de pago"""

    # Crear cadena XML
    chain = create_chain_xml(
        pago_id=pago_id,
        amount=amount,
        email=email,
        description=service_detail,
        cit_client_id=cit_client_id,
    )

    # Encriptación del XML
    try:
        chain_encrypt = encrypt_chain(chain).decode()  # bytes
    except Exception as error:
        raise CitasEncryptError("Error al encriptar el XML") from error

    # Enviar cadena XML a WPP
    respuesta = None
    try:
        respuesta = asyncio.run(send_chain(chain_encrypt))
    except asyncio.TimeoutError as error:
        raise CitasTimeoutError("Error porque se agoto el tiempo de espera con WPP") from error
    except Exception as error:
        raise CitasUnknownError("Error al tratar de enviar la cadena XML a WPP") from error

    # Si no hay respuesta, causar error
    if respuesta is None or respuesta == "" or respuesta == "\n":
        raise CitasNotValidAnswerError("Error en la respuesta de WPP (respuesta vacía)")

    # Descifrar la respuesta y extraer la url
    try:
        url = get_url_from_xml_encrypt(respuesta)
    except Exception as error:
        raise CitasGetURLFromXMLEncryptedError(f"Error al obtener la URL del Banco desde su XML encriptado. {str(error)}") from error

    # Entregar
    return url


def convert_xml_encrypt_to_dict(xml_encrypt_str: str) -> dict:
    """Convertir el xml encriptado a un diccionario"""

    if re.fullmatch(XML_ENCRYPT_REGEXP, xml_encrypt_str) is None:
        raise CitasBankResponseInvalidError(f"Error en la respuesta del banco porque no cumple la validación por regexp. [{xml_encrypt_str}].")

    # Inicializar diccionario de respuesta
    respuesta = {
        "pago_id": None,
        "respuesta": None,
        "folio": None,
        "auth": None,
        "email": None,
    }

    # Procesar el xml encriptado
    try:
        xml = decrypt_chain(xml_encrypt_str)
    except Exception as error:
        raise CitasBankResponseInvalidError(f"Error en la respuesta del Banco porque es inválida. {str(error)}") from error

    # Lee el archivo XML
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as error:
        raise CitasXMLReadError("Error no se entiende el archivo XML desencriptado.") from error

    # Obtener nodos de respuesta
    respuesta["pago_id"] = root.find("reference").text
    respuesta["respuesta"] = root.find("response").text
    respuesta["folio"] = root.find("foliocpagos").text
    respuesta["auth"] = root.find("auth").text
    respuesta["email"] = root.find("email").text

    # Entregar diccionario
    return respuesta
