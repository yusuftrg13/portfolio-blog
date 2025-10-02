from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from core.models import TimeStampedModel
from blog.models import Post


class Comment(TimeStampedModel):
    """Blog yorumları"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Post'))
    
    # Yorum sahibi bilgileri
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'), blank=True, help_text=_('Optional, will not be displayed publicly'))
    website = models.URLField(_('Website'), blank=True)
    
    # Yorum içeriği
    content = models.TextField(_('Content'), max_length=1000)
    
    # Moderasyon
    is_approved = models.BooleanField(_('Is Approved'), default=False)
    is_spam = models.BooleanField(_('Is Spam'), default=False)
    
    # Teknik bilgiler
    ip_address = models.GenericIPAddressField(_('IP Address'))
    user_agent = models.TextField(_('User Agent'), blank=True)
    
    # Yanıt sistemi (isteğe bağlı)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='replies', verbose_name=_('Parent Comment'))

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'is_approved']),
            models.Index(fields=['is_approved', 'created_at']),
        ]

    def __str__(self):
        return f'{self.name} - {self.post.title[:50]}'

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.pk}"

    @property
    def is_reply(self):
        """Bu yorum bir yanıt mı"""
        return self.parent is not None

    @property
    def approved_replies(self):
        """Onaylanmış yanıtlar"""
        return self.replies.filter(is_approved=True, is_spam=False)

    def get_email_hash(self):
        """E-posta hash'i (Gravatar için)"""
        import hashlib
        if self.email:
            return hashlib.md5(self.email.lower().encode()).hexdigest()
        return None

    def approve(self):
        """Yorumu onayla"""
        self.is_approved = True
        self.is_spam = False
        self.save(update_fields=['is_approved', 'is_spam'])

    def mark_as_spam(self):
        """Spam olarak işaretle"""
        self.is_spam = True
        self.is_approved = False
        self.save(update_fields=['is_approved', 'is_spam'])


class CommentReport(TimeStampedModel):
    """Yorum şikayetleri"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports')
    reporter_ip = models.GenericIPAddressField(_('Reporter IP'))
    reason = models.CharField(_('Reason'), max_length=20, choices=[
        ('spam', _('Spam')),
        ('inappropriate', _('Inappropriate Content')),
        ('offensive', _('Offensive Language')),
        ('other', _('Other')),
    ])
    description = models.TextField(_('Description'), blank=True, max_length=500)
    is_resolved = models.BooleanField(_('Is Resolved'), default=False)

    class Meta:
        verbose_name = _('Comment Report')
        verbose_name_plural = _('Comment Reports')
        unique_together = ['comment', 'reporter_ip']

    def __str__(self):
        return f'Report for comment {self.comment.pk} - {self.reason}'
