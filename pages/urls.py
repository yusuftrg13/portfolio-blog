from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
]