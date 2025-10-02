from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('success/', views.ContactSuccessView.as_view(), name='contact_success'),
    path('newsletter/subscribe/', views.NewsletterSubscribeView.as_view(), name='newsletter_subscribe'),
    path('newsletter/confirm/<str:token>/', views.NewsletterConfirmView.as_view(), name='newsletter_confirm'),
    path('newsletter/unsubscribe/<str:token>/', views.NewsletterUnsubscribeView.as_view(), name='newsletter_unsubscribe'),
]