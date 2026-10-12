from conexion import conectar, EXCHANGE, NOMBRE

conexion = conectar()
canal = conexion.channel()

canal.exchange_declare(
    exchange=EXCHANGE,
    exchange_type="fanout",
)

print("Escribí un aviso. Para terminar, escribí /salir.")

try:
    while True:
        texto = input("Aviso: ")

        if texto == "/salir":
            break

        if not texto.strip():
            continue

        mensaje = f"{NOMBRE}: {texto}"

        canal.basic_publish(
            exchange=EXCHANGE,
            routing_key="",
            body=mensaje.encode("utf-8"),
        )

        print(f"Publicado: {mensaje}")

except KeyboardInterrupt:
    print("\nCerrando publicador.")

finally:
    conexion.close()