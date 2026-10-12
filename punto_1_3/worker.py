import sys
import time
from conexion import obtener_conexion, COLA_TAREAS

# Identificador del worker (por defecto 'Worker-1' o tomado del primer argumento)
nombre_worker = sys.argv[1] if len(sys.argv) > 1 else "Worker-1"

def callback(ch, method, properties, body):
    tarea = body.decode("utf-8")
    # La duración es proporcional a la cantidad de puntos en el mensaje (mínimo 1 segundo)
    duracion = tarea.count(".") if "." in tarea else 1

    print(f"[{nombre_worker}] ⏳ Tomó tarea: '{tarea}' | Tiempo estimado: {duracion}s", flush=True)

    # Simulación del procesamiento pesado
    time.sleep(duracion)

    # Confirmación MANUAL (ACK): Solo se envía cuando la tarea realmente terminó.
    # Si el worker se cae antes de esta línea, RabbitMQ reencola la tarea.
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"[{nombre_worker}] ✅ Finalizada con éxito (ACK enviado): '{tarea}'\n", flush=True)

def main():
    conexion = obtener_conexion()
    canal = conexion.channel()

    # Declaramos la misma cola durable
    canal.queue_declare(queue=COLA_TAREAS, durable=True)

    # FAIR DISPATCH (prefetch = 1):
    # Le indica a RabbitMQ que NO entregue más de 1 tarea a la vez a este worker
    # hasta que haya enviado el ACK de la tarea previa.
    # Esto evita que un worker acapare tareas mientras otros están ociosos.
    canal.basic_qos(prefetch_count=1)

    # auto_ack=False asegura que la confirmación sea manual
    canal.basic_consume(
        queue=COLA_TAREAS,
        on_message_callback=callback,
        auto_ack=False,
    )

    print(f"[{nombre_worker}] 🚀 Conectado y listo en '{COLA_TAREAS}' (prefetch=1, ack manual).")
    print(f"[{nombre_worker}] Esperando tareas. Presioná CTRL+C para detener.\n", flush=True)

    try:
        canal.start_consuming()
    except KeyboardInterrupt:
        print(f"\n[{nombre_worker}] 🛑 Deteniendo worker...")
    finally:
        if conexion.is_open:
            conexion.close()

if __name__ == "__main__":
    main()
