from django.contrib import admin
from .models import SiteSetting


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'email', 'is_maintenance', 'updated_at']
    fieldsets = (
        ('General', {
            'fields': ('site_name', 'site_description', 'site_keywords')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url')
        }),
        ('Analytics & SEO', {
            'fields': ('google_analytics_id', 'footer_text')
        }),
        ('System', {
            'fields': ('is_maintenance',)
        }),
    )
    
    def has_add_permission(self, request):
        # Sadece bir site ayarı olmasını sağla
        return not SiteSetting.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Site ayarlarının silinmesini engelle
        return False
