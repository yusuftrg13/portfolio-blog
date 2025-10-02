from .models import SiteSetting


def site_settings(request):
    """Site ayarlarını template context'e ekle"""
    return {
        'site_settings': SiteSetting.get_settings(),
    }


def theme_context(request):
    """Tema bilgilerini template context'e ekle"""
    theme = request.COOKIES.get('theme', 'auto')
    return {
        'current_theme': theme,
    }