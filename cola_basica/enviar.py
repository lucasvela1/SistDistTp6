import pika

from conexion import conectar, COLA, NOMBRE

conexion = conectar()
canal = conexion.channel()

# Creamos la cola si no existe, o reutilizamos la existente.
# durable=True hace que la definición de la cola sobreviva 
# a un reinicio del broker, siempre que se conserven sus datos.
canal.queue_declare(queue=COLA, durable=True)

# Activamos confirmaciones del broker al publicador.
# La publicación esperará la confirmación de RabbitMQ.
# Esto NO confirma que un worker haya terminado la tarea.
canal.confirm_delivery()

print("Escribí tareas. Para terminar, escribí /salir.")

try:
    while True:
        texto = input("Tarea: ")

        if texto == "/salir":
            break

        if not texto.strip():
            continue

        # Agregamos el nombre del productor al texto.
        mensaje = f"{NOMBRE}: {texto}"

        # Publicamos la tarea en RabbitMQ.
        canal.basic_publish(
            # Usamos el exchange predeterminado de RabbitMQ.
            # Es de tipo direct y ya existe: no lo declaramos.
            exchange="",

            # En el exchange predeterminado, la clave es
            # el nombre de la cola de destino.
            routing_key=COLA,

            body=mensaje.encode("utf-8"),

            # delivery_mode=2 marca el mensaje como persistente.
            properties=pika.BasicProperties(delivery_mode=2),

            mandatory=True,
        )

        print(f"Aceptada por RabbitMQ: {mensaje}")

except KeyboardInterrupt:
    print("\nCerrando productor.")

finally:
    if conexion.is_open:
        conexion.close()