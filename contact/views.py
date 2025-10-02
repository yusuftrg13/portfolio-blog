from django.shortcuts import render
from django.views.generic import TemplateView

class ContactView(TemplateView):
    template_name = 'contact/contact.html'

class ContactSuccessView(TemplateView):
    template_name = 'contact/contact_success.html'

class NewsletterSubscribeView(TemplateView):
    template_name = 'contact/newsletter_subscribe.html'

class NewsletterConfirmView(TemplateView):
    template_name = 'contact/newsletter_confirm.html'

class NewsletterUnsubscribeView(TemplateView):
    template_name = 'contact/newsletter_unsubscribe.html'
