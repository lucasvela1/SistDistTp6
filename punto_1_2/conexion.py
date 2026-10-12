import os
from pathlib import Path
import pika
from dotenv import load_dotenv

# Cargar variables de entorno buscando en la carpeta actual o en la raíz
directorio_actual = Path(__file__).resolve().parent
dotenv_path = directorio_actual / ".env"
if not dotenv_path.exists():
    dotenv_path = directorio_actual.parent / ".env"

load_dotenv(dotenv_path)

def get_env(nombre: str, default: str) -> str:
    valor = os.getenv(nombre)
    return valor if valor is not None and valor.strip() != "" else default

# Parámetros de conexión a RabbitMQ
RABBIT_HOST = get_env("RABBIT_HOST", "localhost")
RABBIT_PORT = int(get_env("RABBIT_PORT", "5672"))
RABBIT_USER = get_env("RABBIT_USER", "tpuser")
RABBIT_PASS = get_env("RABBIT_PASS", "tppass")

# Nombre y tipo de Exchange para Pub/Sub con Tópicos
EXCHANGE_TOPIC = "stocks_topic"
TIPO_EXCHANGE = "topic"

def obtener_conexion() -> pika.BlockingConnection:
    """Establece y retorna la conexión con el broker RabbitMQ."""
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    parametros = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=credenciales,
        heartbeat=600,
    )
    return pika.BlockingConnection(parametros)
