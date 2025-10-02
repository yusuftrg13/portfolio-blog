from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from parler.models import TranslatableModel, TranslatedFields
from core.models import TimeStampedModel, SluggedModel, StatusModel, SEOModel
from core.utils import calculate_read_time
import os


class Category(TranslatableModel, TimeStampedModel, SluggedModel):
    """Blog kategorileri"""
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=100),
        description=models.TextField(_('Description'), blank=True),
    )
    color = models.CharField(_('Color'), max_length=7, default='#6366f1', help_text='Hex color code')
    is_active = models.BooleanField(_('Is Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'translations__name']

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f'Category {self.pk}'

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('name', any_language=True))
        super().save(*args, **kwargs)


class Tag(TranslatableModel, TimeStampedModel, SluggedModel):
    """Blog etiketleri"""
    translations = TranslatedFields(
        name=models.CharField(_('Name'), max_length=50),
    )
    is_active = models.BooleanField(_('Is Active'), default=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['translations__name']

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f'Tag {self.pk}'

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.safe_translation_getter('name', any_language=True))
        super().save(*args, **kwargs)


def post_cover_image_path(instance, filename):
    """Post kapak görseli yolu"""
    return f'blog/covers/{instance.slug}/{filename}'


class Post(TranslatableModel, TimeStampedModel, SluggedModel, StatusModel, SEOModel):
    """Blog yazıları"""
    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=200),
        summary=models.TextField(_('Summary'), max_length=300, help_text=_('Short description for post lists')),
        content=models.TextField(_('Content'), help_text=_('Markdown supported')),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name=_('Category'))
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name=_('Tags'))
    
    cover_image = models.ImageField(_('Cover Image'), upload_to=post_cover_image_path, blank=True)
    cover_alt_text = models.CharField(_('Cover Alt Text'), max_length=200, blank=True)
    
    is_featured = models.BooleanField(_('Is Featured'), default=False, help_text=_('Show on homepage'))
    view_count = models.PositiveIntegerField(_('View Count'), default=0)
    read_time = models.PositiveIntegerField(_('Read Time (minutes)'), default=1)
    
    published_at = models.DateTimeField(_('Published At'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f'Post {self.pk}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            title = self.safe_translation_getter('title', any_language=True) if self.pk else None
            if title:
                self.slug = slugify(title)
            else:
                # Eğer henüz translation yoksa, boş bir slug oluştur
                self.slug = f'post-{self.pk or "new"}'
        
        # İlk kayıtta read_time hesaplama
        if self.pk:
            content = self.safe_translation_getter('content', any_language=True)
            if content:
                self.read_time = calculate_read_time(content)
        
        super().save(*args, **kwargs)

    def increment_view_count(self):
        """Görüntülenme sayısını artır"""
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])
        self.refresh_from_db()

    def get_related_posts(self, count=3):
        """Benzer yazıları getir"""
        return Post.objects.filter(
            status='published',
            category=self.category
        ).exclude(pk=self.pk).order_by('-published_at')[:count]

    @property
    def is_published(self):
        return self.status == 'published' and self.published_at is not None


class PostView(models.Model):
    """Post görüntülenme takibi"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Post View')
        verbose_name_plural = _('Post Views')
        unique_together = ['post', 'ip_address']
