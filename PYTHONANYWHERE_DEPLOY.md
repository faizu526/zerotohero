# 🐍 PythonAnywhere Deployment - Easiest for Django!

## Why PythonAnywhere?
- ✅ Django officially supported
- ✅ No CLI needed - Web interface only
- ✅ 24/7 running (no sleep)
- ✅ MySQL database included
- ✅ Easiest setup!

---

## 🚀 Step-by-Step Deployment

### Step 1: Account Create Karein
🔗 **https://www.pythonanywhere.com/**
- **"Start running Python online in less than a minute"**
- Free account create karein

### Step 2: Web App Create Karein
1. Dashboard par **"Web"** tab click karein
2. **"Add a new web app"** button click karein
3. **"Next"** click karein
4. **"Django"** select karein
5. **Python 3.10** select karein
6. **"Next"** → Project name: `zerotohero`

### Step 3: GitHub Repo Clone Karein
**"Consoles"** tab → **"Bash"** console open karein:

```bash
# Yeh commands run karein:
cd ~
git clone https://github.com/faizu526/zerotohero.git
```

### Step 4: Virtual Environment Setup
```bash
# Virtual environment create karein:
cd ~/zerotohero
python3.10 -m venv venv
source venv/bin/activate

# Dependencies install karein:
pip install -r requirements.txt
```

### Step 5: Web App Configuration
**"Web"** tab → Apni web app select karein:

**Source code:** `/home/yourusername/zerotohero`

**Working directory:** `/home/yourusername/zerotohero`

**WSGI file:** Edit karein:
```python
import sys
path = '/home/yourusername/zerotohero'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Static Files Setup
**"Static files"** section:
- URL: `/static/`
- Directory: `/home/yourusername/zerotohero/staticfiles`

### Step 7: Database Migrate
Bash console mein:
```bash
cd ~/zerotohero
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic
```

### Step 8: Reload Karein
**"Web"** tab → **"Reload"** button click karein

---

## 🎉 Done!

**URL:** `https://yourusername.pythonanywhere.com/`

---

## 🆓 Free Tier Limits
- ✅ 1 web app
- ✅ 24/7 running
- ✅ 512 MB storage
- ✅ MySQL database
- ✅ Daily CPU limit (enough for small sites)

---

## 🐛 Common Issues

### Issue: "Module not found"
**Solution:** Virtual environment activate karein, `pip install` karein

### Issue: Static files not loading
**Solution:** `collectstatic` run karein, path check karein

### Issue: Database error
**Solution:** `migrate` command run karein

---

## 📞 Help
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Help pages: https://help.pythonanywhere.com/

---

## 🎯 Ready!

**https://www.pythonanywhere.com/** par jayein aur start karein! 🚀
