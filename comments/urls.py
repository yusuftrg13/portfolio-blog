from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:post_id>/', views.CommentCreateView.as_view(), name='add_comment'),
    path('report/<int:comment_id>/', views.CommentReportView.as_view(), name='report_comment'),
]