#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings')
django.setup()

from blog.models import Category, Tag, Post
from django.contrib.auth.models import User
from django.utils import timezone

def simple_create():
    print("Basit test post oluşturuluyor...")
    
    # Kullanıcı
    user = User.objects.first()
    
    # Kategori
    category = Category.objects.create(slug='test-kategori', order=1)
    category.set_current_language('tr')
    category.name = 'Test Kategori'
    category.save()
    
    # Post oluştur
    post = Post.objects.create(
        slug='test-post-1',
        category=category,
        status='published',
        published_at=timezone.now(),
        view_count=100
    )
    
    # Translation ekle
    post.set_current_language('tr')
    post.title = 'Test Blog Yazısı'
    post.summary = 'Bu bir test yazısıdır.'
    post.content = '<p>Bu test yazısının içeriğidir.</p>'
    post.save()
    
    print(f"✅ Post oluşturuldu: {post.title}")
    print(f"Status: {post.status}")
    print(f"Slug: {post.slug}")
    
    # İkinci post
    post2 = Post.objects.create(
        slug='test-post-2',
        category=category,
        status='published',
        published_at=timezone.now(),
        view_count=85
    )
    
    post2.set_current_language('tr')
    post2.title = 'İkinci Test Yazısı'
    post2.summary = 'İkinci test yazısı.'
    post2.content = '<p>İkinci test yazısının içeriği.</p>'
    post2.save()
    
    print(f"✅ İkinci post oluşturuldu: {post2.title}")
    
    total = Post.objects.filter(status='published').count()
    print(f"\n📊 Toplam yayınlanmış post: {total}")

if __name__ == '__main__':
    simple_create()