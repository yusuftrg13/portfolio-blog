#!/usr/bin/env python
"""
Django Blog Sitesi Test Raporu
Portfolio Blog - Yusuf Turgay Çiğer
Test Tarihi: 3 Ekim 2025
"""

import os
import sys
import django
import requests
from datetime import datetime

# Django ayarlarını yükle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_blog.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from blog.models import Post, Category
from projects.models import Project

class TestReporter:
    def __init__(self):
        self.client = Client()
        self.base_url = 'http://127.0.0.1:8000'
        self.results = {
            'functionality': [],
            'security': [],
            'performance': [],
            'seo': []
        }
    
    def log_test(self, category, test_name, status, details=""):
        """Test sonucunu kaydet"""
        self.results[category].append({
            'test': test_name,
            'status': '✅ BAŞARILI' if status else '❌ BAŞARISIZ',
            'details': details
        })
        status_icon = '✅' if status else '❌'
        print(f"{status_icon} {test_name}: {details}")
    
    def test_functionality(self):
        """İşlevsellik testleri"""
        print("\n🔍 İŞLEVSELLİK TESTLERİ")
        print("=" * 50)
        
        # Ana sayfa testi
        try:
            response = self.client.get('/')
            success = response.status_code == 200
            self.log_test('functionality', 'Ana Sayfa Yükleme', success, 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('functionality', 'Ana Sayfa Yükleme', False, str(e))
        
        # Blog listesi testi
        try:
            response = self.client.get('/blog/')
            success = response.status_code == 200
            self.log_test('functionality', 'Blog Listesi', success, 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('functionality', 'Blog Listesi', False, str(e))
        
        # Hakkında sayfası testi
        try:
            response = self.client.get('/about/')
            success = response.status_code == 200
            self.log_test('functionality', 'Hakkında Sayfası', success, 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('functionality', 'Hakkında Sayfası', False, str(e))
        
        # İletişim sayfası testi
        try:
            response = self.client.get('/contact/')
            success = response.status_code == 200
            self.log_test('functionality', 'İletişim Sayfası', success, 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('functionality', 'İletişim Sayfası', False, str(e))
        
        # Admin panel testi
        try:
            response = self.client.get('/admin-secure/')
            success = response.status_code == 200
            self.log_test('functionality', 'Admin Panel Erişim', success, 
                         f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('functionality', 'Admin Panel Erişim', False, str(e))
        
        # Database işlevsellik testleri
        post_count = Post.objects.filter(status='published').count()
        self.log_test('functionality', 'Blog Post Sayısı', post_count > 0, 
                     f"Yayınlanan post sayısı: {post_count}")
        
        user_count = User.objects.count()
        self.log_test('functionality', 'Kullanıcı Sistemi', user_count > 0, 
                     f"Toplam kullanıcı: {user_count}")
    
    def test_security(self):
        """Güvenlik testleri"""
        print("\n🔒 GÜVENLİK TESTLERİ")
        print("=" * 50)
        
        # CSRF koruması testi
        try:
            response = self.client.post('/contact/', {
                'name': 'Test',
                'email': 'test@test.com',
                'message': 'Test mesajı'
            })
            # CSRF token olmadan 403 olmalı
            csrf_protected = response.status_code == 403
            self.log_test('security', 'CSRF Koruması', csrf_protected, 
                         f"CSRF koruması {'aktif' if csrf_protected else 'pasif'}")
        except Exception as e:
            self.log_test('security', 'CSRF Koruması', False, str(e))
        
        # Admin panel güvenlik testi
        try:
            response = self.client.get('/admin-secure/', follow=True)
            # Login sayfasına yönlendirme olmalı
            redirected = 'login' in response.request['PATH_INFO']
            self.log_test('security', 'Admin Panel Koruması', redirected, 
                         'Yetkisiz erişim engellendi')
        except Exception as e:
            self.log_test('security', 'Admin Panel Koruması', False, str(e))
        
        # XSS koruması testi (basic)
        try:
            xss_payload = '<script>alert("XSS")</script>'
            response = self.client.get('/', {'q': xss_payload})
            xss_blocked = xss_payload not in response.content.decode()
            self.log_test('security', 'XSS Koruması', xss_blocked, 
                         'Script etiketleri filtrelendi')
        except Exception as e:
            self.log_test('security', 'XSS Koruması', False, str(e))
    
    def test_seo(self):
        """SEO testleri"""
        print("\n🔍 SEO TESTLERİ")
        print("=" * 50)
        
        # Meta title testi
        try:
            response = self.client.get('/')
            content = response.content.decode()
            has_title = '<title>' in content and '</title>' in content
            self.log_test('seo', 'Meta Title', has_title, 
                         'Sayfada title etiketi mevcut')
        except Exception as e:
            self.log_test('seo', 'Meta Title', False, str(e))
        
        # Meta description testi
        try:
            response = self.client.get('/')
            content = response.content.decode()
            has_description = 'meta name="description"' in content
            self.log_test('seo', 'Meta Description', has_description, 
                         'Meta description etiketi mevcut')
        except Exception as e:
            self.log_test('seo', 'Meta Description', False, str(e))
        
        # Responsive viewport testi
        try:
            response = self.client.get('/')
            content = response.content.decode()
            has_viewport = 'name="viewport"' in content
            self.log_test('seo', 'Responsive Viewport', has_viewport, 
                         'Viewport meta etiketi mevcut')
        except Exception as e:
            self.log_test('seo', 'Responsive Viewport', False, str(e))
    
    def generate_report(self):
        """Test raporu oluştur"""
        print("\n" + "="*70)
        print("📊 DJANGO BLOG SİTESİ TEST RAPORU")
        print("="*70)
        print(f"Test Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        print(f"Site: Portfolio Blog - Yusuf Turgay Çiğer")
        print(f"URL: {self.base_url}")
        
        for category, tests in self.results.items():
            print(f"\n📋 {category.upper()} TESTLERİ:")
            print("-" * 40)
            
            passed = sum(1 for test in tests if '✅' in test['status'])
            total = len(tests)
            success_rate = (passed / total * 100) if total > 0 else 0
            
            for test in tests:
                print(f"  {test['status']} {test['test']}")
                if test['details']:
                    print(f"    └─ {test['details']}")
            
            print(f"\n  📈 Başarı Oranı: {success_rate:.1f}% ({passed}/{total})")
        
        # Genel özet
        total_tests = sum(len(tests) for tests in self.results.values())
        total_passed = sum(
            sum(1 for test in tests if '✅' in test['status']) 
            for tests in self.results.values()
        )
        overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n🎯 GENEL SONUÇ:")
        print(f"   Toplam Test: {total_tests}")
        print(f"   Başarılı: {total_passed}")
        print(f"   Başarısız: {total_tests - total_passed}")
        print(f"   Genel Başarı: {overall_success:.1f}%")
        
        if overall_success >= 90:
            print("\n🎉 SİTE YAYINA HAZIR! Mükemmel performans.")
        elif overall_success >= 75:
            print("\n✅ SİTE İYİ DURUMDA. Küçük iyileştirmeler yapılabilir.")
        else:
            print("\n⚠️ SİTEDE İYİLEŞTİRME GEREKİYOR.")
        
        print("="*70)

def run_tests():
    """Tüm testleri çalıştır"""
    reporter = TestReporter()
    
    try:
        reporter.test_functionality()
        reporter.test_security()
        reporter.test_seo()
        reporter.generate_report()
        
    except Exception as e:
        print(f"❌ Test sürecinde hata: {e}")

if __name__ == '__main__':
    run_tests()