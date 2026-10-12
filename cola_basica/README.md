## conexion.py	--> Lee el .env y conecta con RabbitMQ.
## enviar.py	--> pide tareas por teclado y las publica en la cola tareas_basicas de RabbitMQ
## worker.py	--> recibe tareas de esa cola, simula su procesamiento y confirma cuando termina.
## .env	        --> Configuración de sdist0, sdist1, sdist2 guarda nombre, host, puerto y credenciales.
## .gitignore	--> Excluye .env, entornos y cachés del repositorio.
## .venv/	    --> Entorno Python en sdist0 y sdist1.
## docker-compose.yml   -->	Define el contenedor RabbitMQ.

NOMBRE=Productor
RABBIT_HOST=localhost
RABBIT_PORT=5672
RABBIT_USER=tpuser
RABBIT_PASS=tppass

NOMBRE=Worker-sdist1
RABBIT_HOST=10.0.2.1
RABBIT_PORT=5672
RABBIT_USER=tpuser
RABBIT_PASS=tppass

### Instalar python3-venv.
### Instalar pika y python-dotenv usando el Python de ese entorno.
### Crear el .env correspondiente a cada VM.

### Levantar RabbitMQ únicamente en sdist0. 
#### docker compose up -d
#### docker ps -a --filter name=rabbit-tp
#### docker start rabbit-tp
#### docker stop rabbit-tp