from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import TechStack, Project, ProjectImage, ProjectView


@admin.register(TechStack)
class TechStackAdmin(TranslatableAdmin):
    list_display = ['name', 'color', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['translations__name']


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'alt_text', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ['title', 'project_type', 'status', 'is_featured', 'view_count', 'start_date']
    list_filter = ['status', 'is_featured', 'project_type', 'tech_stack', 'created_at']
    list_editable = ['status', 'is_featured']
    search_fields = ['translations__title', 'translations__description']
    filter_horizontal = ['tech_stack']
    date_hierarchy = 'start_date'
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'summary', 'description', 'tech_stack')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_alt_text')
        }),
        ('Links', {
            'fields': ('demo_url', 'repo_url', 'documentation_url')
        }),
        ('Project Details', {
            'fields': ('project_type', 'client', 'start_date', 'end_date')
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'order')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count']


@admin.register(ProjectView)
class ProjectViewAdmin(admin.ModelAdmin):
    list_display = ['project', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['project__translations__title', 'ip_address']
    readonly_fields = ['project', 'ip_address', 'user_agent', 'viewed_at']
    
    def has_add_permission(self, request):
        return False
