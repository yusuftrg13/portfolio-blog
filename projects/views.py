from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6
    
    def get_queryset(self):
        return Project.objects.filter(status='published').prefetch_related('tech_stack').order_by('-created_at')


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(status='published').prefetch_related('tech_stack')
