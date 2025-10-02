from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """İletişim mesajları"""
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'), max_length=2000)
    
    # Moderasyon ve takip
    is_read = models.BooleanField(_('Is Read'), default=False)
    is_resolved = models.BooleanField(_('Is Resolved'), default=False)
    admin_notes = models.TextField(_('Admin Notes'), blank=True, help_text=_('Internal notes for admin'))
    
    # Teknik bilgiler
    ip_address = models.GenericIPAddressField(_('IP Address'))
    user_agent = models.TextField(_('User Agent'), blank=True)
    
    # Yanıt bilgileri
    replied_at = models.DateTimeField(_('Replied At'), null=True, blank=True)
    reply_content = models.TextField(_('Reply Content'), blank=True)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_read', 'created_at']),
            models.Index(fields=['is_resolved', 'created_at']),
        ]

    def __str__(self):
        return f'{self.name} - {self.subject}'

    def mark_as_read(self):
        """Okundu olarak işaretle"""
        self.is_read = True
        self.save(update_fields=['is_read'])

    def mark_as_resolved(self):
        """Çözüldü olarak işaretle"""
        self.is_resolved = True
        self.save(update_fields=['is_resolved'])


class Newsletter(TimeStampedModel):
    """Newsletter abonelikleri"""
    email = models.EmailField(_('Email'), unique=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    confirmed_at = models.DateTimeField(_('Confirmed At'), null=True, blank=True)
    confirmation_token = models.CharField(_('Confirmation Token'), max_length=64, blank=True)
    
    # Unsubscribe
    unsubscribed_at = models.DateTimeField(_('Unsubscribed At'), null=True, blank=True)
    unsubscribe_token = models.CharField(_('Unsubscribe Token'), max_length=64, blank=True)
    
    # Teknik bilgiler
    ip_address = models.GenericIPAddressField(_('IP Address'), null=True, blank=True)
    user_agent = models.TextField(_('User Agent'), blank=True)

    class Meta:
        verbose_name = _('Newsletter Subscription')
        verbose_name_plural = _('Newsletter Subscriptions')
        ordering = ['-created_at']

    def __str__(self):
        return self.email

    @property
    def is_confirmed(self):
        return self.confirmed_at is not None

    def confirm_subscription(self):
        """Aboneliği onayla"""
        from django.utils import timezone
        self.confirmed_at = timezone.now()
        self.is_active = True
        self.save(update_fields=['confirmed_at', 'is_active'])

    def unsubscribe(self):
        """Abonelikten çık"""
        from django.utils import timezone
        self.unsubscribed_at = timezone.now()
        self.is_active = False
        self.save(update_fields=['unsubscribed_at', 'is_active'])
