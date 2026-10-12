from conexion import conectar, EXCHANGE, NOMBRE

conexion = conectar()
canal = conexion.channel()

canal.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="fanout",
)

resultado = canal.queue_declare(
    queue="",
    exclusive=True,
)

cola = resultado.method.queue

canal.queue_bind(
    exchange=EXCHANGE,
    queue=cola,
)


def mostrar(canal, metodo, propiedades, cuerpo):
    mensaje = cuerpo.decode("utf-8")
    print(f"[{NOMBRE}] Recibido: {mensaje}", flush=True)


canal.basic_consume(
    queue=cola,
    on_message_callback=mostrar,
    auto_ack=True,
)

print(f"[{NOMBRE}] Esperando avisos. Ctrl+C para salir.")
print(f"Mi cola: {cola}")

try:
    canal.start_consuming()

except KeyboardInterrupt:
    print("\nCerrando suscriptor.")

finally:
    if conexion.is_open:
        conexion.close()