from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, Newsletter


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_resolved', 'created_at']
    list_filter = ['is_read', 'is_resolved', 'created_at']
    list_editable = ['is_read', 'is_resolved']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['ip_address', 'user_agent', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Info', {
            'fields': ('name', 'email', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_resolved')
        }),
        ('Reply', {
            'fields': ('reply_content', 'replied_at'),
            'classes': ('collapse',)
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_resolved']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} messages marked as read.')
    mark_as_read.short_description = 'Mark as read'
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f'{updated} messages marked as resolved.')
    mark_as_resolved.short_description = 'Mark as resolved'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'is_confirmed', 'created_at', 'unsubscribed_at']
    list_filter = ['is_active', 'confirmed_at', 'created_at']
    list_editable = ['is_active']
    search_fields = ['email']
    readonly_fields = ['confirmation_token', 'unsubscribe_token', 'ip_address', 'user_agent', 
                      'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Subscription Info', {
            'fields': ('email', 'is_active')
        }),
        ('Confirmation', {
            'fields': ('confirmed_at', 'confirmation_token'),
            'classes': ('collapse',)
        }),
        ('Unsubscribe', {
            'fields': ('unsubscribed_at', 'unsubscribe_token'),
            'classes': ('collapse',)
        }),
        ('Technical Info', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_confirmed(self, obj):
        return obj.is_confirmed
    is_confirmed.boolean = True
    is_confirmed.short_description = 'Confirmed'
