import sys
from conexion import obtener_conexion, COLA_DEFAULT

def main():
    mensaje = sys.argv[1] if len(sys.argv) > 1 else "¡Hola Mundo desde RabbitMQ!"

    conexion = obtener_conexion()
    canal = conexion.channel()

    # Declaramos la cola para asegurarnos de que exista antes de publicar
    canal.queue_declare(queue=COLA_DEFAULT, durable=True)

    # Publicamos el mensaje en la cola utilizando el exchange por defecto
    canal.basic_publish(
        exchange="",
        routing_key=COLA_DEFAULT,
        body=mensaje.encode("utf-8"),
    )

    print(f"[Productor] Mensaje enviado a '{COLA_DEFAULT}': '{mensaje}'")
    conexion.close()

if __name__ == "__main__":
    main()
