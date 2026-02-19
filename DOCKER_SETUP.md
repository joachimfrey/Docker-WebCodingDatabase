# Docker-Setup für JF Datenbank

## Voraussetzungen

- Docker & Docker Compose installiert
- Linux/Mac/WSL2 (für Windows)

## Schnellstart

### 1. `.env` Datei erstellen

```bash
cp .env.example .env
```

Dann `.env` anpassen (vor allem `SECRET_KEY` und Datenbank-Passwort ändern):

```env
DEBUG=0
SECRET_KEY=your-ultra-secure-random-string-min-50-chars
ALLOWED_HOSTS=localhost,127.0.0.1,example.com,yourdomain.com
DB_NAME=webcodingdatabase
DB_USER=jfdb_user
DB_PASS=very-secure-password-change-this
```

### 2. Container starten

```bash
docker-compose up -d
```

Das wird:
- PostgreSQL-Datenbank starten
- Django-App migrieren und starten
- Nginx als Reverse Proxy starten

### 3. Statische Dateien einsammeln

```bash
docker-compose exec app python manage.py collectstatic --noinput
```

### 4. Admin-Benutzer erstellen

```bash
docker-compose exec app python manage.py createsuperuser
```

## Zugriff

- **Webseite**: http://localhost
- **Admin**: http://localhost/admin
- **Django (direct)**: http://localhost:8000

## Wichtige Befehle

### Logs anschauen
```bash
docker-compose logs -f app
docker-compose logs -f postgres
docker-compose logs -f nginx
```

### Django Shell
```bash
docker-compose exec app python manage.py shell
```

### Migrationen erstellen
```bash
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate
```

### In den Container gehen
```bash
docker-compose exec app bash
```

### Container stoppen
```bash
docker-compose down
```

### Container mit Datenlöschung stoppen
```bash
docker-compose down -v
```

## Production-Konfiguration

### SSL/HTTPS aktivieren

1. Settings.py anpassen:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

2. SSL-Zertifikate in `./ssl/` platzieren:
```
ssl/
├── cert.pem
└── key.pem
```

### Environment-Variablen

Alle wichtigen Einstellungen:

| Variable | Beschreibung | Default |
|----------|-------------|---------|
| `DEBUG` | Debug-Modus (0=Production, 1=Development) | 1 |
| `SECRET_KEY` | Django Secret Key | - |
| `ALLOWED_HOSTS` | Erlaubte Hosts (komma-getrennt) | - |
| `DB_NAME` | Datenbankname | - |
| `DB_USER` | Datenbankbenutzer | - |
| `DB_PASS` | Datenbankpasswort | - |
| `DB_HOST` | Datenbankhost | postgres |

## Dateistruktur

```
├── Dockerfile           # Django App Container
├── docker-compose.yml   # Alle Services
├── .dockerignore        # Files nicht in Image
├── .env                 # Environment (NICHT ins Repo!)
├── .env.example         # Template
├── requirements.txt     # Python Dependencies
├── nginx.conf           # Nginx Konfiguration
└── webcodingdatabase/   # Django Projekt
```

## Troubleshooting

### Port bereits in Benutzung

```bash
# Änder die Ports in docker-compose.yml
# oder:
lsof -i :80    # Linux/Mac
netstat -ano | findstr :80  # Windows
```

### Datenbankfehler

```bash
# Datenbankverbindung testen
docker-compose exec app python manage.py dbshell

# Migrationen zurücksetzen
docker-compose down -v  # ⚠️ Löscht alle Daten!
docker-compose up -d
```

### Static Files laden nicht

```bash
docker-compose exec app python manage.py collectstatic --noinput
docker-compose restart nginx
```

## Sicherheit

- ✅ Non-root Benutzer in Container
- ✅ Secrets über Environment-Variablen
- ✅ WhiteNoise für Static Files
- ✅ Nginx als Reverse Proxy
- ✅ Security Headers konfiguriert
- ✅ HSTS aktivierbar
- ✅ HTTPS/SSL-ready

Immer vor Production überprüfen:
```bash
python manage.py check --deploy
```
