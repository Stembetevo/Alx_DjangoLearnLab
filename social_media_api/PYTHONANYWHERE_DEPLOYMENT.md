# PythonAnywhere Deployment Guide for Social Media API

## Prerequisites
- PythonAnywhere account (free or paid)
- GitHub repository with your code
- PostgreSQL database credentials (if using paid plan)

---

## Step 1: Sign Up and Initial Setup

### 1.1 Create PythonAnywhere Account
1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account (or paid if you need more resources)
3. **Note:** Free accounts can only use SQLite and MySQL, not PostgreSQL
   - For PostgreSQL, you need a paid account ($5/month minimum)

### 1.2 Account Limitations
- **Free Account:**
  - Use MySQL or SQLite only
  - Domain: `yourusername.pythonanywhere.com`
  - Limited outbound internet access
  
- **Paid Account ($5+/month):**
  - Can use PostgreSQL
  - Custom domains allowed
  - Full internet access

---

## Step 2: Push Your Code to GitHub

### 2.1 Initialize Git Repository (if not done)
```bash
cd /home/stephen-kinyua/Documents/ALX/Alx_DjangoLearnLab/social_media_api
git init
git add .
git commit -m "Initial commit for PythonAnywhere deployment"
```

### 2.2 Create .gitignore File
Create a `.gitignore` file with:
```
*.pyc
__pycache__/
db.sqlite3
.env
*.log
staticfiles/
media/
.venv/
venv/
*.backup.*
```

### 2.3 Push to GitHub
```bash
git remote add origin https://github.com/Stembetevo/Alx_DjangoLearnLab.git
git branch -M main
git push -u origin main
```

---

## Step 3: Set Up PythonAnywhere Environment

### 3.1 Open a Bash Console
1. Log into PythonAnywhere
2. Go to "Consoles" tab
3. Click "Bash" to start a new console

### 3.2 Clone Your Repository
```bash
cd ~
git clone https://github.com/Stembetevo/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
```

### 3.3 Create Virtual Environment
```bash
# Create virtual environment with Python 3.10 (or your preferred version)
mkvirtualenv --python=/usr/bin/python3.10 social_media_env

# Activate it (should auto-activate after creation)
workon social_media_env
```

### 3.4 Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Step 4: Configure Database

### Option A: Using MySQL (Free Account Compatible)

#### 4.1 Create MySQL Database
1. Go to "Databases" tab in PythonAnywhere dashboard
2. Set a MySQL password (if first time)
3. Create a new database (e.g., `yourusername$socialmedia`)
4. Note your database credentials:
   - Host: `yourusername.mysql.pythonanywhere-services.com`
   - Database name: `yourusername$socialmedia`
   - Username: `yourusername`
   - Password: (the one you set)

#### 4.2 Update settings.py for MySQL
Add this to your settings.py:
```python
# At the top
import dj_database_url

# Replace DATABASES configuration
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    # Production database (MySQL on PythonAnywhere)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # Development database (PostgreSQL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
```

#### 4.3 Install MySQL Client
```bash
pip install mysqlclient
```

### Option B: Using PostgreSQL (Paid Account Required)

#### 4.1 Set Up PostgreSQL
1. PythonAnywhere doesn't provide PostgreSQL hosting
2. Use external PostgreSQL service:
   - **ElephantSQL** (free tier available)
   - **Heroku Postgres** (free tier available)
   - **Amazon RDS**
   - **DigitalOcean Managed Databases**

#### 4.2 Get PostgreSQL Credentials
Sign up for ElephantSQL (example):
1. Go to [www.elephantsql.com](https://www.elephantsql.com)
2. Create free "Tiny Turtle" instance
3. Get connection details:
   - Host
   - Database name
   - User
   - Password
   - Port (usually 5432)

---

## Step 5: Configure Environment Variables

### 5.1 Create .env File on PythonAnywhere
```bash
cd ~/Alx_DjangoLearnLab/social_media_api
nano .env
```

### 5.2 Add Environment Variables
```bash
# Django Settings
SECRET_KEY=your-new-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
PYTHONANYWHERE_DOMAIN=yourusername.pythonanywhere.com

# Database Settings (MySQL Example)
DB_NAME=yourusername$socialmedia
DB_USER=yourusername
DB_PASSWORD=your-mysql-password
DB_HOST=yourusername.mysql.pythonanywhere-services.com

# Or for PostgreSQL (external)
# DB_NAME=your_elephantsql_db
# DB_USER=your_elephantsql_user
# DB_PASSWORD=your_elephantsql_password
# DB_HOST=your_elephantsql_host
# DB_PORT=5432
```

**Important:** Generate a new SECRET_KEY for production:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Step 6: Run Migrations and Collect Static Files

### 6.1 Run Migrations
```bash
cd ~/Alx_DjangoLearnLab/social_media_api
workon social_media_env
python manage.py migrate
```

### 6.2 Create Superuser
```bash
python manage.py createsuperuser
```

### 6.3 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## Step 7: Configure Web App

### 7.1 Create Web App
1. Go to "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10 (or your version)

### 7.2 Configure WSGI File
1. Click on "WSGI configuration file" link
2. Replace content with:

```python
import os
import sys
from dotenv import load_dotenv

# Add your project directory to the sys.path
project_home = '/home/yourusername/Alx_DjangoLearnLab/social_media_api'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Set environment variable for DJANGO_SETTINGS_MODULE
os.environ['DJANGO_SETTINGS_MODULE'] = 'social_media_api.settings'

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `yourusername` with your actual PythonAnywhere username!**

### 7.3 Configure Virtual Environment
1. In the "Web" tab, find "Virtualenv" section
2. Enter path: `/home/yourusername/.virtualenvs/social_media_env`

### 7.4 Configure Static Files
In the "Web" tab, "Static files" section:
- URL: `/static/`
- Directory: `/home/yourusername/Alx_DjangoLearnLab/social_media_api/staticfiles`

If you have media files:
- URL: `/media/`
- Directory: `/home/yourusername/Alx_DjangoLearnLab/social_media_api/media`

### 7.5 Configure Source Code
In "Code" section:
- Source code: `/home/yourusername/Alx_DjangoLearnLab/social_media_api`
- Working directory: `/home/yourusername/Alx_DjangoLearnLab/social_media_api`

---

## Step 8: Final Configuration in settings.py

### 8.1 Update ALLOWED_HOSTS
Make sure your .env has:
```bash
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

### 8.2 Add WhiteNoise to Middleware (already done)
Verify in settings.py:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # This should be here
    # ... other middleware
]
```

### 8.3 Update Static Files Settings
Verify in settings.py:
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## Step 9: Reload and Test

### 9.1 Reload Web App
1. Go to "Web" tab
2. Click the green "Reload" button
3. Wait for reload to complete

### 9.2 Test Your API
Visit your URLs:
- Main site: `https://yourusername.pythonanywhere.com/`
- Admin: `https://yourusername.pythonanywhere.com/admin/`
- API endpoints: `https://yourusername.pythonanywhere.com/api/...`

### 9.3 Check Error Logs
If something doesn't work:
1. Go to "Web" tab
2. Check "Error log" (click to view)
3. Check "Server log" (click to view)
4. Debug and fix issues

---

## Step 10: Ongoing Maintenance

### 10.1 Update Code
When you make changes:
```bash
# In PythonAnywhere bash console
cd ~/Alx_DjangoLearnLab/social_media_api
git pull origin main
workon social_media_env
pip install -r requirements.txt  # If dependencies changed
python manage.py migrate  # If models changed
python manage.py collectstatic --noinput  # If static files changed

# Then reload web app from Web tab
```

### 10.2 View Logs
```bash
# Error log
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Server log
tail -f /var/log/yourusername.pythonanywhere.com.server.log
```

### 10.3 Database Backups
```bash
# For MySQL
mysqldump -h yourusername.mysql.pythonanywhere-services.com -u yourusername -p yourusername\$socialmedia > backup.sql

# For PostgreSQL (if using external service)
# Use their backup tools or pg_dump
```

---

## Common Issues and Solutions

### Issue 1: ImportError or ModuleNotFoundError
**Solution:** Make sure virtual environment is activated and all packages installed
```bash
workon social_media_env
pip install -r requirements.txt
```

### Issue 2: 502 Bad Gateway
**Solution:** 
- Check WSGI file is correctly configured
- Check error logs
- Verify Python version matches

### Issue 3: Static Files Not Loading
**Solution:**
- Run `python manage.py collectstatic`
- Check static files mapping in Web tab
- Verify STATIC_ROOT path is correct

### Issue 4: Database Connection Error
**Solution:**
- Verify database credentials in .env
- Check database exists
- For MySQL: ensure mysqlclient is installed
- For PostgreSQL: ensure psycopg2-binary is installed

### Issue 5: ALLOWED_HOSTS Error
**Solution:**
- Update .env with correct domain
- Restart web app
- Check ALLOWED_HOSTS in settings.py

---

## Security Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY is unique and not in version control
- [ ] ALLOWED_HOSTS is properly configured
- [ ] Database password is strong
- [ ] HTTPS is enabled (automatic on PythonAnywhere)
- [ ] Security headers are configured
- [ ] Static files use WhiteNoise
- [ ] .env file is not in git repository
- [ ] Regular backups scheduled

---

## Resources

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)

---

## Support

If you encounter issues:
1. Check PythonAnywhere forums
2. Review error logs
3. Contact PythonAnywhere support (support@pythonanywhere.com)
4. Check Django documentation

Good luck with your deployment! 🚀
