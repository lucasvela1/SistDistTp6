import os
from pathlib import Path
import pika
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv(Path(__file__).resolve().parent / ".env")

def get_env(nombre: str, default: str) -> str:
    """Obtiene una variable de entorno o devuelve el valor por defecto si no está definida."""
    valor = os.getenv(nombre)
    return valor if valor is not None and valor.strip() != "" else default

RABBIT_HOST = get_env("RABBIT_HOST", "localhost")
RABBIT_PORT = int(get_env("RABBIT_PORT", "5672"))
RABBIT_USER = get_env("RABBIT_USER", "tpuser")
RABBIT_PASS = get_env("RABBIT_PASS", "tppass")

COLA_DEFAULT = "hola_mundo"

def obtener_conexion() -> pika.BlockingConnection:
    """Crea y retorna una conexión bloqueante con RabbitMQ."""
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    parametros = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=credenciales,
        heartbeat=600,
    )
    return pika.BlockingConnection(parametros)
