from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from .models import Post, Category, Tag


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category').prefetch_related('tags').order_by('-published_at')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(
            category=self.object,
            status='published'
        ).select_related('category').prefetch_related('tags').order_by('-published_at')
        
        paginator = Paginator(posts, 9)
        page = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page)
        return context


class TagDetailView(DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(
            tags=self.object,
            status='published'
        ).select_related('category').prefetch_related('tags').order_by('-published_at')
        
        paginator = Paginator(posts, 9)
        page = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('category').prefetch_related('tags')
    
    def get_object(self):
        obj = super().get_object()
        # Görüntülenme sayısını artır
        obj.increment_view_count()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = self.object.get_related_posts()
        return context
