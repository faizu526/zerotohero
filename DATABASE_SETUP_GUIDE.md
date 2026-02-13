# 🗄️ Database Setup & Viewing Guide - Zero To Hero

## 📊 Database Name
**Database Name:** `zerotohero_db` (updated from `zerotohero`)

---

## 🚀 Option 1: Use SQLite (Easiest - No PostgreSQL Required)

Agar aapke system mein PostgreSQL nahi hai, toh SQLite use karein:

### Step 1: `.env` file edit karein
```bash
USE_SQLITE=True
```

### Step 2: Migrations run karein
```bash
cd /home/redmoon/zerotohero
python manage.py makemigrations
python manage.py migrate
```

### Step 3: SQLite Database View Kaise Karein
SQLite database file directly `db.sqlite3` ke roop mein hai. Isse dekhne ke 3 tareeke:

#### Method A: VS Code Extension (Easiest)
1. VS Code mein jaayein
2. Extensions mein search karein: **"SQLite Viewer"**
3. Install karein
4. `db.sqlite3` file par click karein - directly table view milega!

#### Method B: Command Line
```bash
# SQLite CLI install karein (agar nahi hai)
sudo apt-get install sqlite3

# Database open karein
sqlite3 db.sqlite3

# Tables dekhein
.tables

# Schema dekhein
.schema

# Data dekhein
SELECT * FROM core_customuser;
SELECT * FROM core_order;
.quit
```

#### Method C: DB Browser for SQLite (GUI)
```bash
# Install karein
sudo apt-get install sqlitebrowser

# Open karein
sqlitebrowser db.sqlite3
```

---

## 🐘 Option 2: Use PostgreSQL (Production Ready)

### Step 1: PostgreSQL Install Karein
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
sudo service postgresql start
```

### Step 2: Database & User Create Karein
```bash
# PostgreSQL user switch karein
sudo -u postgres psql

# Database create karein
CREATE DATABASE zerotohero_db;

# User create karein (optional)
CREATE USER zth_user WITH PASSWORD 'your_password';

# Permissions dein
GRANT ALL PRIVILEGES ON DATABASE zerotohero_db TO zth_user;

# Exit
\q
```

### Step 3: `.env` Configure Karein
```bash
DB_NAME=zerotohero_db
DB_USER=postgres  # ya zth_user agar create kiya
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
USE_SQLITE=False
```

### Step 4: Python PostgreSQL Driver Install Karein
```bash
pip install psycopg2-binary
```

### Step 5: Migrations Run Karein
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: PostgreSQL Database Kaise Dekhein

#### Method A: pgAdmin (GUI - Best for beginners)
```bash
# Install pgAdmin
sudo apt-get install pgadmin4

# Web interface open karein
# URL: http://localhost/pgadmin4
```

#### Method B: Command Line (psql)
```bash
# PostgreSQL user switch karein
sudo -u postgres psql

# Database select karein
\c zerotohero_db

# Tables dekhein
\dt

# Table schema dekhein
\d core_customuser

# Data dekhein
SELECT * FROM core_customuser;
SELECT * FROM core_order;

# Exit
\q
```

#### Method C: VS Code Extension
1. Extension install karein: **"PostgreSQL"** by Chris Kolkman
2. Ctrl+Shift+P → "PostgreSQL: New Query"
3. Connection details enter karein

---

## 🖥️ Server Start Kaise Karein

### Development Server
```bash
cd /home/redmoon/zerotohero

# Virtual environment activate karein (agar hai)
source ../venv/bin/activate

# Server start karein
python manage.py runserver

# URL: http://127.0.0.1:8000/
```

### Admin Panel Access
```
http://127.0.0.1:8000/admin/
```

### Superuser Create Karein (Admin ke liye)
```bash
python manage.py createsuperuser
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Issue 2: "database does not exist"
```bash
# PostgreSQL mein database create karein
sudo -u postgres createdb zerotohero_db
```

### Issue 3: "permission denied"
```bash
# PostgreSQL mein permissions dein
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE zerotohero_db TO postgres;"
```

### Issue 4: Server start nahi ho raha
```bash
# Check karein koi process 8000 port use toh nahi kar raha
lsof -ti:8000 | xargs kill -9

# Ya different port use karein
python manage.py runserver 8080
```

---

## 📊 Database Schema Overview

### Tables Created:
1. **core_customuser** - Users with affiliate info
2. **core_order** - Purchase orders
3. **core_course** - Enrolled courses
4. **core_wishlist** - User wishlists
5. **core_affiliatetransaction** - Affiliate earnings
6. **core_category** - Course categories
7. **core_tag** - Course tags

### Key Relationships:
- User → Orders (One to Many)
- User → Courses (One to Many)
- User → Wishlist (One to Many)
- Order → AffiliateTransaction (One to Many)

---

## 🎯 Quick Start Recommendation

**Agar aap beginner hain:**
1. SQLite use karein (`USE_SQLITE=True`)
2. VS Code mein "SQLite Viewer" extension install karein
3. `python manage.py runserver` se start karein

**Agar aap production ready setup chahte hain:**
1. PostgreSQL install karein
2. `pgadmin4` use karein database dekhne ke liye
3. Proper `.env` configuration karein

---

## ❓ Need Help?

Agar koi error aata hai, toh yeh commands run karke output share karein:
```bash
# Django check
python manage.py check

# Database status
python manage.py showmigrations

# Error details
python manage.py runserver --verbosity 2
