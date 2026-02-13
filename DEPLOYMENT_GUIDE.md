# 🚀 Zero To Hero - Render Deployment Guide
## Free Django Hosting with Clean URL

---

## ✅ Kya Kya Setup Ho Gaya Hai

Maine aapke liye yeh files create kar di hain:

| File | Purpose |
|------|---------|
| `render.yaml` | Render deployment configuration |
| `build.sh` | Build script (runs during deployment) |
| `.env.example` | Environment variables template |
| `config/settings.py` | Updated with production settings |
| `requirements.txt` | Added `dj-database-url` |

---

## 🌐 Render Par Deploy Karne Ke Steps

### Step 1: GitHub Repository Push Karein

```bash
# 1. Initialize git (agar nahi hai to)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Ready for Render deployment"

# 4. GitHub par repo create karein (https://github.com/new)
# Phir push karein:
git remote add origin https://github.com/YOUR_USERNAME/zerotohero.git
git branch -M main
git push -u origin main
```

### Step 2: Render Account Banayein

1. **https://render.com** par jayein
2. **"Get Started for Free"** par click karein
3. GitHub se sign up karein (easiest option)

### Step 3: New Web Service Create Karein

1. Dashboard par **"New +"** button click karein
2. **"Web Service"** select karein
3. Apna GitHub repo connect karein:
   - `zerotohero` repo select karein
   - **"Connect"** click karein

### Step 4: Configuration (Auto-filled hoga)

Render automatically `render.yaml` se settings le lega:

- **Name**: `zerotohero` (ya aap change kar sakte hain)
- **Runtime**: Python 3
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`

### Step 5: Environment Variables Set Karein

**"Environment"** tab par jayein aur yeh variables add karein:

```env
# Required Variables
DJANGO_SECRET_KEY = django-insecure-change-this-to-random-string
DEBUG = False
USE_SQLITE = False
RENDER_EXTERNAL_HOSTNAME = zerotohero.onrender.com

# Optional - Payment Gateway
RAZORPAY_KEY_ID = rzp_test_your_key_here
RAZORPAY_KEY_SECRET = your_secret_here

# Optional - Email
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
```

### Step 6: Deploy Karein

1. **"Create Web Service"** button click karein
2. Wait karein (5-10 minutes)
3. **🎉 Done!** Aapka URL ready: `https://zerotohero.onrender.com`

---

## 🔧 Custom Domain (Optional - Free)

Agar aapko apna domain chahiye (jaise `zerotohero.com`):

1. **Namecheap** ya **Freenom** se free domain lein (`.tk`, `.ml`, `.ga`)
2. Render dashboard → **"Custom Domains"**
3. Apna domain add karein
4. DNS settings mein CNAME record add karein:
   ```
   Type: CNAME
   Name: www
   Value: zerotohero.onrender.com
   ```

---

## 🆓 Render Free Tier Limits

| Feature | Limit |
|---------|-------|
| **Bandwidth** | 100 GB/month |
| **Build Minutes** | 500 minutes/month |
| **Disk** | 512 MB |
| **Sleep** | After 15 min idle (first request thoda slow) |
| **Database** | 90 days retention |

**Tip**: Agar traffic zyada ho to paid plan ($7/month) upgrade kar sakte hain.

---

## 🐛 Common Issues & Solutions

### Issue 1: Static Files Not Loading
**Solution**: `build.sh` mein `collectstatic` already hai, check karein ki ` whitenoise` install hai.

### Issue 2: Database Connection Error
**Solution**: Render automatically `DATABASE_URL` set karta hai. Agar error aaye to:
- Render Dashboard → PostgreSQL database check karein
- `USE_SQLITE = False` confirm karein

### Issue 3: 500 Error After Deploy
**Solution**: Logs check karein:
```bash
# Render dashboard → Logs tab
```

### Issue 4: CSRF Error
**Solution**: `RENDER_EXTERNAL_HOSTNAME` sahi set karein environment variables mein.

---

## 📞 Support

Agar koi issue aaye to:
1. Render Docs: https://render.com/docs/deploy-django
2. Django Deploy Checklist: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

---

## 🎉 Success!

Aapki website live hogi at: `https://zerotohero.onrender.com`

**Clean URL** ✅  
**Free SSL (HTTPS)** ✅  
**PostgreSQL Database** ✅  
**Auto Deploy on Git Push** ✅

---

**Ready to deploy?** GitHub push karein aur Render par connect karein! 🚀
