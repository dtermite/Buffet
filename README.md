# Sistema de Buffet Escolar

Un sistema de gestión de buffet escolar desarrollado en Django que permite:

- Registrar consumos de alumnos
- Gestionar pagos
- Consultar deudas de alumnos
- Enviar notificaciones por WhatsApp sobre deudas pendientes

## Características Principales

- **Gestión de alumnos**: Registro de alumnos por grado con información de contacto WhatsApp
- **Control de consumos**: Registro detallado de consumos con fecha, hora e importe
- **Gestión de pagos**: Registro de pagos con diferentes formas de pago
- **Cuenta corriente**: Cálculo automático de saldos (consumos - pagos)
- **Notificaciones WhatsApp**: Integración para enviar recordatorios de deuda vía WhatsApp
- **Interface web responsive**: Interface moderna con Bootstrap

## Tecnologías Utilizadas

- **Backend**: Django 5.2.6
- **Base de datos**: MySQL
- **Frontend**: Bootstrap 5, HTML5
- **Integración**: WhatsApp Web API

## Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/dtermite/Buffet.git
   cd Buffet
   ```

2. **Crear entorno virtual (recomendado):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   ```
   
   Editar el archivo `.env` con tus configuraciones:
   ```env
   SECRET_KEY=tu-clave-secreta-muy-segura
   DEBUG=False
   ALLOWED_HOSTS=tu-dominio.com,localhost
   
   DB_NAME=buffet_db
   DB_USER=tu_usuario_mysql
   DB_PASSWORD=tu_password_mysql
   DB_HOST=localhost
   DB_PORT=3306
   
   EMAIL_HOST_USER=tu-email@gmail.com
   EMAIL_HOST_PASSWORD=tu-password-de-aplicacion
   ```

5. **Configurar la base de datos:**
   ```bash
   # Crear la base de datos en MySQL
   mysql -u root -p
   CREATE DATABASE buffet_db CHARACTER SET utf8;
   exit
   
   # Ejecutar migraciones
   python manage.py migrate
   ```

6. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Configurar datos iniciales:**
   ```bash
   # Recomendado: crear grados y formas de pago iniciales desde el admin
   python manage.py runserver
   # Visitar http://localhost:8000/admin para configurar datos iniciales
   ```

### Configuración para Producción

#### Opción 1: Deployment Manual

1. **Usar configuración de producción:**
   ```bash
   export DJANGO_SETTINGS_MODULE=buffet_app.settings_production
   ```

2. **Recolectar archivos estáticos:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Ejecutar con Gunicorn:**
   ```bash
   gunicorn buffet_app.wsgi:application --bind 0.0.0.0:8000
   ```

#### Opción 2: Docker (Recomendado)

1. **Construir imagen:**
   ```bash
   docker build -t buffet-app .
   ```

2. **Ejecutar contenedor:**
   ```bash
   docker run -d --name buffet \
     --env-file .env \
     -p 8000:8000 \
     buffet-app
   ```

#### Opción 3: Docker Compose

```bash
docker-compose up -d
```

### Configuración del Servidor Web (Nginx)

Ejemplo de configuración Nginx:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location /static/ {
        alias /path/to/buffet/staticfiles/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## Configuración de Email

Para la funcionalidad de recuperación de contraseña, configura una cuenta de Gmail:

1. Habilita la verificación en dos pasos en tu cuenta Gmail
2. Genera una contraseña de aplicación
3. Usa esa contraseña en `EMAIL_HOST_PASSWORD`

## Uso del Sistema

1. **Acceder al sistema:** `http://tu-dominio.com`
2. **Panel administrativo:** `http://tu-dominio.com/admin`
3. **Configurar datos iniciales:**
   - Crear grados (1°A, 2°B, etc.)
   - Crear formas de pago (Efectivo, Transferencia, etc.)
   - Registrar alumnos

4. **Flujo operativo:**
   - Registrar consumos diarios
   - Registrar pagos recibidos
   - Consultar deudas pendientes
   - Enviar recordatorios por WhatsApp

## Estructura del Proyecto

```
Buffet/
├── buffet_app/          # Configuración principal Django
│   ├── settings.py      # Configuración desarrollo
│   ├── settings_production.py  # Configuración producción
│   ├── urls.py
│   └── wsgi.py
├── core/               # Aplicación principal
│   ├── models.py       # Modelos de datos
│   ├── views.py        # Lógica de vistas
│   ├── urls.py         # URLs de la app
│   ├── forms.py        # Formularios
│   └── templates/      # Plantillas HTML
├── requirements.txt    # Dependencias Python
├── .env.example       # Ejemplo configuración
└── README.md          # Esta documentación
```

## Seguridad

- Cambia la `SECRET_KEY` en producción
- Usa `DEBUG=False` en producción
- Configura `ALLOWED_HOSTS` correctamente
- Usa HTTPS en producción
- Mantén actualizada la contraseña de la base de datos
- Usa contraseñas de aplicación para Gmail

## Resolución de Problemas

### Error de conexión a base de datos
- Verificar configuración MySQL en `.env`
- Confirmar que MySQL está ejecutándose
- Verificar permisos de usuario en MySQL

### Errores de archivos estáticos
```bash
python manage.py collectstatic --clear
```

### Problemas con migraciones
```bash
python manage.py migrate --fake-initial
```

## Mantenimiento

### Backup de base de datos
```bash
mysqldump -u usuario -p buffet_db > backup_$(date +%Y%m%d).sql
```

### Actualización del sistema
```bash
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

## Soporte

Para reportar problemas o solicitar funcionalidades, crear un issue en el repositorio de GitHub.

## Licencia

Este proyecto está desarrollado para uso educativo y administrativo escolar.