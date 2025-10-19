# Microservicios con Django REST Framework, Next.js y Apache Kafka

Este proyecto es una aplicación web moderna construida sobre una arquitectura de microservicios. Utiliza Django REST Framework para los servicios de backend, Next.js para una interfaz de usuario reactiva y Apache Kafka como bus de eventos para la comunicación asíncrona entre servicios.

## Arquitectura

La aplicación se compone de varios servicios independientes que se ejecutan en contenedores de Docker y se comunican entre sí a través de eventos de Kafka y llamadas API REST.

- **Frontend (Next.js):** Es la puerta de entrada para los usuarios. Se comunica con los servicios de backend a través de una API Gateway o directamente con los microservicios correspondientes.
- **Microservicios (Django REST Framework):** Cada servicio es responsable de una lógica de negocio específica (ej: servicio de usuarios, servicio de productos, etc.). Exponen una API REST para operaciones síncronas.
- **Apache Kafka:** Actúa como el sistema nervioso central de la aplicación, permitiendo que los servicios se comuniquen de forma asíncrona y desacoplada. Por ejemplo, cuando un usuario se registra en el `servicio-de-usuarios`, este puede publicar un evento `usuario_creado` en un topic de Kafka, y otros servicios pueden reaccionar a ese evento.

## Stack Tecnológico

- **Frontend:** Next.js, React, Tailwind CSS
- **Backend (Microservicios):** Django, Django REST Framework
- **Base de Datos:** PostgreSQL, Redis (para caché)
- **Mensajería / Event Streaming:** Apache Kafka
- **Contenerización:** Docker y Docker Compose

## Prerrequisitos

Asegúrate de tener instalado el siguiente software en tu sistema:

- Docker
- Docker Compose
- Node.js (v18.x o superior)
- Python (v3.10.x o superior)

## Instalación y Configuración

Sigue estos pasos para poner en marcha el entorno de desarrollo:

1.  **Clona el repositorio:**

    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2.  **Configura las variables de entorno:**
    Habrá un archivo `.env.example` en la raíz del proyecto y/o dentro de cada carpeta de servicio. Cópialos para crear tus propios archivos `.env` y ajústalos según sea necesario.

    ```bash
    # Ejemplo para el servicio de usuarios
    cp services/user_service/.env.example services/user_service/.env
    ```

    _Asegúrate de configurar las claves de API, secretos de base de datos y otras configuraciones sensibles._

3.  **Construye e inicia los contenedores:**
    Este comando construirá las imágenes de Docker para cada servicio y los iniciará en segundo plano.
    ```bash
    docker-compose up --build -d
    ```

## Uso

- **Iniciar todos los servicios:**

  ```bash
  docker-compose up -d
  ```

- **Detener todos los servicios:**

  ```bash
  docker-compose down
  ```

- **Ver los logs de un servicio específico (ej. `users_service`):**
  ```bash
  docker-compose logs -f users_service
  ```

Una vez que los servicios estén en funcionamiento:

- El frontend estará disponible en `http://localhost:3000`.
- Las APIs de los microservicios estarán accesibles a través de los puertos definidos en `docker-compose.yml` (ej. `http://localhost:8001`, `http://localhost:8002`, etc.).

## Comunicación por Eventos (Kafka)

Los servicios se comunican de forma asíncrona utilizando los siguientes topics de Kafka:

- `user_events`:
  - **Evento:** `user.created` - Se publica cuando un nuevo usuario se registra.
  - **Productor:** `users_service`
  - **Consumidores:** `notifications_service` (para enviar un email de bienvenida).
- `order_events`:
  - **Evento:** `order.placed` - Se publica cuando se realiza un nuevo pedido.
  - **Productor:** `orders_service`
  - **Consumidores:** `products_service` (para actualizar el stock), `notifications_service` (para notificar al usuario).

_(Esta sección es un ejemplo, adáptala a tus topics y eventos reales)_

## Licencia

Este proyecto está bajo la Licencia MIT.
