from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from core.models import TimeStampedModel, SluggedModel, StatusModel, SEOModel


class Page(TranslatableModel, TimeStampedModel, SluggedModel, StatusModel, SEOModel):
    """Statik sayfalar (Hakkımda, Gizlilik Politikası vb.)"""
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=200),
        content=models.TextField(_('Content'), help_text=_('Markdown supported')),
    )
    
    # Sayfa türü
    page_type = models.CharField(_('Page Type'), max_length=20, choices=[
        ('about', _('About')),
        ('privacy', _('Privacy Policy')),
        ('terms', _('Terms of Service')),
        ('contact', _('Contact')),
        ('custom', _('Custom')),
    ], default='custom')
    
    # Görünüm ayarları
    show_in_menu = models.BooleanField(_('Show in Menu'), default=False)
    show_in_footer = models.BooleanField(_('Show in Footer'), default=False)
    menu_order = models.PositiveIntegerField(_('Menu Order'), default=0)
    
    # Template
    template_name = models.CharField(_('Template Name'), max_length=100, blank=True,
                                   help_text=_('Custom template name (optional)'))

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
        ordering = ['menu_order', 'translations__title']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Page {self.pk}'

    def get_absolute_url(self):
        return reverse('pages:page_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('title', any_language=True))
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == 'published'


class AboutSection(TranslatableModel, TimeStampedModel):
    """Hakkımda sayfası bölümleri"""
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=100),
        content=models.TextField(_('Content')),
    )
    
    icon = models.CharField(_('Icon Class'), max_length=100, blank=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('About Section')
        verbose_name_plural = _('About Sections')
        ordering = ['order']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Section {self.pk}'


class Skill(TranslatableModel, TimeStampedModel):
    """Beceriler"""
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=100),
    )
    
    category = models.CharField(_('Category'), max_length=50, choices=[
        ('programming', _('Programming Languages')),
        ('framework', _('Frameworks & Libraries')),
        ('database', _('Databases')),
        ('tool', _('Tools & Software')),
        ('soft_skill', _('Soft Skills')),
        ('other', _('Other')),
    ])
    
    proficiency = models.IntegerField(_('Proficiency'), choices=[
        (1, _('Beginner')),
        (2, _('Intermediate')),
        (3, _('Advanced')),
        (4, _('Expert')),
    ], default=2)
    
    icon = models.CharField(_('Icon Class'), max_length=100, blank=True)
    color = models.CharField(_('Color'), max_length=7, default='#6366f1')
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['category', 'order', 'translations__name']

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f'Skill {self.pk}'

    @property
    def proficiency_percentage(self):
        """Yetenek seviyesini yüzde olarak döndür"""
        return (self.proficiency / 4) * 100


class Experience(TranslatableModel, TimeStampedModel):
    """İş deneyimleri"""
    translations = TranslatedFields(
        position=models.CharField(_('Position'), max_length=100),
        company=models.CharField(_('Company'), max_length=100),
        description=models.TextField(_('Description'), blank=True),
    )
    
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    is_current = models.BooleanField(_('Is Current'), default=False)
    
    company_url = models.URLField(_('Company URL'), blank=True)
    location = models.CharField(_('Location'), max_length=100, blank=True)
    
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Experience')
        verbose_name_plural = _('Experiences')
        ordering = ['-start_date', 'order']

    def __str__(self):
        position = self.safe_translation_getter('position', any_language=True)
        company = self.safe_translation_getter('company', any_language=True)
        return f'{position} at {company}' if position and company else f'Experience {self.pk}'

    @property
    def duration(self):
        """İş süresi"""
        from django.utils import timezone
        end = self.end_date or timezone.now().date()
        return end - self.start_date


class Education(TranslatableModel, TimeStampedModel):
    """Eğitim bilgileri"""
    translations = TranslatedFields(
        degree=models.CharField(_('Degree'), max_length=100),
        institution=models.CharField(_('Institution'), max_length=100),
        description=models.TextField(_('Description'), blank=True),
    )
    
    start_date = models.DateField(_('Start Date'))
    end_date = models.DateField(_('End Date'), null=True, blank=True)
    is_current = models.BooleanField(_('Is Current'), default=False)
    
    gpa = models.DecimalField(_('GPA'), max_digits=3, decimal_places=2, null=True, blank=True)
    institution_url = models.URLField(_('Institution URL'), blank=True)
    location = models.CharField(_('Location'), max_length=100, blank=True)
    
    order = models.PositiveIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Education')
        ordering = ['-start_date', 'order']

    def __str__(self):
        degree = self.safe_translation_getter('degree', any_language=True)
        institution = self.safe_translation_getter('institution', any_language=True)
        return f'{degree} - {institution}' if degree and institution else f'Education {self.pk}'
