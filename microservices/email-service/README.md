# Email Service (`email-service`)

Este microservicio es un "worker" dedicado exclusivamente al envío de correos electrónicos transaccionales de la plataforma.

## Propósito Principal

La responsabilidad de este servicio es centralizar y gestionar todas las comunicaciones salientes por correo electrónico. Actúa como un servicio de utilidad que es invocado de forma asíncrona, desacoplando la lógica de negocio de la entrega de correos.

**Este servicio no expone ninguna API REST pública.**

## Arquitectura y Funcionamiento

El `email-service` opera como un consumidor de eventos de Kafka. Se suscribe a varios topics y, cuando recibe un mensaje relevante, utiliza la información del payload para renderizar una plantilla de correo y enviarla al destinatario correspondiente a través de un servidor SMTP.

---

## Integración con Kafka (Eventos Consumidos)

Este servicio actúa únicamente como **Consumidor** de eventos.

| Topic          | Evento                | Acción Realizada                                              | Payload Esperado                                                         |
| :------------- | :-------------------- | :------------------------------------------------------------ | :----------------------------------------------------------------------- |
| `user_events`  | `user.created`        | Envía un correo de bienvenida al nuevo usuario.               | `{"email": "...", "name": "..."}`                                        |
| `user_events`  | `user.password_reset` | Envía un correo con el enlace para restablecer la contraseña. | `{"email": "...", "reset_link": "..."}`                                  |
| `order_events` | `order.confirmed`     | Envía una confirmación de pedido al cliente.                  | `{"email": "...", "order_id": "...", "total": "..."}`                    |
| `blog_events`  | `blog.post.published` | Envía una notificación a los suscriptores del blog.           | `{"subscriber_emails": ["..."], "post_title": "...", "post_url": "..."}` |

_(Nota: Los payloads son ejemplos simplificados. Deben contener toda la información necesaria para renderizar la plantilla de correo.)_

---

## Gestión de Plantillas (Templates)

Las plantillas de correo electrónico se encuentran en el directorio `email_service/templates/emails/`. Son archivos HTML que utilizan el sistema de plantillas de Django.

- `welcome.html`: Plantilla para el correo de bienvenida.
- `order_confirmation.html`: Plantilla para la confirmación de pedido.

Para añadir una nueva plantilla, simplemente crea un nuevo archivo HTML en este directorio y actualiza la lógica del consumidor de Kafka para que la utilice con el evento correspondiente.

---

## Variables de Entorno

Para ejecutar este servicio, es necesario configurar las siguientes variables en un archivo `.env`.

| Variable                  | Descripción                                                           | Ejemplo                                       |
| :------------------------ | :-------------------------------------------------------------------- | :-------------------------------------------- |
| `SECRET_KEY`              | Clave secreta de Django (requerida, aunque no se use intensivamente). | `django-insecure-xyz...`                      |
| `DEBUG`                   | Activa el modo debug de Django. (`1` o `0`)                           | `0`                                           |
| `KAFKA_BOOTSTRAP_SERVERS` | URL del broker de Kafka.                                              | `kafka:9092`                                  |
| `EMAIL_BACKEND`           | Backend de correo de Django.                                          | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST`              | Host del servidor SMTP.                                               | `smtp.mailgun.org`                            |
| `EMAIL_PORT`              | Puerto del servidor SMTP.                                             | `587`                                         |
| `EMAIL_HOST_USER`         | Nombre de usuario para la autenticación SMTP.                         | `postmaster@example.com`                      |
| `EMAIL_HOST_PASSWORD`     | Contraseña para la autenticación SMTP.                                | `supersecretpassword`                         |
| `EMAIL_USE_TLS`           | Indica si se debe usar una conexión TLS. (`True` o `False`)           | `True`                                        |
| `DEFAULT_FROM_EMAIL`      | Dirección de correo electrónico del remitente por defecto.            | `noreply@example.com`                         |

---

## Desarrollo y Pruebas Locales

### Backend de Correo para Desarrollo

Para evitar el envío de correos reales durante el desarrollo, se recomienda cambiar el `EMAIL_BACKEND` en tu archivo `.env` local a:

```
# Imprime el contenido del correo en la consola donde se ejecuta el servicio
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Alternativamente, puedes usar un servidor SMTP local como MailHog, que captura todos los correos enviados y los muestra en una interfaz web.

### Probar el envío manualmente

Puedes usar el shell de Django para probar el envío de un correo:

```bash
# Acceder al shell del servicio
docker-compose exec email-service python manage.py shell

# Dentro del shell de Python
from django.core.mail import send_mail
send_mail(
    'Asunto de prueba',
    'Este es un mensaje de prueba.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

---

## Estado y Persistencia

Este servicio es **stateless** (sin estado) y no requiere una base de datos. Su escalabilidad se logra simplemente ejecutando más instancias del contenedor.
