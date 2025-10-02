from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Tag, Post, PostView


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'color', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['translations__name']


@admin.register(Tag)
class TagAdmin(TranslatableAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['translations__name']


@admin.register(Post)
class PostAdmin(TranslatableAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'view_count', 'published_at']
    list_filter = ['status', 'is_featured', 'category', 'tags', 'created_at']
    list_editable = ['status', 'is_featured']
    search_fields = ['translations__title', 'translations__content']
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'summary', 'content', 'category', 'tags')
        }),
        ('Media', {
            'fields': ('cover_image', 'cover_alt_text')
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'read_time'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count', 'read_time']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['post__translations__title', 'ip_address']
    readonly_fields = ['post', 'ip_address', 'user_agent', 'viewed_at']
    
    def has_add_permission(self, request):
        return False
