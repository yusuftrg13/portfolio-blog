from django.urls import path
from .views import HomeView, AboutView, BlogListView, ProjectListView, ContactView, SearchView, SitemapView, RobotsView, RSSFeedView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('search/', SearchView.as_view(), name='search'),
    path('sitemap.xml', SitemapView.as_view(), name='sitemap'),
    path('robots.txt', RobotsView.as_view(), name='robots'),
    path('rss/', RSSFeedView(), name='rss'),
]