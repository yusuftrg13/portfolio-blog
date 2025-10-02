"""
URL configuration for portfolio_blog project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin URL'ini değiştir (güvenlik için)
admin.site.site_header = 'Portfolio Blog Yönetimi'
admin.site.site_title = 'Portfolio Blog'
admin.site.index_title = 'Yönetim Paneli'

# URL patterns
urlpatterns = [
    path('admin-secure/', admin.site.urls),  # Güvenlik için farklı URL
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('projects/', include('projects.urls')),
    path('contact/', include('contact.urls')),
]

# Media ve static dosyalar (development için)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
