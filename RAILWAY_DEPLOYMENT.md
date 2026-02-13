# 🚂 Railway Deployment Guide - Zero To Hero

## ✅ Kya Kya Setup Ho Gaya

| File | Purpose |
|------|---------|
| `railway.json` | Railway deployment configuration |
| `config/settings.py` | Updated for Railway + Render |
| `requirements.txt` | All dependencies included |

---

## 🚀 Railway Par Deploy Karne Ke Steps

### Step 1: Railway Account Banayein
🔗 **https://railway.app/**

1. **"Get Started"** click karein
2. GitHub se login karein

### Step 2: New Project Create Karein

1. Dashboard par **"New Project"** click karein
2. **"Deploy from GitHub repo"** select karein
3. **"zerotohero"** repository select karein
4. **"Add Variables"** par click karein

### Step 3: Environment Variables Add Karein

**Variables** tab mein yeh add karein:

```env
DJANGO_SECRET_KEY = django-insecure-railway-secret-key-change-this
DEBUG = False
USE_SQLITE = False
```

**Optional (agar chahiye to):**
```env
RAZORPAY_KEY_ID = your_key_here
RAZORPAY_KEY_SECRET = your_secret_here
EMAIL_HOST_USER = your_email@gmail.com
EMAIL_HOST_PASSWORD = your_app_password
```

### Step 4: PostgreSQL Database Add Karein

1. **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway automatically `DATABASE_URL` set kar dega

### Step 5: Deploy Karein

1. **"Deploy"** button click karein
2. 2-3 minute wait karein
3. **🎉 Done!** URL automatically generate hoga

---

## 🌐 URL Kaisa Hoga

Railway automatically clean URL deta hai:
- Example: `https://zerotohero-production.up.railway.app/`
- Ya: `https://zerotohero.railway.app/`

**Custom domain** bhi free mein add kar sakte hain!

---

## 🆓 Railway Free Tier

| Feature | Limit |
|---------|-------|
| **Execution Time** | $5 credit/month (~500 hours) |
| **Bandwidth** | 100 GB/month |
| **Disk** | 1 GB |
| **Sleep** | Nahi hota (24/7 running) |

---

## 🎯 Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| **Sleep Mode** | ✅ 15 min idle (slow first request) | ❌ No sleep |
| **Database** | ✅ Free PostgreSQL | ✅ Free PostgreSQL |
| **URL** | `app.onrender.com` | `app.railway.app` |
| **Setup** | Blueprint/Web Service | Auto from GitHub |
| **Best For** | Static + Dynamic | Dynamic apps |

---

## 🐛 Common Issues

### Issue 1: "Module not found"
**Solution:** `requirements.txt` check karein, sab dependencies present honi chahiye

### Issue 2: Database connection error
**Solution:** PostgreSQL service add karein, `DATABASE_URL` automatically set ho jayega

### Issue 3: Static files not loading
**Solution:** `railway.json` mein `collectstatic` command already hai

---

## 📞 Help

Agar koi issue aaye to:
- Railway Docs: https://docs.railway.app/
- Discord: https://discord.gg/railway

---

## 🎉 Ready to Deploy!

**Railway** par jayein aur **"New Project"** → **"GitHub Repo"** select karein! 🚀
