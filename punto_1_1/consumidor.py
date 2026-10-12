from conexion import obtener_conexion, COLA_DEFAULT

def callback(ch, method, properties, body):
    mensaje = body.decode("utf-8")
    print(f"[Consumidor] Mensaje recibido: '{mensaje}'")
    # Confirmar procesamiento del mensaje
    # Confirmamos que recibimos el mensaje con ack
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # Establecemos conexión con RabbitMQ
    conexion = obtener_conexion()
    canal = conexion.channel()

    # Declaramos la cola para asegurarnos de que exista
    canal.queue_declare(queue=COLA_DEFAULT, durable=True)

    # Configuramos el callback para recibir mensajes de la cola
    canal.basic_consume(
        queue=COLA_DEFAULT,
        on_message_callback=callback,
        auto_ack=False, # Deshabilitamos el autoack porque vamos a confirmar manualmente con ack
    )

    print(f"[Consumidor] Esperando mensajes en la cola '{COLA_DEFAULT}'. Presiona CTRL+C para salir.")
    try:
        canal.start_consuming()
    except KeyboardInterrupt:
        print("\n[Consumidor] Deteniendo consumidor...") # Ctrl c
    finally:
        if conexion.is_open:
            conexion.close()

if __name__ == "__main__":
    main()
