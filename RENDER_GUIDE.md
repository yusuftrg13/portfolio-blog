# 🚀 Render.com Deployment Guide

## Render ile Django Deploy - Adım Adım

### 1. Render Hesabı Oluşturun
1. **https://render.com** sayfasına gidin
2. **GitHub ile giriş yapın**
3. GitHub hesabınızı bağlayın

### 2. PostgreSQL Veritabanı Oluşturun
1. Dashboard'da **"New +"** tıklayın
2. **"PostgreSQL"** seçin
3. Ayarlar:
   - **Name**: `portfolio-blog-db`
   - **Database**: `portfolio_blog`
   - **User**: `portfolio_user`
   - **Region**: `Frankfurt (EU Central)`
   - **Plan**: **Free** seçin
4. **"Create Database"** tıklayın
5. ⏳ Veritabanı hazır olana kadar bekleyin (2-3 dakika)

### 3. Web Service Oluşturun
1. Tekrar **"New +"** tıklayın
2. **"Web Service"** seçin
3. **"Connect a repository"** > GitHub'dan `portfolio-blog` seçin
4. Ayarları yapın:

**Basic Settings:**
- **Name**: `portfolio-blog`
- **Region**: `Frankfurt (EU Central)`
- **Branch**: `master`
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn portfolio_blog.wsgi:application`

### 4. Environment Variables Ekleyin
**Environment** sekmesinde şu değişkenleri ekleyin:

```
SECRET_KEY = django-insecure-your-super-secret-key-here-123456789-change-this
DEBUG = False
DJANGO_SETTINGS_MODULE = portfolio_blog.settings_production
ALLOWED_HOSTS = portfolio-blog.onrender.com
```

### 5. DATABASE_URL Bağlayın
1. Environment variables'da **"Add from database"** tıklayın
2. Oluşturduğunuz `portfolio-blog-db` veritabanını seçin
3. **"Add DATABASE_URL"** tıklayın

### 6. Deploy Edin
1. **"Create Web Service"** butonuna tıklayın
2. ⏳ Build sürecini izleyin (5-10 dakika sürebilir)

### 7. Site Hazır! 🎉
- Site URL'iniz: `https://portfolio-blog.onrender.com`
- Admin paneli: `https://portfolio-blog.onrender.com/admin/`

### 8. Super User Oluşturun (Opsiyonel)
1. Dashboard'da web service'inize gidin
2. **"Shell"** sekmesinde terminal açın
3. Komut çalıştırın:
```bash
python manage.py createsuperuser --settings=portfolio_blog.settings_production
```

## ✅ Deployment Checklist
- [ ] GitHub repo hazır
- [ ] PostgreSQL veritabanı oluşturuldu
- [ ] Web service oluşturuldu
- [ ] Environment variables eklendi
- [ ] DATABASE_URL bağlandı
- [ ] Build başarılı
- [ ] Site erişilebilir
- [ ] Admin paneli çalışıyor

## 🔧 Sorun Giderme
- **Build hatası**: Logs sekmesinde build loglarını kontrol edin
- **Database hatası**: DATABASE_URL doğru bağlandığından emin olun
- **Static dosya sorunu**: `./build.sh` dosyasının çalıştığını kontrol edin
- **500 hatası**: Environment variables'ı kontrol edin

**Render ücretsiz planı:** 750 saat/ay, 15 dakika inaktivite sonrası sleep mode