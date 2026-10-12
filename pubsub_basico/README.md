## conexion.py	--> Lee el .env y conecta con RabbitMQ.
## publicar.py	--> Permite escribir y publicar avisos. sdist0
## recibir.py	--> Recibe y muestra los avisos. sdist1
## .env	        --> Configuración de sdist0, configuración de sdist1, guarda nombre, host, puerto y credenciales.
## .gitignore	--> Excluye .env, entornos y cachés del repositorio.
## venv/	    --> Entorno Python en sdist0 y sdist1.
## docker-compose.yml   -->	Define el contenedor RabbitMQ.


NOMBRE	        Emisor	        Lector
RABBIT_HOST	    localhost    	10.0.2.1
RABBIT_PORT	    5672	        5672
RABBIT_USER	    tpuser	        tpuser
RABBIT_PASS	    tppass	        tppass


### Instalar python3-venv.
### Crear el entorno local en sdist0 y en sdist1.
### Instalar pika y python-dotenv usando el Python de ese entorno.
### Crear el .env correspondiente a cada VM.


### Levantar RabbitMQ únicamente en sdist0. 
#### docker compose up -d
#### docker ps -a --filter name=rabbit-tp
#### docker start rabbit-tp
#### docker stop rabbit-tp