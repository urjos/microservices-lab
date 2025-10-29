# Email Service (`email-service`)

Este microservicio es responsable de gestionar y enviar notificaciones por correo electrónico, como las solicitudes de contacto recibidas.

## Propósito Principal

Su responsabilidad se centra en:

- Recibir solicitudes de contacto a través de un endpoint API.
- Persistir estas solicitudes en su propia base de datos.
- Simular el envío de correos electrónicos (configurable para envío real).
- Proporcionar un endpoint de `healthcheck` para monitorear su estado.

---

## API Endpoints

| Endpoint        | Método | Descripción                                                                 |
| :-------------- | :----- | :-------------------------------------------------------------------------- |
| `/healthz`      | `GET`  | Verifica el estado de la conexión a la base de datos y Redis.               |
| `/api/contact/` | `POST` | Recibe un formulario de contacto, lo guarda y simula el envío de un correo. |

---

## Cómo ejecutar el servicio

1.  **Asegúrate de tener Docker y Docker Compose instalados.**

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz de este servicio (`email-service/`) a partir del ejemplo.

    ```bash
    cp .env.example .env
    ```

3.  **Construir y levantar los contenedores:**
    Desde el directorio raíz del proyecto (`microservices-lab/`), ejecuta:

    ```bash
    docker-compose up --build -d email_service
    ```

    Esto construirá la imagen del servicio y levantará su contenedor junto con sus dependencias (`db_email` y `redis`).

4.  **Verificar que el servicio está funcionando:**
    El servicio estará disponible a través del Reverse Proxy en `http://localhost/api/email/`.

---

## Ejemplos de uso con cURL

**Health Check:**

```bash
curl -i http://localhost:8002/healthz/
```

**Enviar un mensaje de contacto:**

```bash
curl -X POST http://localhost:8002/api/contact/ \
-H "Content-Type: application/json" \
-d '{"name": "Ana", "email": "ana@example.com", "message": "Hola, estoy interesada en su producto."}'
```

Tras ejecutar el comando anterior, deberías ver el contenido del correo en los logs del servicio:

```bash
docker-compose logs -f email_service
```
