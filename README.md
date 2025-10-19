# Laboratorio de Microservicios con Django, React y Kafka

Este proyecto es una aplicación web moderna construida sobre una arquitectura de microservicios. Utiliza Django REST Framework para los servicios de backend, Next.js para una interfaz de usuario reactiva y Apache Kafka como bus de eventos para la comunicación asíncrona entre servicios.

## Arquitectura

La aplicación se compone de varios servicios independientes que se ejecutan en contenedores de Docker y se comunican entre sí a través de un API Gateway, llamadas REST directas y eventos de Kafka.

_(Reemplaza esta URL con un diagrama real de tu arquitectura si lo tienes)_

- **Frontend (React):** Es la puerta de entrada para los usuarios. Se comunica con los servicios de backend a través del Reverse Proxy.
- **Reverse Proxy (Nginx):** Actúa como un **API Gateway**, siendo el único punto de entrada para todo el tráfico. Enruta las peticiones al servicio interno correspondiente.
- **Microservicios (Django):** Cada servicio es responsable de una lógica de negocio específica.
- **Apache Kafka:** Actúa como el sistema nervioso central, permitiendo que los servicios se comuniquen de forma asíncrona y desacoplada.

## Stack Tecnológico

- **Frontend:** Next.js, React, Tailwind CSS
- **Backend (Microservicios):** Django, Django REST Framework
- **API Gateway:** Nginx
- **Base de Datos:** PostgreSQL
- **Caché:** Redis
- **Mensajería / Event Streaming:** Apache Kafka, Zookeeper
- **Contenerización:** Docker, Docker Compose

## Estructura del Proyecto

```
.
├── docker-compose.yml      # Orquestación de todos los servicios
├── frontend/               # Código fuente del proyecto Next.js
└── microservices/          # Contenedor de todos los servicios de backend
    ├── auth-service/       # Servicio de autenticación
    ├── blog-service/       # Servicio de gestión del blog
    ├── email-service/      # Servicio para envío de correos
    └── reverse-proxy/      # Configuración de Nginx
```

## Prerrequisitos

Asegúrate de tener instalado el siguiente software en tu sistema:

- Docker
- Docker Compose

## Instalación y Configuración

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2.  **Configura las variables de entorno:**
    Cada servicio en la carpeta `microservices/` tiene un archivo `.env.example`. Debes crear una copia de cada uno llamada `.env` y rellenar los valores.

    ```bash
    # Ejemplo para el servicio de autenticación
    cp microservices/auth-service/.env.example microservices/auth-service/.env

    # Ejemplo para el servicio de blog
    cp microservices/blog-service/.env.example microservices/blog-service/.env

    # Repite para todos los servicios que lo requieran...
    ```

    **¡Este paso es crucial!** Asegúrate de configurar las claves secretas, credenciales de base de datos y otras configuraciones sensibles.

3.  **Construye e inicia los contenedores:**
    Este comando construirá las imágenes de Docker para cada servicio y los iniciará en segundo plano.
    ```bash
    docker-compose up --build -d
    ```

## Uso

Una vez que los servicios estén en funcionamiento:

- El **Frontend** estará disponible en `http://localhost:3000`.
- Todas las **APIs de backend** son accesibles a través del Reverse Proxy en `http://localhost:80`. Por ejemplo:
  - `http://localhost/api/auth/login`
  - `http://localhost/api/blog/posts`

### Comandos útiles

- **Iniciar todos los servicios:**

  ```bash
  docker-compose up -d
  ```

- **Detener todos los servicios:**

  ```bash
  docker-compose down
  ```

- **Ver los logs de un servicio específico (ej. `auth-service`):**
  ```bash
  docker-compose logs -f auth-service
  ```

## Comunicación por Eventos (Kafka)

Los servicios se comunican de forma asíncrona utilizando los siguientes topics de Kafka:

- `user_events`:
  - **Evento:** `user.created` - Se publica cuando un nuevo usuario se registra.
  - **Productor:** `auth-service`
  - **Consumidor:** `email-service` (para enviar un email de bienvenida).
- `blog_events`:
  - **Evento:** `blog.post.published` - Se publica cuando un artículo se publica.
  - **Productor:** `blog-service`
  - **Consumidor:** `email-service` (para notificar a suscriptores).

## Licencia

Este proyecto está bajo la Licencia MIT.
