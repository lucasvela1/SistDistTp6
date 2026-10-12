# Punto 1.2: Pub/Sub con Topic Exchange

Este ejercicio implementa un patrón **Publicador/Suscriptor (1-a-N)** utilizando un Exchange de tipo `topic` en RabbitMQ y routing keys jerárquicas delimitadas por puntos.

## Estructura de Claves (Routing Keys)
El formato utilizado es: `stock.<MERCADO>.<SIMBOLO>`
- Ejemplos: `stock.NYSE.AAPL`, `stock.NASDAQ.MSFT`, `stock.NYSE.IBM`

## Suscriptores pedidos en la consigna
1. **Suscriptor 1 (`stock.NYSE.*`)**: recibe cualquier acción pero **solo** del mercado NYSE.
2. **Suscriptor 2 (`stock.#`)**: recibe **todo** lo que pertenezca a `stock`, sin importar el mercado ni la acción.
3. **Suscriptor 3 (`stock.*.AAPL`)**: recibe **solo** la acción `AAPL`, de cualquier mercado (NYSE, NASDAQ, etc.).

---

## Cómo ejecutar la prueba 1-a-N

Abrí 4 terminales (con el entorno `.venv` activado):

### 1. Terminal 1 (Suscriptor NYSE)
```powershell
python subscriber.py "stock.NYSE.*"
```

### 2. Terminal 2 (Suscriptor Todo Stock)
```powershell
python subscriber.py "stock.#"
```

### 3. Terminal 3 (Suscriptor Solo AAPL)
```powershell
python subscriber.py "stock.*.AAPL"
```

### 4. Terminal 4 (Publicador)
Podés ejecutarlo pasando los parámetros directamente o en modo interactivo ejecutando `python publisher.py`:

* **Prueba A: `stock.NYSE.AAPL`**
  ```powershell
  python publisher.py stock.NYSE.AAPL "AAPL en NYSE a 180 USD"
  ```
  👉 **Llega a los 3 suscriptores** (coincide con `stock.NYSE.*`, `stock.#` y `stock.*.AAPL`).

* **Prueba B: `stock.NASDAQ.MSFT`**
  ```powershell
  python publisher.py stock.NASDAQ.MSFT "MSFT en NASDAQ a 420 USD"
  ```
  👉 **Llega únicamente al Suscriptor 2 (`stock.#`)**.

* **Prueba C: `stock.NASDAQ.AAPL`**
  ```powershell
  python publisher.py stock.NASDAQ.AAPL "AAPL en NASDAQ a 180 USD"
  ```
  👉 **Llega al Suscriptor 2 (`stock.#`) y al Suscriptor 3 (`stock.*.AAPL`)**.

---

## Pregunta teórica: ¿Qué pasa si publicás una clave que no coincide con ningún binding?

> Si publicás un evento con una routing key que no hace match con ninguna de las colas conectadas al exchange (por ejemplo: `forex.EUR.USD` o `crypto.BINANCE.BTC`), **RabbitMQ descarta el mensaje inmediatamente y de forma silenciosa** (se pierde/drop).
>
> La única forma de evitar que se descarte es:
> 1. Publicar el mensaje con el flag `mandatory=True` (RabbitMQ devolverá el mensaje al publicador mediante un evento `basic_return`).
> 2. Tener configurado un **Alternate Exchange** en el broker para capturar mensajes huérfanos.
