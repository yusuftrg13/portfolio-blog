#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings')
django.setup()

from blog.models import Post, Category
from projects.models import Project
from django.contrib.auth.models import User

def create_test_content():
    print('Creating test content...')

    # Get or create admin user
    try:
        admin = User.objects.get(username='admin')
        print(f'Found admin user: {admin.username}')
    except User.DoesNotExist:
        print('Creating admin user...')
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

    # Create blog categories
    tech_cat, created = Category.objects.get_or_create(
        slug='veri-bilimi',
        defaults={'color': '#3B82F6', 'is_active': True}
    )
    if created:
        tech_cat.create_translation('tr', name='Veri Bilimi', description='Veri bilimi ve analitik çözümleri')
    print(f'Data Science category: {tech_cat.safe_translation_getter("name", any_language=True)} (created: {created})')

    ai_cat, created = Category.objects.get_or_create(
        slug='yapay-zeka',
        defaults={'color': '#8B5CF6', 'is_active': True}
    )
    if created:
        ai_cat.create_translation('tr', name='Yapay Zeka', description='Yapay zeka ve makine öğrenmesi')
    print(f'AI category: {ai_cat.safe_translation_getter("name", any_language=True)} (created: {created})')

    # Create test blog posts
    post1_content = """Django, Python tabanlı güçlü bir web framework'üdür. Bu yazıda Django ile modern web uygulamaları geliştirme sürecini inceleyeceğiz.

## Django'nun Avantajları

- **Hızlı Geliştirme**: Django'un "Batteries Included" felsefesi sayesinde çok hızlı geliştirme yapabilirsiniz
- **Güvenlik**: Django, güvenlik açıklarına karşı built-in korumalar sunar
- **Ölçeklenebilirlik**: Büyük projelerde kullanılabilecek kadar güçlü bir yapıya sahiptir

## Model-View-Template (MVT) Mimarisi

Django, MVT mimarisini kullanır:

1. **Model**: Veritabanı katmanı
2. **View**: Business logic katmanı  
3. **Template**: Sunum katmanı

Bu mimari sayesinde kod daha organize ve sürdürülebilir olur.

## Sonuç

Django ile hızlı, güvenli ve ölçeklenebilir web uygulamaları geliştirebilirsiniz."""

    post1, created = Post.objects.get_or_create(
        title='Django ile Modern Web Uygulamaları',
        slug='django-ile-modern-web-uygulamalari',
        defaults={
            'content': post1_content,
            'author': admin,
            'category': web_cat,
            'status': 'published',
            'featured': True
        }
    )
    print(f'Post 1: {post1.title} (created: {created})')

    post2_content = """Python, veri analizi için en popüler dillerden biridir. Bu yazıda Pandas ve NumPy kütüphanelerini kullanarak veri analizi yapmayı öğreneceğiz.

## Pandas Nedir?

Pandas, Python için geliştirilmiş güçlü bir veri analizi kütüphanesidir. CSV, Excel, JSON gibi formatlardan veri okuyabilir ve işleyebilir.

### Temel Pandas İşlemleri

```python
import pandas as pd

# CSV dosyası okuma
df = pd.read_csv("data.csv")

# İlk 5 satırı gösterme
print(df.head())

# Temel istatistikler
print(df.describe())
```

## NumPy ile Matematiksel İşlemler

NumPy, Python için sayısal hesaplama kütüphanesidir:

```python
import numpy as np

# Array oluşturma
arr = np.array([1, 2, 3, 4, 5])

# Matematiksel işlemler
print(np.mean(arr))  # Ortalama
print(np.std(arr))   # Standart sapma
```

## Sonuç

Pandas ve NumPy ile Python'da güçlü veri analizleri yapabilirsiniz."""

    post2, created = Post.objects.get_or_create(
        title='Python Veri Analizi: Pandas ve NumPy',
        slug='python-veri-analizi-pandas-numpy',
        defaults={
            'content': post2_content,
            'author': admin,
            'category': tech_cat,
            'status': 'published',
            'featured': False
        }
    )
    print(f'Post 2: {post2.title} (created: {created})')

    # Create test projects
    project1_description = """Bir e-ticaret sitesi için modern ve kullanıcı dostu bir web uygulaması geliştirdim. Django, PostgreSQL ve React teknolojilerini kullanarak oluşturulan bu proje, tam kapsamlı bir online alışveriş deneyimi sunuyor.

## Özellikler

- **Kullanıcı Yönetimi**: Kayıt, giriş, profil yönetimi
- **Ürün Katalogu**: Kategoriler, filtreleme, arama
- **Sepet Sistemi**: Ürün ekleme, çıkarma, güncelleme
- **Ödeme Entegrasyonu**: Güvenli ödeme sistemi
- **Admin Panel**: Ürün ve sipariş yönetimi

## Teknolojiler

- Backend: Django REST Framework
- Frontend: React.js, Redux
- Veritabanı: PostgreSQL
- Stil: Tailwind CSS
- Dağıtım: Docker, AWS"""

    project1, created = Project.objects.get_or_create(
        title='E-Ticaret Web Uygulaması',
        slug='e-ticaret-web-uygulamasi',
        defaults={
            'description': project1_description,
            'technology_stack': 'Django, React, PostgreSQL, Docker',
            'github_url': 'https://github.com/example/ecommerce-app',
            'live_url': 'https://example-ecommerce.com',
            'status': 'completed',
            'featured': True
        }
    )
    print(f'Project 1: {project1.title} (created: {created})')

    project2_description = """Veri analizi ve görselleştirme için geliştirilmiş bir Python uygulaması. Bu proje, büyük veri setlerini analiz ederek anlamlı içgörüler çıkarıyor ve interaktif grafikler oluşturuyor.

## Özellikler

- **Veri İmportı**: CSV, Excel, JSON formatları
- **Veri Temizleme**: Eksik veriler, duplikasyonlar
- **İstatistiksel Analiz**: Descriptive ve inferential istatistikler
- **Görselleştirme**: Plotly ve Matplotlib grafikleri
- **Raporlama**: PDF ve HTML rapor oluşturma

## Teknolojiler

- Python, Pandas, NumPy
- Plotly, Matplotlib, Seaborn
- Jupyter Notebook
- Streamlit (Web Interface)"""

    project2, created = Project.objects.get_or_create(
        title='Veri Analizi Dashboard',
        slug='veri-analizi-dashboard',
        defaults={
            'description': project2_description,
            'technology_stack': 'Python, Pandas, Plotly, Streamlit',
            'github_url': 'https://github.com/example/data-analysis-dashboard',
            'live_url': 'https://example-dashboard.streamlit.app',
            'status': 'completed',
            'featured': True
        }
    )
    print(f'Project 2: {project2.title} (created: {created})')

    print('Test content created successfully!')
    print(f'Total posts: {Post.objects.count()}')
    print(f'Total projects: {Project.objects.count()}')

if __name__ == '__main__':
    create_test_content()