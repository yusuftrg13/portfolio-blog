# 🚂 Railway Deployment Guide

## Railway ile Django Deploy - Süper Kolay!

### 1. Railway Hesabı Oluşturun
1. **https://railway.app** sayfasına gidin
2. **"Login with GitHub"** tıklayın
3. GitHub hesabınızı bağlayın

### 2. Yeni Proje Oluşturun
1. Dashboard'da **"New Project"** tıklayın
2. **"Deploy from GitHub repo"** seçin
3. `yusuftrg13/portfolio-blog` deposunu seçin
4. **"Deploy Now"** tıklayın

### 3. Environment Variables Ekleyin
**Variables** sekmesinde şu değişkenleri ekleyin:

```
DJANGO_SETTINGS_MODULE = portfolio_blog.settings_railway
SECRET_KEY = django-insecure-super-secret-key-change-this-123456789
DEBUG = False
PYTHONPATH = /app
PORT = 8000
```

### 4. PostgreSQL Ekleyin (Opsiyonel)
1. **"+ New"** tıklayın
2. **"Database"** > **"Add PostgreSQL"** seçin
3. Otomatik olarak `DATABASE_URL` environment variable'ı eklenecek

### 5. Deploy Ayarları
Railway otomatik olarak:
- ✅ `requirements.txt`'yi okuyacak
- ✅ Dependencies'leri yükleyecek
- ✅ `Procfile`'ı çalıştıracak
- ✅ PostgreSQL'i bağlayacak

### 6. Custom Domain (Opsiyonel)
1. **Settings** > **Domains** 
2. **"Generate Domain"** tıklayın
3. Özel URL alın: `your-app-name.up.railway.app`

## ✅ Railway Avantajları:
- 🚀 **Süper hızlı** deployment (2-3 dakika)
- 🔄 **Auto deploy** GitHub push'larda
- 💾 **PostgreSQL** otomatik
- 📊 **Real-time logs** 
- 💳 **$5 kredi/ay** ücretsiz

## 🎯 Beklenen Sonuç:
- Site URL'iniz: `https://portfolio-blog-production.up.railway.app`
- Admin paneli: `/admin/`
- Otomatik SSL sertifikası

## 🔧 Sorun Giderme:
- **Build hatası**: Deployment logs'ları kontrol edin
- **Database hatası**: PostgreSQL service'inin aktif olduğunu kontrol edin
- **Static files**: WhiteNoise otomatik çalışır

**Railway kredisi bittiyse SQLite ile de çalışır!**