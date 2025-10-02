from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from core.models import TimeStampedModel, SluggedModel, StatusModel, SEOModel
import os


def project_image_path(instance, filename):
    """Proje görseli yolu"""
    return f'projects/{instance.slug}/{filename}'


class TechStack(TranslatableModel, TimeStampedModel, SluggedModel):
    """Teknoloji yığını/araçları"""
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=50),
    )
    icon = models.CharField(_('Icon Class'), max_length=100, blank=True, help_text=_('CSS icon class'))
    color = models.CharField(_('Color'), max_length=7, default='#6366f1', help_text='Hex color code')
    is_active = models.BooleanField(_('Is Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Tech Stack')
        verbose_name_plural = _('Tech Stacks')
        ordering = ['order', 'translations__name']

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f'Tech {self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('name', any_language=True))
        super().save(*args, **kwargs)


class Project(TranslatableModel, TimeStampedModel, SluggedModel, StatusModel, SEOModel):
    """Projeler"""
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=200),
        summary=models.TextField(_('Summary'), max_length=300, help_text=_('Short description for project lists')),
        description=models.TextField(_('Description'), help_text=_('Detailed project description, Markdown supported')),
    )
    
    tech_stack = models.ManyToManyField(TechStack, blank=True, related_name='projects', verbose_name=_('Tech Stack'))
    
    # Görseller
    featured_image = models.ImageField(_('Featured Image'), upload_to=project_image_path, blank=True)
    image_alt_text = models.CharField(_('Image Alt Text'), max_length=200, blank=True)
    
    # Linkler
    demo_url = models.URLField(_('Demo URL'), blank=True, help_text=_('Live demo link'))
    repo_url = models.URLField(_('Repository URL'), blank=True, help_text=_('GitHub/GitLab repository link'))
    documentation_url = models.URLField(_('Documentation URL'), blank=True)
    
    # Proje detayları
    start_date = models.DateField(_('Start Date'), null=True, blank=True)
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    client = models.CharField(_('Client'), max_length=100, blank=True)
    project_type = models.CharField(_('Project Type'), max_length=50, choices=[
        ('personal', _('Personal')),
        ('commercial', _('Commercial')),
        ('open_source', _('Open Source')),
        ('academic', _('Academic')),
    ], default='personal')
    
    # Görünüm ayarları
    is_featured = models.BooleanField(_('Is Featured'), default=False, help_text=_('Show on homepage'))
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    order = models.PositiveIntegerField(_('Order'), default=0, help_text=_('Display order on project list'))

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Project {self.pk}'

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('title', any_language=True))
        super().save(*args, **kwargs)

    def increment_view_count(self):
        """Görüntülenme sayısını artır"""
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])
        self.refresh_from_db()

    @property
    def is_published(self):
        return self.status == 'published'

    @property
    def duration(self):
        """Proje süresi"""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        return None

    @property
    def is_ongoing(self):
        """Devam eden proje mi"""
        return self.start_date and not self.end_date


class ProjectImage(models.Model):
    """Proje ek görselleri"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('Image'), upload_to=project_image_path)
    alt_text = models.CharField(_('Alt Text'), max_length=200, blank=True)
    caption = models.CharField(_('Caption'), max_length=300, blank=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Project Image')
        verbose_name_plural = _('Project Images')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'{self.project.title} - Image {self.order}'


class ProjectView(models.Model):
    """Proje görüntülenme takibi"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Project View')
        verbose_name_plural = _('Project Views')
        unique_together = ['project', 'ip_address']
