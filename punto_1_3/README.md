# Punto 1.3: Workers y Competing Consumers (Fair Dispatch)

En este ejercicio se implementa el patrón **Competing Consumers** (Consumidores Competitivos):
- Múltiples workers escuchan la **misma cola** (`cola_trabajo_competitivo`).
- Cada tarea la procesa **un único worker** (distribución de carga 1-a-1).
- Se utiliza **Fair Dispatch** (`basic_qos(prefetch_count=1)`) y **ACK manual** para que ningún worker acapare tareas mientras otro está libre.

---

## Cómo ejecutar y probar

Abrí varias terminales (con el entorno `.venv` activado):

### 1. Terminal 1 — Worker 1
```powershell
python punto_1_3\worker.py Worker-1
```

### 2. Terminal 2 — Worker 2
```powershell
python punto_1_3\worker.py Worker-2
```

### 3. Terminal 3 (Opcional) — Worker 3
```powershell
python punto_1_3\worker.py Worker-3
```

---

### 4. Terminal 4 — Productor
Encolá el lote de tareas de prueba:
```powershell
python punto_1_3\productor.py
```

O encolá una tarea personalizada con cierta cantidad de puntos (`.`):
```powershell
python punto_1_3\productor.py "Procesar imagen en alta resolución....."
```

---

## Observaciones a verificar en la prueba

1. **Cada tarea la toma un solo worker:**
   Una tarea que entra a la cola es entregada exclusivamente al primer worker disponible. Los demás no la reciben ni la duplican.

2. **Fair Dispatch (`prefetch = 1`):**
   Si el `Worker-1` recibe una tarea pesada de 5 segundos (`.....`), RabbitMQ **no** le envía más tareas hasta que haga ACK. Durante esos 5 segundos, las siguientes tareas se despachan al `Worker-2` o `Worker-3` que están desocupados.

3. **Capacidad y tiempo total:**
   - Con **1 solo worker**, el lote de 18 segundos de trabajo tarda **~18 segundos** (secuencial).
   - Con **2 workers**, se procesa en paralelo en aproximadamente **~9-10 segundos**.
   - Con **3 workers**, se reduce aún más a **~6-7 segundos**.
    Agregar workers aumenta la capacidad de procesamiento del sistema y reduce el tiempo total de vaciado de la cola.

---

## Consigna:

> **¿Qué pasa con una tarea si el worker se cae antes de hacer ack?**

Gracias a que usamos **ACK manual** (`auto_ack=False`), el mensaje permanece en RabbitMQ en estado `Unacknowledged` mientras el worker lo procesa. Básicamente, RabbitMQ no sabe si el trabajador la procesó o no, por lo que la deja en la cola hasta que el trabajador le diga que ya la procesó.

Si el worker se interrumpe o se cae (cierre de proceso, corte de luz, excepción no capturada, pérdida de conexión de red):
1. RabbitMQ detecta que el canal o socket TCP del worker se cerró (o venció el timeout de heartbeat).
2. Como el worker **nunca envió el ACK**, RabbitMQ **reencola la tarea automáticamente** (`requeue`).
3. La tarea vuelve a estar disponible inmediatamente al inicio de la cola para que **otro worker activo la tome y la termine**.
4. **Ningún mensaje se pierde.**
