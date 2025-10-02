from django.shortcuts import render
from django.utils.translation import get_language


def get_client_ip(request):
    """Client IP adresini getir"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calculate_read_time(content):
    """İçerik okuma süresini hesapla (dakika)"""
    words = len(content.split())
    # Ortalama okuma hızı: 200 kelime/dakika
    read_time = max(1, round(words / 200))
    return read_time


def get_theme_preference(request):
    """Kullanıcı tema tercihini getir"""
    theme = request.COOKIES.get('theme', 'auto')
    return theme


def set_language_preference(response, language_code):
    """Dil tercihini cookie'ye kaydet"""
    response.set_cookie('django_language', language_code, max_age=365*24*60*60)
    return response