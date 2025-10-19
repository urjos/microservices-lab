# Reverse Proxy / API Gateway (`reverse-proxy`)

Este servicio actúa como el punto de entrada único (API Gateway) para todo el tráfico HTTP/HTTPS dirigido al backend. Está implementado con **Nginx**.

## Propósito Principal

Este no es un microservicio de negocio, sino un componente de infraestructura crítico. Sus responsabilidades son:

- **Enrutamiento (Routing):** Recibir todas las peticiones entrantes y redirigirlas al microservicio interno apropiado basándose en la ruta de la URL.
- **Terminación SSL:** Gestionar los certificados SSL y manejar las conexiones HTTPS. El tráfico entre el proxy y los servicios internos viaja por la red de Docker y no necesita estar encriptado.
- **Punto de Acceso Único:** Proporcionar una única dirección (`api.example.com`) para que el frontend y otros clientes consuman los servicios, simplificando la configuración y la seguridad.
- **Balanceo de Carga:** Distribuir la carga entre múltiples instancias de un mismo servicio si fuera necesario.

## Archivo de Configuración

Toda la lógica de enrutamiento se define en el archivo `nginx/default.conf`. Este archivo es montado como un volumen dentro del contenedor de Nginx.

---

## Tabla de Enrutamiento (Routing Table)

La siguiente tabla describe cómo se enrutan las peticiones entrantes:

| Ruta Pública   | Servicio Interno      | Descripción                                                           |
| :------------- | :-------------------- | :-------------------------------------------------------------------- |
| `/api/auth/`   | `auth-service:8001`   | Enruta todas las peticiones de autenticación al servicio de usuarios. |
| `/api/blog/`   | `blog-service:8002`   | Enruta las peticiones relacionadas con el contenido del blog.         |
| `/api/orders/` | `orders-service:8003` | Enruta las peticiones para la gestión de pedidos.                     |
| `/`            | `frontend:3000`       | (Opcional) Enruta el tráfico de la raíz al frontend de Next.js.       |

**Nota:** Los nombres de los servicios (`auth-service`, `blog-service`, etc.) corresponden a los nombres definidos en el archivo `docker-compose.yml`.

---

## Gestión de SSL

- **Desarrollo:** En el entorno local, el proxy escucha en el puerto `80` (HTTP).
- **Producción:** En producción, el proxy debe configurarse para escuchar en el puerto `443` (HTTPS). Los certificados SSL (ej. de Let's Encrypt) deben ser montados en el contenedor, típicamente en directorios como `/etc/letsencrypt/live/your_domain/`.

---

## Mantenimiento y Desarrollo

### Añadir una Nueva Ruta

Para enrutar el tráfico a un nuevo microservicio (ej. `new-service` en el puerto `8004`):

1.  Abre el archivo `nginx/default.conf`.
2.  Añade un nuevo bloque `location`:

    ```nginx
    location /api/new-service/ {
        proxy_pass http://new-service:8004/;
        # Añadir cabeceras estándar de proxy
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    ```

3.  Guarda el archivo y recarga la configuración de Nginx.

### Recargar la Configuración de Nginx

Después de realizar cambios en el archivo `default.conf`, no es necesario reiniciar todo el stack. Puedes recargar la configuración de Nginx sin interrumpir el servicio con el siguiente comando:

```bash
# Valida la sintaxis de la configuración antes de recargar
docker-compose exec reverse-proxy nginx -t

# Si la validación es exitosa, recarga la configuración
docker-compose exec reverse-proxy nginx -s reload
```
