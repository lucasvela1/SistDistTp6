import sys
from conexion import obtener_conexion, EXCHANGE_TOPIC, TIPO_EXCHANGE

def publicar_evento(canal, routing_key: str, mensaje: str):
    canal.basic_publish(
        exchange=EXCHANGE_TOPIC,
        routing_key=routing_key,
        body=mensaje.encode("utf-8"),
    )
    print(f"[Publicador] Evento enviado con clave '{routing_key}': '{mensaje}'")

def main():
    conexion = obtener_conexion()
    canal = conexion.channel()

    # Declaramos el exchange de tipo 'topic'
    canal.exchange_declare(exchange=EXCHANGE_TOPIC, exchange_type=TIPO_EXCHANGE, durable=True)

    # Si se pasan parámetros por consola: python publisher.py <routing_key> <mensaje>
    if len(sys.argv) > 2:
        routing_key = sys.argv[1]
        mensaje = " ".join(sys.argv[2:])
        publicar_evento(canal, routing_key, mensaje)
    else:
        # Modo interactivo amigable
        print("=== Publicador de Eventos (Topic Exchange) ===")
        print(f"Exchange activo: '{EXCHANGE_TOPIC}' (tipo: {TIPO_EXCHANGE})")
        print("\nEjemplos de routing keys:")
        print("  1. stock.NYSE.AAPL    (Bolsa NYSE, acción Apple)")
        print("  2. stock.NASDAQ.MSFT  (Bolsa NASDAQ, acción Microsoft)")
        print("  3. stock.NYSE.IBM     (Bolsa NYSE, acción IBM)")
        print("  4. forex.EUR.USD      (Mercado Forex - sin coincidencias de stock)")
        print("Escribí /salir para terminar.\n")

        while True:
            try:
                routing_key = input("Routing key (ej. stock.NYSE.AAPL): ").strip()
                if routing_key.lower() == "/salir":
                    break
                if not routing_key:
                    continue

                mensaje = input("Mensaje (ej. AAPL sube 1.5%): ").strip()
                if not mensaje:
                    mensaje = f"Cotización actualizada para {routing_key}"

                publicar_evento(canal, routing_key, mensaje)
                print("-" * 50)
            except KeyboardInterrupt:
                print("\nSaliendo...")
                break

    conexion.close()

if __name__ == "__main__":
    main()
