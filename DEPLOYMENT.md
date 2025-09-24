# Guía de Publicación del Sistema Buffet

Esta guía paso a paso te ayudará a publicar el Sistema de Buffet Escolar en un servidor de producción.

## Opción 1: Despliegue Rápido con Docker (Recomendado)

### Prerrequisitos
- Docker y Docker Compose instalados
- Clonar el repositorio

### Pasos
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/dtermite/Buffet.git
   cd Buffet
   ```

2. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Iniciar la aplicación:**
   ```bash
   docker-compose up -d
   ```

4. **Crear superusuario:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Acceder al sistema:**
   - Aplicación: http://localhost
   - Admin: http://localhost/admin

## Opción 2: Despliegue Manual en Servidor Linux

### Prerrequisitos
- Ubuntu/Debian/CentOS con Python 3.8+
- MySQL Server
- Nginx (opcional pero recomendado)

### Pasos Detallados

1. **Preparar el servidor:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3-pip python3-venv mysql-server nginx
   
   # CentOS/RHEL
   sudo yum install python3-pip mysql-server nginx
   ```

2. **Configurar MySQL:**
   ```bash
   sudo mysql_secure_installation
   sudo mysql -u root -p
   ```
   ```sql
   CREATE DATABASE buffet_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'buffet_user'@'localhost' IDENTIFIED BY 'tu_password_segura';
   GRANT ALL PRIVILEGES ON buffet_db.* TO 'buffet_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

3. **Configurar la aplicación:**
   ```bash
   # Crear usuario para la aplicación
   sudo useradd --system --shell /bin/bash --home /opt/buffet buffet
   
   # Crear directorios
   sudo mkdir -p /opt/buffet
   sudo chown buffet:buffet /opt/buffet
   
   # Cambiar al usuario buffet
   sudo -u buffet -H bash
   cd /opt/buffet
   
   # Clonar repositorio
   git clone https://github.com/dtermite/Buffet.git .
   
   # Crear entorno virtual
   python3 -m venv venv
   source venv/bin/activate
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar con tu configuración
   nano .env
   ```

5. **Configurar Django:**
   ```bash
   # Ejecutar script de despliegue
   ./deploy.sh
   
   # O manualmente:
   python manage.py migrate --settings=buffet_app.settings_production
   python manage.py collectstatic --noinput --settings=buffet_app.settings_production
   python manage.py createsuperuser --settings=buffet_app.settings_production
   ```

6. **Configurar servicio systemd:**
   ```bash
   # Salir del usuario buffet
   exit
   
   # Copiar archivo de servicio
   sudo cp /opt/buffet/buffet.service /etc/systemd/system/
   
   # Habilitar y iniciar servicio
   sudo systemctl daemon-reload
   sudo systemctl enable buffet
   sudo systemctl start buffet
   sudo systemctl status buffet
   ```

7. **Configurar Nginx:**
   ```bash
   sudo cp /opt/buffet/nginx.conf /etc/nginx/sites-available/buffet
   sudo ln -s /etc/nginx/sites-available/buffet /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   sudo nginx -t
   sudo systemctl reload nginx
   ```

## Opción 3: Despliegue en Servicios Cloud

### Heroku

1. **Crear archivos adicionales para Heroku:**
   ```bash
   # Procfile
   echo "web: gunicorn buffet_app.wsgi:application --bind 0.0.0.0:\$PORT" > Procfile
   
   # runtime.txt
   echo "python-3.12.3" > runtime.txt
   ```

2. **Configurar Heroku:**
   ```bash
   heroku create tu-app-buffet
   heroku config:set DJANGO_SETTINGS_MODULE=buffet_app.settings_production
   heroku config:set SECRET_KEY="tu-clave-secreta-muy-larga"
   heroku config:set DEBUG=False
   
   # Configurar base de datos (usar ClearDB MySQL)
   heroku addons:create cleardb:ignite
   heroku config:get CLEARDB_DATABASE_URL
   # Configurar DB_* variables basado en la URL obtenida
   
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

### DigitalOcean/AWS/Google Cloud

Similar al despliegue manual, pero usando sus servicios de base de datos manejados:
- **DigitalOcean:** App Platform + Managed Databases
- **AWS:** Elastic Beanstalk + RDS
- **Google Cloud:** App Engine + Cloud SQL

## Configuraciones Post-Despliegue

### 1. Configurar HTTPS (Recomendado)

```bash
# Con Let's Encrypt (Certbot)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com
```

### 2. Configurar Datos Iniciales

Accede a `http://tu-dominio.com/admin` y configura:

1. **Grados:** 1°A, 1°B, 2°A, 2°B, etc.
2. **Formas de pago:** Efectivo, Transferencia, Mercado Pago, etc.
3. **Parámetros:** Mensaje base para WhatsApp
4. **Alumnos:** Registra los alumnos con sus datos de WhatsApp

### 3. Configurar Backup Automático

```bash
# Crear script de backup
sudo nano /opt/buffet/backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u buffet_user -p'tu_password' buffet_db > /opt/buffet/backups/backup_$DATE.sql
find /opt/buffet/backups/ -name "backup_*.sql" -mtime +7 -delete
```

```bash
# Hacer ejecutable
sudo chmod +x /opt/buffet/backup.sh

# Agregar a crontab (backup diario a las 2 AM)
sudo crontab -e
# Agregar línea:
0 2 * * * /opt/buffet/backup.sh
```

### 4. Monitoreo

```bash
# Ver logs de la aplicación
sudo journalctl -f -u buffet

# Ver estado de servicios
sudo systemctl status buffet nginx mysql

# Monitorear uso de recursos
htop
df -h
```

## Solución de Problemas Comunes

### Error 500 - Internal Server Error
```bash
# Verificar logs
sudo journalctl -f -u buffet
# Verificar configuración
sudo nginx -t
```

### Error de conexión a base de datos
```bash
# Verificar configuración .env
cat /opt/buffet/.env
# Probar conexión manualmente
mysql -u buffet_user -p buffet_db
```

### Archivos estáticos no cargan
```bash
# Recolectar archivos estáticos
cd /opt/buffet
source venv/bin/activate
python manage.py collectstatic --clear --noinput
```

### Problemas con permisos
```bash
# Ajustar permisos
sudo chown -R buffet:buffet /opt/buffet
sudo chmod -R 755 /opt/buffet
```

## Mantenimiento

### Actualizaciones
```bash
cd /opt/buffet
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --settings=buffet_app.settings_production
python manage.py collectstatic --noinput --settings=buffet_app.settings_production
sudo systemctl restart buffet
```

### Limpieza
```bash
# Limpiar logs antiguos
sudo journalctl --vacuum-time=30d

# Limpiar archivos temporales de Django
python manage.py clearsessions
```

## Seguridad

- ✅ Cambiar SECRET_KEY para producción
- ✅ Usar DEBUG=False
- ✅ Configurar ALLOWED_HOSTS correctamente
- ✅ Usar HTTPS
- ✅ Mantener Django y dependencias actualizadas
- ✅ Configurar firewall (UFW/iptables)
- ✅ Cambiar contraseñas por defecto
- ✅ Configurar backups regulares

¡El sistema ya está listo para usar en producción! 🎉