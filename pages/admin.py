from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Page, AboutSection, Skill, Experience, Education


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    list_display = ['title', 'page_type', 'status', 'show_in_menu', 'show_in_footer', 'menu_order']
    list_filter = ['page_type', 'status', 'show_in_menu', 'show_in_footer']
    list_editable = ['status', 'show_in_menu', 'show_in_footer', 'menu_order']
    search_fields = ['translations__title', 'translations__content']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'page_type')
        }),
        ('Display Options', {
            'fields': ('show_in_menu', 'show_in_footer', 'menu_order', 'template_name')
        }),
        ('Publishing', {
            'fields': ('status',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AboutSection)
class AboutSectionAdmin(TranslatableAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['translations__title', 'translations__content']


@admin.register(Skill)
class SkillAdmin(TranslatableAdmin):
    list_display = ['name', 'category', 'proficiency', 'order', 'is_active']
    list_filter = ['category', 'proficiency', 'is_active']
    list_editable = ['proficiency', 'order', 'is_active']
    search_fields = ['translations__name']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'category', 'proficiency')
        }),
        ('Display', {
            'fields': ('icon', 'color', 'order', 'is_active')
        }),
    )


@admin.register(Experience)
class ExperienceAdmin(TranslatableAdmin):
    list_display = ['position', 'company', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['is_current', 'is_active', 'start_date']
    list_editable = ['is_current', 'is_active']
    search_fields = ['translations__position', 'translations__company']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Job Info', {
            'fields': ('position', 'company', 'description')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Info', {
            'fields': ('company_url', 'location')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Education)
class EducationAdmin(TranslatableAdmin):
    list_display = ['degree', 'institution', 'start_date', 'end_date', 'is_current', 'is_active']
    list_filter = ['is_current', 'is_active', 'start_date']
    list_editable = ['is_current', 'is_active']
    search_fields = ['translations__degree', 'translations__institution']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Education Info', {
            'fields': ('degree', 'institution', 'description')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Info', {
            'fields': ('gpa', 'institution_url', 'location')
        }),
        ('Display', {
            'fields': ('order', 'is_active')
        }),
    )
