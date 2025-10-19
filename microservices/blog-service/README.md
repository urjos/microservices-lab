# Blog Service (`blog-service`)

Este microservicio es responsable de toda la lógica y la gestión de datos relacionados con el contenido del blog, incluyendo artículos, categorías y comentarios.

## Propósito Principal

Su responsabilidad se centra en el ciclo de vida del contenido del blog:

- Creación y gestión de artículos (posts).
- Organización de artículos en categorías.
- Gestión de comentarios en los artículos.
- Exposición de una API pública para leer el contenido del blog.

## Funcionalidades Clave

- **CRUD de Artículos:** Permite a los administradores o autores crear, leer, actualizar y eliminar artículos.
- **Gestión de Categorías:** Permite crear y asignar categorías a los artículos.
- **Sistema de Comentarios:** Permite a los usuarios comentar en los artículos y a los moderadores gestionarlos.
- **Publicación:** Maneja el estado de los artículos (borrador, publicado, archivado).

---

## API Endpoints

Todos los endpoints están prefijados con `/api/blog`.

| Endpoint                    | Método      | Descripción                                          | Requiere Auth |
| :-------------------------- | :---------- | :--------------------------------------------------- | :------------ |
| `/posts`                    | `GET`       | Obtiene una lista paginada de artículos publicados.  | No            |
| `/posts`                    | `POST`      | Crea un nuevo artículo (por defecto, como borrador). | Sí (Autor)    |
| `/posts/{post_id}`          | `GET`       | Obtiene los detalles de un artículo específico.      | No            |
| `/posts/{post_id}`          | `PUT/PATCH` | Actualiza un artículo existente.                     | Sí (Autor)    |
| `/posts/{post_id}`          | `DELETE`    | Elimina un artículo.                                 | Sí (Autor)    |
| `/posts/{post_id}/comments` | `GET`       | Obtiene los comentarios de un artículo.              | No            |
| `/posts/{post_id}/comments` | `POST`      | Añade un nuevo comentario a un artículo.             | Sí (Usuario)  |
| `/categories`               | `GET`       | Obtiene una lista de todas las categorías.           | No            |

---

## Modelo de Datos (PostgreSQL)

Este servicio gestiona las siguientes tablas principales:

- **`Post` Model:**

  - `id` (UUID, Primary Key)
  - `title` (string)
  - `slug` (string, unique)
  - `content` (text)
  - `author_id` (UUID, Foreign Key conceptual al `user` del `auth-service`)
  - `status` (string, ej: 'draft', 'published')
  - `created_at`, `updated_at`, `published_at` (datetime)

- **`Category` Model:**

  - `id` (UUID, Primary Key)
  - `name` (string, unique)
  - `slug` (string, unique)

- **`Comment` Model:**
  - `id` (UUID, Primary Key)
  - `post` (Foreign Key al modelo `Post`)
  - `author_id` (UUID, Foreign Key conceptual al `user` del `auth-service`)
  - `content` (text)
  - `created_at` (datetime)

---

## Integración con Kafka (Eventos)

Este servicio actúa como **Productor** y **Consumidor** de eventos.

### Eventos Publicados

- **Topic:** `blog_events`
  - **Evento:** `blog.post.published`
  - **Descripción:** Se publica cuando un artículo cambia su estado a "publicado". Puede ser consumido por `notifications-service` para notificar a los suscriptores.
  - **Payload:** `{"event_type": "blog.post.published", "data": {"post_id": "...", "title": "...", "author_id": "..."}}`

### Eventos Consumidos

- **Topic:** `user_events`
  - **Evento:** `user.deleted`
  - **Descripción:** Escucha este evento para anonimizar o eliminar el contenido (artículos, comentarios) asociado a un usuario que ha sido eliminado del sistema.

---

## Variables de Entorno

Para ejecutar este servicio, es necesario configurar las siguientes variables en un archivo `.env`.

| Variable                  | Descripción                                     | Ejemplo                  |
| :------------------------ | :---------------------------------------------- | :----------------------- |
| `SECRET_KEY`              | Clave secreta de Django.                        | `django-insecure-abc...` |
| `DEBUG`                   | Activa el modo debug de Django. (`1` o `0`)     | `1`                      |
| `DB_NAME`                 | Nombre de la base de datos PostgreSQL.          | `blog_db`                |
| `DB_USER`                 | Usuario para la conexión a la base de datos.    | `blog_user`              |
| `DB_PASSWORD`             | Contraseña para la conexión a la base de datos. | `supersecretpassword`    |
| `DB_HOST`                 | Host donde se ejecuta la base de datos.         | `blog_db_postgres`       |
| `DB_PORT`                 | Puerto de la base de datos.                     | `5432`                   |
| `KAFKA_BOOTSTRAP_SERVERS` | URL del broker de Kafka.                        | `kafka:9092`             |

---

## Desarrollo y Pruebas Locales

Para ejecutar comandos específicos de Django dentro del contenedor de este servicio:

```bash
# Aplicar migraciones de la base de datos
docker-compose exec blog-service python manage.py migrate

# Ejecutar los tests del servicio
docker-compose exec blog-service python manage.py test
```
