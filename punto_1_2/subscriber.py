import sys
from conexion import obtener_conexion, EXCHANGE_TOPIC, TIPO_EXCHANGE

def callback(ch, method, properties, body):
    mensaje = body.decode("utf-8")
    routing_key = method.routing_key
    print(f"📥 [Recibido] Routing Key: '{routing_key}' | Mensaje: '{mensaje}'")

def main():
    patrones = sys.argv[1:]

    # Si no se pasó ningún patrón por argumento, damos un menú para elegir fácilmente
    if not patrones:
        print("=== Suscriptor de Eventos (Topic Exchange) ===")
        print("Elegí el patrón de suscripción:")
        print("  1. stock.NYSE.*   (Solo acciones de NYSE)")
        print("  2. stock.#        (Todo lo de stock, cualquier mercado/acción)")
        print("  3. stock.*.AAPL   (Solo AAPL, de cualquier mercado)")
        print("  4. Ingresar patrón personalizado")
        opcion = input("Opción (1/2/3/4): ").strip()

        if opcion == "1":
            patrones = ["stock.NYSE.*"] #El * sirve como wildcard, se subscribe a escuchar todo lo que llegue al stock de NYSE
        elif opcion == "2":
            patrones = ["stock.#"] #El # sirve como wildcard, se subscribe a escuchar todo lo que llegue al stock
        elif opcion == "3":
            patrones = ["stock.*.AAPL"] #Escucha en todos los mercados lo que sea AAPL
        elif opcion == "4":
            patron_custom = input("Ingresá el patrón deseado: ").strip()
            if patron_custom:
                patrones = [patron_custom]
            else:
                patrones = ["#"]
        else:
            print("Opción inválida. Usando 'stock.#' por defecto.")
            patrones = ["stock.#"]

    conexion = obtener_conexion()
    canal = conexion.channel()

    # Declaramos el exchange de tipo topic
    canal.exchange_declare(exchange=EXCHANGE_TOPIC, exchange_type=TIPO_EXCHANGE, durable=True)

    # Creamos una cola exclusiva y efímera (RabbitMQ le asigna un nombre único y la borra al desconectar)
    resultado = canal.queue_declare(queue="", exclusive=True)
    nombre_cola = resultado.method.queue

    # Vinculamos (bind) la cola a cada patrón indicado
    for patron in patrones:
        canal.queue_bind(exchange=EXCHANGE_TOPIC, queue=nombre_cola, routing_key=patron)

    print(f"\n[Suscriptor activo]")
    print(f" - Exchange: '{EXCHANGE_TOPIC}'")
    print(f" - Cola asignada: '{nombre_cola}'")
    print(f" - Patrones escuchados (bindings): {patrones}")
    print("Esperando eventos coincidentes. Presioná CTRL+C para salir.\n")

    canal.basic_consume(
        queue=nombre_cola,
        on_message_callback=callback,
        auto_ack=True,
    )

    try:
        canal.start_consuming()
    except KeyboardInterrupt:
        print("\nCerrando suscriptor...")
    finally:
        if conexion.is_open:
            conexion.close()

if __name__ == "__main__":
    main()
