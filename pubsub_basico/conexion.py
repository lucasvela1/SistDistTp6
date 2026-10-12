import os
from pathlib import Path

import pika
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))


def variable(nombre, default):
    return os.getenv(nombre) or default


NOMBRE = variable("NOMBRE", "Nodo")
EXCHANGE = "avisos_basicos"


def conectar():
    credenciales = pika.PlainCredentials(
        variable("RABBIT_USER", "tpuser"),
        variable("RABBIT_PASS", "tppass"),
    )

    parametros = pika.ConnectionParameters(
        host=variable("RABBIT_HOST", "localhost"),
        port=int(variable("RABBIT_PORT", "5672")),
        credentials=credenciales,
    )

    return pika.BlockingConnection(parametros)