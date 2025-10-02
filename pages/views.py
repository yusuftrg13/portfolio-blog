from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class PageDetailView(DetailView):
    template_name = 'pages/page_detail.html'
    
    def get_object(self):
        return None
