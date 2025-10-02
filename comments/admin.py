from django.contrib import admin
from django.utils.html import format_html
from .models import Comment, CommentReport


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'content_preview', 'is_approved', 'is_spam', 'created_at']
    list_filter = ['is_approved', 'is_spam', 'created_at', 'post__category']
    list_editable = ['is_approved']
    search_fields = ['name', 'email', 'content', 'post__translations__title']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Comment Info', {
            'fields': ('post', 'parent', 'name', 'email', 'website')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_spam')
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_comments', 'mark_as_spam', 'mark_as_not_spam']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_approved=True, is_spam=False)
        self.message_user(request, f'{updated} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def mark_as_spam(self, request, queryset):
        updated = queryset.update(is_spam=True, is_approved=False)
        self.message_user(request, f'{updated} comments marked as spam.')
    mark_as_spam.short_description = 'Mark as spam'
    
    def mark_as_not_spam(self, request, queryset):
        updated = queryset.update(is_spam=False)
        self.message_user(request, f'{updated} comments marked as not spam.')
    mark_as_not_spam.short_description = 'Mark as not spam'


@admin.register(CommentReport)
class CommentReportAdmin(admin.ModelAdmin):
    list_display = ['comment', 'reason', 'reporter_ip', 'is_resolved', 'created_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    list_editable = ['is_resolved']
    readonly_fields = ['comment', 'reporter_ip', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('comment')
