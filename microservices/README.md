# Backend Microservices

Esta carpeta contiene todos los microservicios que componen el backend de la aplicación. Cada subdirectorio representa un servicio independiente, autocontenido y desplegable, construido con **Django** y **Django REST Framework**.

## Listado de Servicios

A continuación se detalla cada servicio y su principal responsabilidad dentro del ecosistema.

- auth-service/ → Autenticación y tokens JWT
- blog-service/ → Publicaciones, autores y categorías
- email-service/ → Notificaciones y formularios
- reverse-proxy/ → Balanceo / Gateway local

## Convenciones Comunes

Para mantener la consistencia y facilitar el desarrollo, todos los servicios en este directorio deben seguir las siguientes convenciones:

1.  **Contenerización:** Cada servicio debe tener su propio `Dockerfile` para construir su imagen de Docker.
2.  **Configuración:**
    - La configuración sensible o específica del entorno se gestiona a través de variables de entorno.
    - Cada servicio debe incluir un archivo `.env.example` con todas las variables necesarias. Para ejecutarlo, se debe crear una copia llamada `.env`.
3.  **Dependencias:** Las dependencias de Python se gestionan con `pip` y se listan en un archivo `requirements.txt` en la raíz de cada servicio.
4.  **Comunicación:**
    - **Síncrona (REST API):** Cada servicio expone una API REST para operaciones de tipo solicitud-respuesta.
    - **Asíncrona (Eventos):** La comunicación desacoplada se realiza publicando y consumiendo eventos en **Apache Kafka**. Consulta el `README.md` principal del proyecto para ver el mapa de topics y eventos.

## Cómo Añadir un Nuevo Microservicio

Si necesitas añadir un nuevo servicio, sigue estos pasos:

1.  **Crear el Directorio:** Crea una nueva carpeta dentro de `services/` con un nombre descriptivo (ej: `payment_service`).
2.  **Inicializar el Proyecto:** Dentro de la nueva carpeta, crea un proyecto de Django.
3.  **Crear `Dockerfile`:** Añade un `Dockerfile` para construir la imagen del servicio.
4.  **Añadir a Docker Compose:** Agrega la definición del nuevo servicio al archivo `docker-compose.yml` principal del proyecto.
5.  **Configurar Variables de Entorno:** Crea el archivo `.env.example` con las variables necesarias.
6.  **Implementar la Lógica:** Desarrolla la lógica de negocio, las APIs y los productores/consumidores de Kafka que necesites.
