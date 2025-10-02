# PythonAnywhere Deployment Guide for Django Portfolio Blog

## 1. PythonAnywhere Hesabı Oluşturma
1. https://www.pythonanywhere.com sayfasına gidin
2. "Create a Beginner account" tıklayın (ücretsiz)
3. Kullanıcı adınızı seçin (örn: yusuftrg13)
4. Hesabınızı oluşturun

## 2. GitHub'dan Projeyi Klonlama
PythonAnywhere Dashboard'da:
1. "Tasks" > "Bash Console" açın
2. Şu komutları çalıştırın:

```bash
git clone https://github.com/yusuftrg13/portfolio-blog.git portfolio_blog
cd portfolio_blog
```

## 3. Virtual Environment Oluşturma
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. MySQL Veritabanı Oluşturma
1. Dashboard'da "Databases" sekmesine gidin
2. "Create a database" tıklayın
3. Database adı: `portfolioblog`
4. Şifrenizi kaydedin

## 5. Django Ayarları
```bash
cd portfolio_blog
python manage.py migrate --settings=portfolio_blog.settings_pythonanywhere
python manage.py collectstatic --noinput --settings=portfolio_blog.settings_pythonanywhere
python manage.py createsuperuser --settings=portfolio_blog.settings_pythonanywhere
```

## 6. Web App Oluşturma
1. Dashboard'da "Web" sekmesine gidin
2. "Add a new web app" tıklayın
3. "Manual configuration" seçin
4. "Python 3.10" seçin

## 7. WSGI Configuration
1. Web sekmesinde "WSGI configuration file" linkine tıklayın
2. Dosyayı tamamen silin ve `pythonanywhere_wsgi.py` içeriğini yapıştırın
3. Dosyada `yusuftrg13` kısmını kendi kullanıcı adınızla değiştirin

## 8. Static Files Mapping
Web sekmesinde "Static files" bölümünde:
- URL: `/static/`
- Directory: `/home/yusuftrg13/portfolio_blog/staticfiles`

## 9. Virtual Environment Path
Web sekmesinde "Virtualenv" bölümünde:
- Path: `/home/yusuftrg13/portfolio_blog/venv`

## 10. Reload Web App
"Reload" butonuna tıklayın ve sitenizi test edin!

## Önemli Notlar:
- Database şifresini `settings_pythonanywhere.py` dosyasında güncelleyin
- Kullanıcı adı `yusuftrg13` yerine kendi kullanıcı adınızı kullanın
- Ücretsiz hesapta 1 web app sınırı var
- Site URL'iniz: https://yusuftrg13.pythonanywhere.com olacak