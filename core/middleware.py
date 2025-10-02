from django.utils.deprecation import MiddlewareMixin


class ThemeMiddleware(MiddlewareMixin):
    """Tema middleware'i - tema tercihlerini yönetir"""
    
    def process_request(self, request):
        theme = request.GET.get('theme')
        if theme in ['light', 'dark', 'auto']:
            request.theme_change = theme
        return None
    
    def process_response(self, request, response):
        if hasattr(request, 'theme_change'):
            response.set_cookie('theme', request.theme_change, max_age=365*24*60*60)
        return response