import sys
import pika
from conexion import obtener_conexion, COLA_TAREAS

# Lote de tareas predeterminado para demostrar la distribución y el paralelismo.
# Cada punto (.) representa 1 segundo de trabajo para el worker.
TAREAS_DEMO = [
    "Tarea A: Reporte financiero...",         # 3 segundos
    "Tarea B: Backup de base de datos.....",   # 5 segundos
    "Tarea C: Notificación email.",           # 1 segundo
    "Tarea D: Compresión de video....",        # 4 segundos
    "Tarea E: Generar factura..",             # 2 segundos
    "Tarea F: Sincronizar catálogo...",       # 3 segundos
]

def encolar_tarea(canal, tarea: str):
    canal.basic_publish(
        exchange="",
        routing_key=COLA_TAREAS,
        body=tarea.encode("utf-8"),
        # Marcamos el mensaje como persistente (delivery_mode=2) para tolerar caídas del broker
        properties=pika.BasicProperties(delivery_mode=2),
    )
    puntos = tarea.count(".")
    print(f"[Productor] Encolada: '{tarea}' (~{puntos} seg)")

def main():
    conexion = obtener_conexion()
    canal = conexion.channel()

    # Declaramos la cola como durable (persiste a reinicios de RabbitMQ)
    canal.queue_declare(queue=COLA_TAREAS, durable=True)

    # Si se pasan tareas por parámetro, se encolan esas; si no, se encola el lote demo
    if len(sys.argv) > 1:
        tareas = [" ".join(sys.argv[1:])]
    else:
        tareas = TAREAS_DEMO

    tiempo_total_estimado = sum(t.count(".") if "." in t else 1 for t in tareas)
    print(f"=== Productor de Tareas (Competing Consumers) ===")
    print(f"Encolando {len(tareas)} tareas en la cola '{COLA_TAREAS}'...")
    print(f"Tiempo de trabajo total acumulado (secuencial): ~{tiempo_total_estimado} segundos\n")

    for tarea in tareas:
        encolar_tarea(canal, tarea)

    print(f"\n[Productor] Todas las tareas fueron encoladas correctamente.")
    print("Observá cómo se distribuyen entre los workers activos.")
    conexion.close()

if __name__ == "__main__":
    main()
