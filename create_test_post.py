#!/usr/bin/env python
"""
Test blog postu oluşturmak için script
"""
import os
import sys
import django
from datetime import datetime
from django.utils import timezone

# Django ayarlarını yükle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings')
django.setup()

from blog.models import Category, Tag, Post
from django.contrib.auth.models import User

def create_test_content():
    print("Test içeriği oluşturuluyor...")
    
    # Test kullanıcısı al/oluştur
    try:
        user = User.objects.get(username='admin')
    except User.DoesNotExist:
        user = User.objects.get(username='test')
    
    # Kategori oluştur
    category, created = Category.objects.get_or_create(
        slug='veri-bilimi',
        defaults={
            'order': 1
        }
    )
    category.set_current_language('tr')
    category.name = 'Veri Bilimi'
    category.description = 'Veri analizi ve makine öğrenmesi konuları'
    category.save()
    print(f"Kategori oluşturuldu: {category}")
    
    # Tag oluştur
    tag, created = Tag.objects.get_or_create(
        slug='python'
    )
    tag.set_current_language('tr')
    tag.name = 'Python'
    tag.save()
    print(f"Tag oluşturuldu: {tag}")
    
    # Blog postu oluştur
    post, created = Post.objects.get_or_create(
        slug='veri-analizi-nedir',
        defaults={
            'category': category,
            'status': 'published',
            'is_featured': True,
            'published_at': timezone.now(),
            'view_count': 150
        }
    )
    
    if created:
        post.set_current_language('tr')
        post.title = 'Veri Analizi Nedir?'
        post.summary = 'Veri analizinin temellerini ve önemini keşfedelim.'
        post.content = '''<h2>Veri Analizi Nedir?</h2>

<p>Veri analizi, ham verileri anlamlı bilgilere dönüştürme süreci olarak tanımlanabilir. Bu süreç, verilerden örüntüler keşfetmek, trendleri belirlemek ve iş kararları için değerli içgörüler elde etmek amacıyla gerçekleştirilir.</p>

<h3>Veri Analizinin Aşamaları</h3>

<ol>
<li><strong>Veri Toplama:</strong> İhtiyaç duyulan verilerin farklı kaynaklardan toplanması</li>
<li><strong>Veri Temizleme:</strong> Eksik, hatalı veya tutarsız verilerin düzeltilmesi</li>
<li><strong>Veri Keşfi:</strong> Verinin yapısının ve özelliklerinin anlaşılması</li>
<li><strong>Veri Analizi:</strong> İstatistiksel yöntemler ve algoritmalar kullanılarak analiz</li>
<li><strong>Veri Görselleştirme:</strong> Sonuçların anlaşılır grafik ve tablolarla sunumu</li>
</ol>

<h3>Python ile Veri Analizi</h3>

<p>Python, veri analizi için en popüler programlama dillerinden biridir. Özellikle aşağıdaki kütüphaneler çok kullanılır:</p>

<ul>
<li><strong>Pandas:</strong> Veri manipülasyonu ve analizi</li>
<li><strong>NumPy:</strong> Sayısal hesaplamalar</li>
<li><strong>Matplotlib:</strong> Veri görselleştirme</li>
<li><strong>Seaborn:</strong> İstatistiksel veri görselleştirme</li>
</ul>

<p>Veri analizi, günümüzde her sektörde kritik bir rol oynamaktadır ve doğru analiz teknikleriyle işletmeler rekabet avantajı sağlayabilmektedir.</p>'''
        post.meta_title = 'Veri Analizi Nedir? - Python ile Veri Analizi Rehberi'
        post.meta_description = 'Veri analizinin temellerini öğrenin. Python kullanarak veri analizi nasıl yapılır, hangi araçlar kullanılır detaylı rehber.'
        post.meta_keywords = 'veri analizi, python, pandas, numpy, veri bilimi'
        post.save()
        
        # Tag'i post'a ekle
        post.tags.add(tag)
    
    print(f"Blog postu oluşturuldu: {post}")
    print(f"Status: {post.status}")
    print(f"Published: {post.is_published}")
    
    # İkinci post
    post2, created = Post.objects.get_or_create(
        slug='django-web-geliştirme',
        defaults={
            'category': category,
            'status': 'published',
            'is_featured': False,
            'published_at': timezone.now(),
            'view_count': 89
        }
    )
    
    if created:
        post2.set_current_language('tr')
        post2.title = 'Django ile Web Geliştirme'
        post2.summary = 'Django framework kullanarak modern web uygulamaları geliştirmeyi öğrenin.'
        post2.content = '''<h2>Django Nedir?</h2>

<p>Django, Python programlama dili ile yazılmış ücretsiz ve açık kaynaklı bir web framework'üdür. "Piller dahil" felsefesi ile gelir ve web geliştirme için gereken birçok özelliği hazır sunar.</p>

<h3>Django'nun Avantajları</h3>

<ul>
<li>Hızlı geliştirme imkanı</li>
<li>Güvenlik odaklı tasarım</li>
<li>Ölçeklenebilir yapı</li>
<li>Zengin ekosistem</li>
<li>Güçlü ORM sistemi</li>
</ul>

<p>Django ile modern, güvenli ve performanslı web uygulamaları geliştirebilirsiniz.</p>'''
        post2.save()
        post2.tags.add(tag)
    
    print(f"İkinci blog postu oluşturuldu: {post2}")
    
    print("\n✅ Test içeriği başarıyla oluşturuldu!")
    print(f"Toplam post sayısı: {Post.objects.filter(status='published').count()}")

if __name__ == '__main__':
    create_test_content()