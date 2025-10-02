# Portfolio Blog

Modern, çok dilli (Türkçe/İngilizce) Django tabanlı portfolyo ve blog web sitesi.

## Özellikler

### Temel Özellikler
- 🌐 Çok dilli destek (Türkçe/İngilizce)
- 🌙 Karanlık/Açık tema desteği
- 📱 Responsive tasarım
- 🔍 Gelişmiş arama işlevselliği
- 📊 Blog ve proje istatistikleri
- 🗂️ Kategori ve etiket sistemi
- 💬 Yorum sistemi (moderasyon ile)
- 📧 İletişim formu ve newsletter
- 🔒 Güvenlik özellikleri (CAPTCHA, rate limiting)

### Teknik Özellikler
- Django 5.2.7
- MySQL veritabanı
- Tailwind CSS
- Parler (çoklu dil desteği)
- WhiteNoise (static dosya servisı)
- Docker desteği
- SEO optimizasyonu

## Kurulum

### Gereksinimler
- Python 3.12+
- MySQL 8.0+
- Node.js (opsiyonel, development için)

### 1. Projeyi İndirin
```bash
git clone <repository-url>
cd Blog
```

### 2. Virtual Environment Oluşturun
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# veya
source .venv/bin/activate  # Linux/Mac
```

### 3. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 4. Çevre Değişkenlerini Ayarlayın
`.env.example` dosyasını `.env` olarak kopyalayın ve gerekli değerleri girin:

```bash
cp .env.example .env
```

Önemli ayarlar:
- `SECRET_KEY`: Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: MySQL veritabanı bilgileri
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`: E-posta ayarları
- `HCAPTCHA_SITEKEY`, `HCAPTCHA_SECRET`: CAPTCHA ayarları

### 5. Veritabanını Oluşturun
```bash
# MySQL'de veritabanı oluşturun
mysql -u root -p
CREATE DATABASE portfolio_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Django migration'ları çalıştırın
python manage.py makemigrations
python manage.py migrate
```

### 6. Superuser Oluşturun
```bash
python manage.py createsuperuser
```

### 7. Static Dosyaları Toplayın
```bash
python manage.py collectstatic
```

### 8. Çeviri Dosyalarını Oluşturun
```bash
python manage.py makemessages -l en
python manage.py makemessages -l tr
python manage.py compilemessages
```

### 9. Geliştirme Sunucusunu Başlatın
```bash
python manage.py runserver
```

## Proje Yapısı

```
Blog/
├── portfolio_blog/          # Ana Django projesi
│   ├── settings.py         # Ayarlar
│   ├── urls.py            # Ana URL yapılandırması
│   └── wsgi.py            # WSGI yapılandırması
├── core/                   # Temel işlevsellik
│   ├── models.py          # Site ayarları, temel modeller
│   ├── views.py           # Anasayfa, arama, RSS
│   └── utils.py           # Yardımcı fonksiyonlar
├── blog/                   # Blog uygulaması
│   ├── models.py          # Post, Category, Tag modelleri
│   ├── views.py           # Blog view'ları
│   └── admin.py           # Admin yapılandırması
├── projects/               # Proje sergisi uygulaması
│   ├── models.py          # Project, TechStack modelleri
│   └── admin.py           # Admin yapılandırması
├── pages/                  # Statik sayfalar
│   ├── models.py          # Page, About, Skill modelleri
│   └── admin.py           # Admin yapılandırması
├── comments/               # Yorum sistemi
│   ├── models.py          # Comment, CommentReport modelleri
│   └── admin.py           # Admin yapılandırması
├── contact/                # İletişim ve newsletter
│   ├── models.py          # ContactMessage, Newsletter modelleri
│   └── admin.py           # Admin yapılandırması
├── templates/              # Template dosyaları
│   └── base/              # Temel template'ler
├── static/                 # Static dosyalar
│   ├── css/               # CSS dosyaları
│   ├── js/                # JavaScript dosyaları
│   └── images/            # Görsel dosyalar
├── media/                  # Kullanıcı yükleme dosyaları
├── locale/                 # Çeviri dosyaları
└── requirements.txt        # Python bağımlılıkları
```

## Kullanım

### Admin Panel
Admin paneline `/admin-secure/` URL'inden erişebilirsiniz. Güvenlik için varsayılan `/admin/` URL'i değiştirilmiştir.

### İçerik Yönetimi
1. **Blog Yazıları**: Blog kategorileri, etiketler ve yazılar
2. **Projeler**: Teknoloji yığını ve proje portföyü
3. **Sayfalar**: Statik sayfalar (Hakkımda, vb.)
4. **Yorumlar**: Yorum moderasyonu ve onay
5. **İletişim**: İletişim mesajları ve newsletter yönetimi
6. **Site Ayarları**: Genel site yapılandırması

### Çoklu Dil Desteği
- URL yapısı: `/tr/` (Türkçe), `/en/` (İngilizce)
- Varsayılan dil: Türkçe
- İçerik çevirileri: django-parler ile
- Arayüz çevirileri: Django i18n ile

### Tema Sistemi
- Otomatik: Sistem tercihi
- Açık tema
- Karanlık tema
- LocalStorage'da kalıcı

## Güvenlik

### Güvenlik Önlemleri
- CSRF koruması
- XSS koruması
- SQL injection koruması
- CAPTCHA (hCaptcha)
- Rate limiting
- Güvenli headers
- Admin URL değiştirilmiş

### Spam Koruması
- CAPTCHA doğrulaması
- Honeypot alanları
- IP tabanlı rate limiting
- Yorum moderasyonu

## Performans

### Optimizasyonlar
- Database query optimizasyonu
- Static dosya sıkıştırma
- Görsel optimizasyonu
- Caching (LocalMem)
- CDN desteği (hazır)

## Dağıtım

### Docker ile Dağıtım
```bash
# Docker Compose ile başlatın
docker-compose up -d
```

### Manuel Dağıtım
1. Sunucuda Python ve MySQL kurun
2. Projeyi klonlayın
3. Production ayarlarını yapın (.env)
4. Requirements yükleyin
5. Database migration'ları çalıştırın
6. Static dosyaları toplayın
7. Gunicorn + Nginx ile servis edin

## API Endpoints

### Public Endpoints
- `/` - Anasayfa
- `/blog/` - Blog listesi
- `/projects/` - Proje listesi
- `/about/` - Hakkımda sayfası
- `/contact/` - İletişim formu
- `/search/` - Arama
- `/rss/` - RSS feed
- `/sitemap.xml` - XML sitemap

### Admin Endpoints
- `/admin-secure/` - Admin panel

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Branch'i push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## İletişim

- **LinkedIn**: [Yusuf Turgay Çiğer](https://www.linkedin.com/in/yusuf-turgay-ciğer-557a32362)
- **GitHub**: [yusuftrg13](https://github.com/yusuftrg13?tab=repositories)
- **Email**: ytrc13@gmail.com

## Changelog

### v1.0.0 (2025-01-01)
- İlk sürüm
- Temel blog ve portfolyo işlevselliği
- Çoklu dil desteği
- Karanlık tema desteği
- Yorum sistemi
- Admin paneli
- SEO optimizasyonu