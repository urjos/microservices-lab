# Authentication Service (`auth-service`)

Este microservicio es el responsable central de la gestión de la identidad y la autenticación de usuarios en la plataforma.

## Propósito Principal

Su única responsabilidad es manejar el ciclo de vida de la autenticación del usuario:

- Registro de nuevos usuarios.
- Inicio de sesión (autenticación).
- Emisión, validación y refresco de JSON Web Tokens (JWT).
- Gestión básica del perfil de usuario.

## Funcionalidades Clave

- **Registro de Usuario:** Permite a nuevos usuarios crear una cuenta.
- **Autenticación por Credenciales:** Valida el email y la contraseña de un usuario.
- **Emisión de Tokens JWT:** Genera un `access_token` de corta duración y un `refresh_token` de larga duración tras un login exitoso.
- **Refresco de Tokens:** Permite obtener un nuevo `access_token` usando un `refresh_token` válido.

---

## API Endpoints

Todos los endpoints están prefijados con `/api/auth`.

| Endpoint         | Método  | Descripción                                              | Requiere Auth | Payload de Ejemplo                                 |
| :--------------- | :------ | :------------------------------------------------------- | :------------ | :------------------------------------------------- |
| `/register`      | `POST`  | Registra un nuevo usuario en el sistema.                 | No            | `{"email": "user@example.com", "password": "..."}` |
| `/login`         | `POST`  | Autentica a un usuario y devuelve los tokens JWT.        | No            | `{"email": "user@example.com", "password": "..."}` |
| `/token/refresh` | `POST`  | Refresca un `access_token` usando un `refresh_token`.    | No            | `{"refresh": "ey..."}`                             |
| `/profile`       | `GET`   | Obtiene los datos del perfil del usuario autenticado.    | Sí            | N/A                                                |
| `/profile`       | `PATCH` | Actualiza parcialmente los datos del perfil del usuario. | Sí            | `{"first_name": "John", "last_name": "Doe"}`       |

---

## Modelo de Datos (PostgreSQL)

Este servicio gestiona una única tabla principal: `auth_user`.

- **`CustomUser` Model:**
  - `id` (UUID, Primary Key)
  - `email` (string, unique)
  - `password` (string, hashed)
  - `first_name` (string)
  - `last_name` (string)
  - `is_active`, `is_staff`, `is_superuser` (boolean)
  - `date_joined`, `last_login` (datetime)

---

## Integración con Kafka (Eventos)

Este servicio actúa como **Productor** de eventos relacionados con el usuario.

### Eventos Publicados

- **Topic:** `user_events`
  - **Evento:** `user.created`
  - **Descripción:** Se publica inmediatamente después de que un nuevo usuario se registra exitosamente. Es utilizado por otros servicios para inicializar datos relacionados con el nuevo usuario (ej. `notifications_service` para enviar un email de bienvenida).
  - **Payload:**
    ```json
    {
      "event_type": "user.created",
      "data": {
        "user_id": "c3a2b1f0-...",
        "email": "new.user@example.com",
        "timestamp": "2023-10-27T10:00:00Z"
      }
    }
    ```

---

## Variables de Entorno

Para ejecutar este servicio, es necesario configurar las siguientes variables en un archivo `.env` dentro de este directorio.

| Variable                            | Descripción                                           | Ejemplo                                            |
| :---------------------------------- | :---------------------------------------------------- | :------------------------------------------------- |
| `SECRET_KEY`                        | Clave secreta de Django para seguridad criptográfica. | `django-insecure-xyz...`                           |
| `DEBUG`                             | Activa el modo debug de Django. (`1` o `0`)           | `1`                                                |
| `DB_NAME`                           | Nombre de la base de datos PostgreSQL.                | `auth_db`                                          |
| `DB_USER`                           | Usuario para la conexión a la base de datos.          | `auth_user`                                        |
| `DB_PASSWORD`                       | Contraseña para la conexión a la base de datos.       | `supersecretpassword`                              |
| `DB_HOST`                           | Host donde se ejecuta la base de datos.               | `auth_db_postgres` (nombre del servicio en Docker) |
| `DB_PORT`                           | Puerto de la base de datos.                           | `5432`                                             |
| `KAFKA_BOOTSTRAP_SERVERS`           | URL del broker de Kafka.                              | `kafka:9092`                                       |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | Duración del token de acceso en minutos.              | `5`                                                |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS`   | Duración del token de refresco en días.               | `1`                                                |

---

## Desarrollo y Pruebas Locales

Para ejecutar comandos específicos de Django dentro del contenedor de este servicio:

```bash
# Aplicar migraciones de la base de datos
docker-compose exec auth-service python manage.py migrate

# Crear un superusuario
docker-compose exec auth-service python manage.py createsuperuser

# Ejecutar los tests del servicio
docker-compose exec auth-service python manage.py test
```
