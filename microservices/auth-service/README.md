# Authentication Service (`auth-service`)

Este microservicio es el responsable central de la gestión de la identidad, autenticación y perfiles de usuario en la plataforma.

## Propósito Principal

Su responsabilidad es manejar el ciclo de vida completo del usuario:

- Registro de nuevos usuarios.
- Activación de cuentas por correo electrónico.
- Inicio de sesión (autenticación por credenciales).
- Emisión, validación y refresco de JSON Web Tokens (JWT).
- Autenticación a través de proveedores sociales (Google, Facebook).
- Gestión de perfiles de usuario (fotos, información personal, redes sociales).
- Recuperación y cambio de contraseñas.

---

## API Endpoints

Todos los endpoints están prefijados con `/auth`. La mayoría son proporcionados por la librería **Djoser**.

| Endpoint                  | Método          | Descripción                                                    | Requiere Auth |
| :------------------------ | :-------------- | :------------------------------------------------------------- | :------------ |
| `/users/`                 | `POST`          | Registra un nuevo usuario.                                     | No            |
| `/users/`                 | `GET`           | **(Custom)** Lista todos los usuarios del sistema.             | No            |
| `/users/me/`              | `GET/PUT/PATCH` | Obtiene o actualiza los datos del usuario autenticado.         | Sí            |
| `/users/{id}`             | `GET`           | **(Custom)** Obtiene los datos de un usuario por su ID.        | No            |
| `/activate/{uid}/{token}` | `GET`           | Activa la cuenta de un usuario.                                | No            |
| `/jwt/create/`            | `POST`          | Autentica a un usuario y devuelve los tokens JWT.              | No            |
| `/jwt/refresh/`           | `POST`          | Refresca un `access_token` usando un `refresh_token`.          | No            |
| `/jwt/verify/`            | `POST`          | Verifica la validez de un `access_token`.                      | No            |
| `/profile/{slug}`         | `GET`           | **(Custom)** Obtiene el perfil público de un usuario por slug. | No            |

---

## Modelo de Datos (PostgreSQL)

Este servicio gestiona dos tablas principales interconectadas: `user_useraccount` y `user_profile_profile`.

- **`UserAccount` Model:** Almacena la información de autenticación y los datos básicos.

  - `id` (UUID, Primary Key)
  - `email` (string, unique)
  - `username` (string, unique)
  - `slug` (string, unique)
  - `password` (string, hashed)
  - `first_name` (string)
  - `last_name` (string)
  - `is_active`, `is_staff`, `is_superuser`, `is_online`, `verified` (boolean)
  - `role` (string, con choices como 'customer', 'admin', etc.)

- **`Profile` Model:** Almacena información extendida y opcional del usuario. Se crea automáticamente al registrar un nuevo usuario.
  - `user` (OneToOne con `UserAccount`)
  - `picture`, `banner` (ImageField)
  - `location`, `url`, `profile_info` (string/text)
  - `birthday` (date)
  - Campos para redes sociales (`facebook`, `twitter`, `github`, etc.)

---

## Integración con Kafka (Eventos)

Este servicio está diseñado para actuar como **Productor** de eventos relacionados con el ciclo de vida del usuario.

### Eventos Publicados

- **Topic:** `user_events`
  - **Evento:** `user.created`
  - **Descripción:** Se publica inmediatamente después de que un nuevo usuario se registra exitosamente. Es utilizado por otros servicios para inicializar datos relacionados con el nuevo usuario (ej. `email-service` para enviar un email de bienvenida o `blog-service` para asociar contenido).
  - **Payload:**
    ```json
    {
      "event_type": "user.created",
      "data": {
        "id": "c3a2b1f0-...",
        "email": "new.user@example.com",
        "username": "newuser"
      }
    }
    ```
    **Nota:** La implementación de la producción de eventos está presente como código comentado en `apps/user/models.py` y debe ser activada.

---

## Variables de Entorno

Para ejecutar este servicio, es necesario configurar las siguientes variables en un archivo `.env`. La configuración se lee a través de `django-environ`.

| Variable                    | Descripción                                           | Ejemplo (del `docker-compose.yaml`) |
| :-------------------------- | :---------------------------------------------------- | :---------------------------------- |
| `SECRET_KEY`                | Clave secreta de Django para seguridad criptográfica. | `django-insecure-xyz...`            |
| `DEBUG`                     | Activa el modo debug de Django. (`True` o `False`)    | `True`                              |
| `POSTGRES_DB`               | Nombre de la base de datos PostgreSQL.                | `solopython_auth_db`                |
| `POSTGRES_USER`             | Usuario para la conexión a la base de datos.          | `postgres`                          |
| `POSTGRES_PASSWORD`         | Contraseña para la conexión a la base de datos.       | `12345678`                          |
| `REDIS_HOST`                | Host del servicio de Redis.                           | `redis`                             |
| `REDIS_PORT`                | Puerto del servicio de Redis.                         | `6379`                              |
| `ALLOWED_HOSTS_DEV`         | Lista de hosts permitidos en desarrollo.              | `localhost,127.0.0.1`               |
| `CORS_ORIGIN_WHITELIST_DEV` | Lista de orígenes permitidos para CORS en desarrollo. | `http://localhost:3000`             |

---

## Desarrollo y Pruebas Locales

Para ejecutar comandos específicos de Django dentro del contenedor de este servicio:

```bash
# Aplicar migraciones de la base de datos (se ejecuta automáticamente al iniciar)
docker-compose exec solopython_ms_auth python manage.py migrate

# Crear un superusuario
docker-compose exec solopython_ms_auth python manage.py createsuperuser

# Ejecutar los tests del servicio
docker-compose exec solopython_ms_auth python manage.py test
```
