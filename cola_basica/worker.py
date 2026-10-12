import sys
import time

from conexion import conectar, COLA, NOMBRE

nombre = sys.argv[1] if len(sys.argv) > 1 else NOMBRE

conexion = conectar()
canal = conexion.channel()

canal.queue_declare(queue=COLA, durable=True)
canal.basic_qos(prefetch_count=1)


def procesar(canal, metodo, propiedades, cuerpo):
    # canal: canal por el que recibimos la tarea.
    # metodo: información de la entrega, incluido delivery_tag.
    # propiedades: metadatos del mensaje.
    # cuerpo: contenido de la tarea en bytes.
    tarea = cuerpo.decode("utf-8")

    print(f"[{nombre}] Comenzando: {tarea}", flush=True)

    # Simulamos un trabajo de tres segundos.
    # En una aplicación real, aquí iría el procesamiento:
    # generar un informe, convertir un archivo, etc.
    time.sleep(3)

    # Confirmamos SOLO después de terminar el trabajo.
    # delivery_tag identifica esta entrega dentro del canal.
    # RabbitMQ puede retirar el mensaje de la cola.
    canal.basic_ack(delivery_tag=metodo.delivery_tag)

    print(f"[{nombre}] Terminada: {tarea}", flush=True)

# Registramos el worker como consumidor de la cola compartida.
canal.basic_consume(
    queue=COLA,

    # Pasamos la función, sin ejecutarla aquí.
    on_message_callback=procesar,

    auto_ack=False,
)

print(f"[{nombre}] Esperando tareas en '{COLA}'.", flush=True)

try:
    canal.start_consuming()

except KeyboardInterrupt:
    print(f"\n[{nombre}] Cerrando.")

finally:
    if conexion.is_open:
        conexion.close()