import os
from pathlib import Path
import pika
from dotenv import load_dotenv

# Cargar variables de entorno buscando en la carpeta actual o en la raíz del proyecto
directorio_actual = Path(__file__).resolve().parent
dotenv_path = directorio_actual / ".env"
if not dotenv_path.exists():
    dotenv_path = directorio_actual.parent / ".env"

load_dotenv(dotenv_path)

def get_env(nombre: str, default: str) -> str:
    valor = os.getenv(nombre)
    return valor if valor is not None and valor.strip() != "" else default

# Configuración de conexión con RabbitMQ
RABBIT_HOST = get_env("RABBIT_HOST", "localhost")
RABBIT_PORT = int(get_env("RABBIT_PORT", "5672"))
RABBIT_USER = get_env("RABBIT_USER", "tpuser")
RABBIT_PASS = get_env("RABBIT_PASS", "tppass")

# Nombre de la cola compartida para Competing Consumers
COLA_TAREAS = "cola_trabajo_competitivo"

def obtener_conexion() -> pika.BlockingConnection:
    """Retorna una conexión activa con RabbitMQ."""
    credenciales = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    parametros = pika.ConnectionParameters(
        host=RABBIT_HOST,
        port=RABBIT_PORT,
        credentials=credenciales,
        heartbeat=600,
    )
    return pika.BlockingConnection(parametros)
