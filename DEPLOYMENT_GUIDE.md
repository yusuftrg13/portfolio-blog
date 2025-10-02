# 🚀 RENDER DEPLOYMENT REHBERİ
## Portfolio Blog - Yusuf Turgay Çiğer

### ADIM 1: GitHub Repository Hazırlığı

1. **GitHub'da yeni repository oluşturun**:
   - Repository name: `portfolio-blog`
   - Public veya Private seçin
   - README.md eklemeyin (zaten var)

2. **Local projeyi GitHub'a push edin**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Portfolio Blog"
   git branch -M main
   git remote add origin https://github.com/yourusername/portfolio-blog.git
   git push -u origin main
   ```

### ADIM 2: Render.com'da Hesap Oluşturma

1. **Render.com'a gidin**: https://render.com
2. **GitHub ile sign up yapın**
3. **Dashboard'a girin**

### ADIM 3: PostgreSQL Database Oluşturma

1. **Render Dashboard → "New +" → "PostgreSQL"**
2. **Database ayarları**:
   - Name: `portfolio-blog-db`
   - Database: `portfolio_blog`
   - User: `portfolio_user`
   - Region: `Frankfurt` (Avrupa için)
   - Plan: `Free` (başlangıç için)

3. **"Create Database" tıklayın**
4. **Connection string'i kopyalayın** (sonra lazım olacak)

### ADIM 4: Web Service Oluşturma

1. **Dashboard → "New +" → "Web Service"**
2. **GitHub repository'nizi seçin**
3. **Service ayarları**:
   ```
   Name: portfolio-blog
   Environment: Python 3
   Branch: main
   Root Directory: (boş bırakın)
   Build Command: ./build.sh
   Start Command: gunicorn --bind 0.0.0.0:$PORT portfolio_blog.wsgi:application
   ```

### ADIM 5: Environment Variables Ekleme

**"Environment" sekmesinde şu değişkenleri ekleyin**:

```
DJANGO_SETTINGS_MODULE = portfolio_blog.settings_production
DEBUG = False
SECRET_KEY = [50 karakterlik güçlü key oluşturun]
ALLOWED_HOSTS = portfolio-blog-xxxx.onrender.com
DATABASE_URL = [PostgreSQL connection string'i buraya]
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### ADIM 6: Deploy İşlemi

1. **"Create Web Service" tıklayın**
2. **Build işlemini izleyin** (5-10 dakika sürer)
3. **Deploy tamamlandığında URL'nizi alın**

### ADIM 7: İlk Admin Kullanıcısı Oluşturma

1. **Render Dashboard → Web Service → "Shell"**
2. **Terminal'de şu komutu çalıştırın**:
   ```bash
   python manage.py createsuperuser --settings=portfolio_blog.settings_production
   ```

### ADIM 8: Test ve Doğrulama

1. **Site URL'nizi ziyaret edin**
2. **Ana sayfa çalışıyor mu kontrol edin**
3. **Admin panel'e girin**: `https://your-url/admin-secure/`
4. **Blog yazısı ekleyin ve test edin**

---

## 🛠️ SORUN GIDERME

### Build Hatası Alırsanız:
- Render logs'unu kontrol edin
- requirements.txt doğru mu kontrol edin
- Python version uyumlu mu kontrol edin

### Database Bağlantı Hatası:
- DATABASE_URL environment variable doğru mu
- PostgreSQL service çalışıyor mu kontrol edin

### Static Files Yüklenmiyor:
- STATIC_ROOT ayarları doğru mu
- WhiteNoise middleware ekli mi kontrol edin

---

## 📞 DESTEK

Herhangi bir sorun yaşarsanız:
1. Render documentation'a bakın
2. GitHub Issues açın
3. Render community forum'unu kullanın

## 🎉 BAŞARILAR!

Deployment tamamlandığında siteniz şu özelliklere sahip olacak:
- ✅ HTTPS ile güvenli erişim
- ✅ PostgreSQL database
- ✅ Otomatik SSL sertifikası
- ✅ CDN ile hızlı static files
- ✅ Ücretsiz hosting (Free tier)

**Not**: Free tier'da site 15 dakika inaktivite sonrası uyur, ilk ziyarette 30-60 saniye açılma süresi olabilir.