from django.shortcuts import render
from django.views.generic import TemplateView

class CommentCreateView(TemplateView):
    template_name = 'comments/comment_create.html'

class CommentReportView(TemplateView):
    template_name = 'comments/comment_report.html'
