Deployment HTTPS Guide

This document provides a minimal reference for enabling HTTPS for your Django site using Nginx as a reverse proxy and Let's Encrypt (Certbot) for TLS certificates.

Prerequisites
- The Django app is served by a WSGI server (e.g. Gunicorn) on localhost (127.0.0.1) and port (e.g. 8000).
- Nginx runs on the server and listens on ports 80 and 443.
- Your domain DNS points to the server IP and `ALLOWED_HOSTS` in Django settings includes your domain.

1) Typical Nginx server block (example)

server {
    listen 80;
    server_name example.com www.example.com;

    # Redirect all HTTP to HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL certificate (managed by certbot)
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Recommended security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/static/;
    }
}

2) Obtain certificates with Certbot (on Ubuntu)

sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com

Follow prompts to obtain and install certificates. Certbot will update Nginx config and set up automatic renewal.

3) Configure Django for proxy setup
- In `settings.py` set:
  - `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`
  - Ensure `SECURE_SSL_REDIRECT = True` (or configure via env var in production)
  - Ensure `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True`

4) Local development notes
- `runserver` doesn't provide HTTPS. For local TLS testing you can:
  - Use `django-sslserver` package: `pip install django-sslserver` and run `python manage.py runsslserver 127.0.0.1:8000` (for dev only).
  - Or use a local reverse proxy (nginx) with self-signed certificates.

5) HSTS caution
- HSTS tells browsers to only use HTTPS for your domain. Once you publish a long HSTS max-age and preload, it's hard to undo.
- Test with a short `SECURE_HSTS_SECONDS` first (e.g. 60), then increase when you're confident.

6) Security review checklist
- `DEBUG=False` in production
- `ALLOWED_HOSTS` configured for your domain(s)
- HTTPS certificate renewed automatically (Certbot timer/cron)
- Cookies marked secure (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`)
- HSTS enabled after testing
- Secure headers present (CSP, X-Frame-Options, X-Content-Type-Options)

