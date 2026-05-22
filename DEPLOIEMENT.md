# 🚀 Guide de Déploiement - Dashboard Google Ads

Ce guide détaille les étapes pour déployer l'application en production.

## 📋 Pré-requis

- Serveur Linux (Ubuntu 20.04+ recommandé) ou macOS
- Domaine configuré (ex: dashboard.votreentreprise.com)
- Certificat SSL (Let's Encrypt recommandé)
- Node.js 18+
- Python 3.13+
- Nginx ou Apache
- Base de données (optionnel pour production, SQLite par défaut)

## 🔐 1. Configuration des Credentials Google Ads

### Google Cloud Console

1. Accédez à https://console.cloud.google.com
2. Créez un nouveau projet ou sélectionnez-en un existant
3. Activez **Google Ads API**
4. Créez des **OAuth 2.0 credentials**:
   - Type: Application Web
   - Origines autorisées: `https://votredomaine.com`
   - URI de redirection: `https://votredomaine.com/api/auth/callback`

### Google Ads Developer Token

1. Accédez à votre compte Google Ads
2. Outils → Configuration → Accès API
3. Demandez un developer token (peut prendre 24-48h)

### Configuration .env

Créez `backend/.env.production`:

```bash
# Application
APP_NAME="Google Ads Dashboard"
DEBUG=False

# API
API_PREFIX=/api

# CORS
CORS_ORIGINS=https://votredomaine.com

# JWT
SECRET_KEY=générez-avec-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Google Ads API
GOOGLE_ADS_DEVELOPER_TOKEN=votre-developer-token
GOOGLE_ADS_CLIENT_ID=votre-client-id.apps.googleusercontent.com
GOOGLE_ADS_CLIENT_SECRET=votre-client-secret
GOOGLE_ADS_REDIRECT_URI=https://votredomaine.com/api/auth/callback
GOOGLE_ADS_API_VERSION=v16

# Cache
CACHE_TTL=3600

# Database (optionnel)
DATABASE_URL=postgresql://user:password@localhost/google_ads_dashboard
```

## 🏗️ 2. Build de Production

### Frontend Angular

```bash
cd frontend
npm install --production
npm run build

# Les fichiers sont dans: frontend/dist/frontend/
```

### Backend FastAPI

```bash
cd backend
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Serveur WSGI pour production
```

## 🌐 3. Configuration Nginx

Créez `/etc/nginx/sites-available/google-ads-dashboard`:

```nginx
# Redirection HTTP → HTTPS
server {
    listen 80;
    server_name votredomaine.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS
server {
    listen 443 ssl http2;
    server_name votredomaine.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/votredomaine.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/votredomaine.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Frontend (Angular)
    root /var/www/google-ads-dashboard/frontend/dist/frontend;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API (FastAPI)
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (si nécessaire)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # API Docs (désactiver en production si besoin)
    location /docs {
        proxy_pass http://127.0.0.1:8000/docs;
        proxy_set_header Host $host;
    }

    # Cache statique
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Logs
    access_log /var/log/nginx/google-ads-dashboard-access.log;
    error_log /var/log/nginx/google-ads-dashboard-error.log;
}
```

Activez le site:

```bash
sudo ln -s /etc/nginx/sites-available/google-ads-dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔄 4. Configuration Systemd (Backend)

Créez `/etc/systemd/system/google-ads-backend.service`:

```ini
[Unit]
Description=Google Ads Dashboard Backend (FastAPI)
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/google-ads-dashboard/backend
Environment="PATH=/var/www/google-ads-dashboard/backend/venv/bin"
Environment="ENV_FILE=/var/www/google-ads-dashboard/backend/.env.production"

ExecStart=/var/www/google-ads-dashboard/backend/venv/bin/gunicorn \
    -c gunicorn_config.py \
    app.main:app

Restart=always
RestartSec=10

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/var/www/google-ads-dashboard/backend/data
ReadWritePaths=/var/www/google-ads-dashboard/backend/.credentials

[Install]
WantedBy=multi-user.target
```

Créez `backend/gunicorn_config.py`:

```python
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 60
keepalive = 5

# Logging
accesslog = "/var/log/google-ads-dashboard/access.log"
errorlog = "/var/log/google-ads-dashboard/error.log"
loglevel = "info"

# Process naming
proc_name = "google-ads-backend"

# Server mechanics
daemon = False
pidfile = "/var/run/google-ads-backend.pid"
user = "www-data"
group = "www-data"
```

Démarrez le service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable google-ads-backend
sudo systemctl start google-ads-backend
sudo systemctl status google-ads-backend
```

## 🔒 5. Certificat SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votredomaine.com
sudo certbot renew --dry-run  # Test renouvellement automatique
```

## 📦 6. Déploiement des fichiers

```bash
# Créer répertoires
sudo mkdir -p /var/www/google-ads-dashboard
sudo mkdir -p /var/log/google-ads-dashboard
sudo chown -R www-data:www-data /var/www/google-ads-dashboard
sudo chown -R www-data:www-data /var/log/google-ads-dashboard

# Copier les fichiers
sudo cp -r frontend/dist/frontend /var/www/google-ads-dashboard/frontend
sudo cp -r backend /var/www/google-ads-dashboard/backend

# Permissions
sudo chown -R www-data:www-data /var/www/google-ads-dashboard
```

## 🐳 7. Alternative: Déploiement Docker

Créez `docker-compose.production.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    environment:
      - ENV_FILE=/app/.env.production
    volumes:
      - ./backend/.env.production:/app/.env.production:ro
      - ./backend/data:/app/data
      - ./backend/.credentials:/app/.credentials
    ports:
      - "8000:8000"
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - backend
    restart: always

  # Optionnel: Base de données PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: google_ads_dashboard
      POSTGRES_USER: dashboard_user
      POSTGRES_PASSWORD: changeme
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

Créez `backend/Dockerfile.prod`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Code application
COPY . .

# User non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "-c", "gunicorn_config.py", "app.main:app"]
```

Créez `frontend/Dockerfile.prod`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist/frontend /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
```

Déployez avec Docker:

```bash
docker-compose -f docker-compose.production.yml up -d
```

## 📊 8. Monitoring et Logs

### Logs Backend

```bash
# Systemd
sudo journalctl -u google-ads-backend -f

# Fichiers
tail -f /var/log/google-ads-dashboard/access.log
tail -f /var/log/google-ads-dashboard/error.log
```

### Logs Frontend/Nginx

```bash
tail -f /var/log/nginx/google-ads-dashboard-access.log
tail -f /var/log/nginx/google-ads-dashboard-error.log
```

### Monitoring avec Prometheus (optionnel)

Ajoutez au backend `app/main.py`:

```python
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
```

## 🔄 9. Mise à jour de l'application

Script de déploiement `deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Déploiement de la nouvelle version..."

# Backend
cd backend
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart google-ads-backend

# Frontend
cd ../frontend
git pull origin main
npm install
npm run build
sudo rsync -av --delete dist/frontend/ /var/www/google-ads-dashboard/frontend/

# Reload Nginx
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Déploiement terminé !"
```

## 🔐 10. Sécurité

### Checklist de sécurité

- [ ] Certificat SSL/TLS configuré
- [ ] Headers de sécurité HTTP
- [ ] SECRET_KEY unique et sécurisé
- [ ] DEBUG=False en production
- [ ] Credentials Google Ads sécurisés
- [ ] Firewall configuré (UFW, iptables)
- [ ] Mises à jour système régulières
- [ ] Backups automatiques
- [ ] Monitoring actif
- [ ] Rate limiting sur l'API
- [ ] CORS restreint au domaine
- [ ] Logs rotatifs configurés

### Configuration Firewall (UFW)

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

## 💾 11. Backups

Script de backup `backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/google-ads-dashboard"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Database
pg_dump google_ads_dashboard > $BACKUP_DIR/db_$DATE.sql

# Credentials
tar -czf $BACKUP_DIR/credentials_$DATE.tar.gz backend/.credentials

# Data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz backend/data

# Rotation (garder 7 jours)
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "✅ Backup créé: $DATE"
```

Cron quotidien:

```bash
0 2 * * * /var/www/google-ads-dashboard/backup.sh
```

## 📈 12. Performance

### Optimisations recommandées

1. **CDN**: Utilisez CloudFlare ou AWS CloudFront
2. **Compression**: Gzip/Brotli activé dans Nginx
3. **Cache**: Redis pour le cache backend
4. **Database**: PostgreSQL en production (vs SQLite)
5. **Workers**: Ajustez le nombre de workers Gunicorn
6. **Monitoring**: New Relic, DataDog, ou Grafana

### Configuration Redis (cache)

```bash
sudo apt install redis-server
```

Mise à jour `backend/requirements.txt`:

```
redis==5.0.1
```

## ✅ 13. Vérification Post-Déploiement

```bash
# Backend API
curl https://votredomaine.com/api/health

# Frontend
curl https://votredomaine.com

# SSL
curl -I https://votredomaine.com | grep -i strict

# Status services
sudo systemctl status google-ads-backend
sudo systemctl status nginx
```

## 🆘 14. Troubleshooting

### Backend ne démarre pas

```bash
sudo journalctl -u google-ads-backend -n 50
sudo systemctl status google-ads-backend
```

### Frontend 404 sur refresh

Vérifiez `try_files $uri $uri/ /index.html;` dans Nginx

### CORS errors

Vérifiez `CORS_ORIGINS` dans `.env.production`

### Google Ads API errors

Vérifiez credentials dans `.credentials/google-ads.yaml`

## 📞 Support

- **Documentation**: Voir README.md
- **Logs**: `/var/log/google-ads-dashboard/`
- **Issues**: GitHub repository

---

**Note**: Adaptez les chemins et domaines selon votre configuration.
