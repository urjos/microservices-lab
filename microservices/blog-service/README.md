# Blog Service (`blog-service`)

Este microservicio es responsable de exponer el contenido del blog (posts y categorías) con funcionalidades de paginación, búsqueda y caché.

## Propósito Principal

Su responsabilidad se centra en la exposición de datos de solo lectura del blog:

- Exponer artículos (posts) y categorías.
- Soportar paginación en la lista de posts.
- Permitir búsqueda por texto en los posts.
- Implementar caché con Redis para mejorar el rendimiento.
- Estar preparado para una futura integración con un servicio de autenticación (JWT).

---

## API Endpoints

Todos los endpoints están prefijados con `/api`.

| Endpoint            | Método | Descripción                                                                   | Caché     |
| :------------------ | :----- | :---------------------------------------------------------------------------- | :-------- |
| `/healthz`          | `GET`  | Verifica el estado de la DB y Redis.                                          | No        |
| `/api/categories`   | `GET`  | Obtiene una lista de categorías activas.                                      | Sí (120s) |
| `/api/posts`        | `GET`  | Obtiene una lista paginada de posts publicados. Acepta `?search=` y `?page=`. | No        |
| `/api/posts/{slug}` | `GET`  | Obtiene los detalles de un post por su slug.                                  | Sí (120s) |

---

## Cómo ejecutar el servicio

1.  **Asegúrate de tener Docker y Docker Compose instalados.**

2.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz de este servicio (`blog-service/`) a partir del ejemplo. Puedes simplemente copiarlo.

    ```bash
    cp .env.example .env
    ```

    Este archivo será utilizado por `docker-compose.yml` para configurar la base de datos, Redis y Django.

3.  **Construir y levantar los contenedores:**
    Desde el directorio que contiene el `docker-compose.yml` principal (probablemente la raíz de `microservices/`), ejecuta:

    ```bash
    docker-compose up --build blog
    ```

    Esto construirá la imagen del servicio de blog y levantará su contenedor junto con las dependencias (`postgres` y `redis`).

4.  **Poblar la base de datos (Seed):**
    Una vez que el contenedor esté corriendo, abre otra terminal y ejecuta el comando de `seed` para crear datos de ejemplo.

    ```bash
    docker-compose exec blog_service python manage.py seed_blog
    ```

    Esto creará 5 categorías, 3 autores y 30 posts.

5.  **Verificar que el servicio está funcionando:**
    El servicio estará disponible en `http://localhost:8001`.

---

## Ejemplos de uso con cURL

Puedes probar los endpoints usando `cURL`:

**Health Check:**

```bash
curl -i http://localhost:8001/healthz/
```

**Listar Categorías (cacheado):**

```bash
curl http://localhost:8001/api/categories/
```

**Listar Posts (primera página):**

```bash
curl http://localhost:8001/api/posts/
```

**Buscar Posts:**

```bash
curl "http://localhost:8001/api/posts/?search=development"
```

**Ver detalle de un Post (cacheado):**
(Reemplaza `un-slug-de-ejemplo` con un slug real que obtengas de la lista de posts)

```bash
curl http://localhost:8001/api/posts/un-slug-de-ejemplo/
```
