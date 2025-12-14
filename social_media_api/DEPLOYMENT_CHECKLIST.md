# PythonAnywhere Quick Deployment Checklist

## Before You Start
- [ ] PythonAnywhere account created
- [ ] Code pushed to GitHub repository
- [ ] requirements.txt file created
- [ ] .gitignore file in place
- [ ] SECRET_KEY ready for production

---

## Quick Steps Summary

### 1. PythonAnywhere Setup (5 min)
```bash
# In PythonAnywhere Bash Console
cd ~
git clone https://github.com/Stembetevo/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/social_media_api
```

### 2. Create Virtual Environment (2 min)
```bash
mkvirtualenv --python=/usr/bin/python3.10 social_media_env
pip install -r requirements.txt
```

### 3. Database Setup (3 min)
**For FREE account (use MySQL):**
- Go to Databases tab → Create MySQL database
- Note: username$socialmedia
- Get password

**For PAID account (can use PostgreSQL):**
- Sign up for ElephantSQL.com (free tier)
- Get connection credentials

### 4. Create .env File (2 min)
```bash
cd ~/Alx_DjangoLearnLab/social_media_api
nano .env
```

**For MySQL (Free Account):**
```bash
SECRET_KEY=generate-new-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DB_ENGINE=django.db.backends.mysql
DB_NAME=yourusername$socialmedia
DB_USER=yourusername
DB_PASSWORD=your-mysql-password
DB_HOST=yourusername.mysql.pythonanywhere-services.com
```

**For PostgreSQL (External):**
```bash
SECRET_KEY=generate-new-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your-elephantsql-db
DB_USER=your-elephantsql-user
DB_PASSWORD=your-elephantsql-password
DB_HOST=your-elephantsql-host
DB_PORT=5432
```

### 5. Generate SECRET_KEY (1 min)
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 6. Run Migrations (2 min)
```bash
workon social_media_env
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 7. Configure Web App (5 min)
**Web Tab:**
- Add new web app → Manual configuration → Python 3.10
- Virtual environment: `/home/yourusername/.virtualenvs/social_media_env`
- Source code: `/home/yourusername/Alx_DjangoLearnLab/social_media_api`

**Static files:**
- URL: `/static/` → Directory: `/home/yourusername/Alx_DjangoLearnLab/social_media_api/staticfiles`
- URL: `/media/` → Directory: `/home/yourusername/Alx_DjangoLearnLab/social_media_api/media`

### 8. Edit WSGI File (3 min)
Click "WSGI configuration file" and replace content with:

```python
import os
import sys
from dotenv import load_dotenv

# Add project directory
project_home = '/home/yourusername/Alx_DjangoLearnLab/social_media_api'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'social_media_api.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ Replace `yourusername` with YOUR actual username!**

### 9. Reload & Test (1 min)
- Click green "Reload" button in Web tab
- Visit: `https://yourusername.pythonanywhere.com/admin/`
- Check error logs if issues

---

## Testing Your API

Test these endpoints:
```bash
# Admin panel
https://yourusername.pythonanywhere.com/admin/

# API endpoints (adjust based on your urls.py)
https://yourusername.pythonanywhere.com/api/accounts/register/
https://yourusername.pythonanywhere.com/api/accounts/login/
https://yourusername.pythonanywhere.com/api/posts/
```

---

## Updating Your Code

When you make changes:
```bash
# In PythonAnywhere Bash Console
cd ~/Alx_DjangoLearnLab/social_media_api
git pull origin main
workon social_media_env
python manage.py migrate
python manage.py collectstatic --noinput

# Then reload from Web tab
```

---

## Troubleshooting

### If you see errors:
1. Check error log in Web tab
2. Verify .env file has correct values
3. Check WSGI file has correct username
4. Ensure virtual environment path is correct
5. Run: `python manage.py check --deploy`

### Common fixes:
```bash
# Reinstall packages
workon social_media_env
pip install -r requirements.txt --force-reinstall

# Check Django setup
python manage.py check

# View logs
tail -f ~/logs/*.log
```

---

## Important Notes

✅ **FREE Account Limitations:**
- Must use MySQL (not PostgreSQL)
- One web app only
- Limited CPU/bandwidth
- Domain: yourusername.pythonanywhere.com

✅ **PAID Account ($5/month):**
- Can use external PostgreSQL
- Custom domains
- More resources
- Multiple web apps

✅ **Security:**
- Never commit .env to GitHub
- Use strong SECRET_KEY
- Set DEBUG=False in production
- Keep dependencies updated

---

## Time Estimate
Total deployment time: **20-30 minutes**

Need help? Check: https://help.pythonanywhere.com/
