import os
from pathlib import Path

import pika
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

def variable(nombre, default):
    # Consulta una variable.
    # Si no existe o está vacía, usa el valor predeterminado.
    return os.getenv(nombre) or default

NOMBRE = variable("NOMBRE", "Nodo")

# Todos los workers deben usar este mismo nombre de cola.
COLA = "tareas_basicas"

def conectar():
    credenciales = pika.PlainCredentials(
        variable("RABBIT_USER", "tpuser"),
        variable("RABBIT_PASS", "tppass"),
    )

    parametros = pika.ConnectionParameters(
        host=variable("RABBIT_HOST", "localhost"),
        port=int(variable("RABBIT_PORT", "5672")),
        credentials=credenciales,
        # mantenemos la conexión viva durante 10 minutos, aunque no haya actividad.
        heartbeat=600,
    )

    return pika.BlockingConnection(parametros)