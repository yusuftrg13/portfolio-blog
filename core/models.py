from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator
import json


class SiteSetting(models.Model):
    """Site genel ayarları"""
    site_name = models.CharField(_('Site Name'), max_length=100, default='Portfolio Blog')
    site_description = models.TextField(_('Site Description'), blank=True)
    site_keywords = models.CharField(_('Site Keywords'), max_length=255, blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    github_url = models.URLField(_('GitHub URL'), blank=True)
    twitter_url = models.URLField(_('Twitter URL'), blank=True)
    email = models.EmailField(_('Contact Email'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=50, blank=True)
    footer_text = models.TextField(_('Footer Text'), blank=True)
    is_maintenance = models.BooleanField(_('Maintenance Mode'), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        """Site ayarlarını getir veya oluştur"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class TimeStampedModel(models.Model):
    """Zaman damgalı temel model"""
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        abstract = True


class SluggedModel(models.Model):
    """Slug'lı temel model"""
    slug = models.SlugField(_('Slug'), max_length=255, unique=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """Durum içeren temel model"""
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='draft')

    class Meta:
        abstract = True


class SEOModel(models.Model):
    """SEO alanları içeren temel model"""
    meta_title = models.CharField(_('Meta Title'), max_length=60, blank=True)
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True)

    class Meta:
        abstract = True
