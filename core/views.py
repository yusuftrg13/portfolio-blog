from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.syndication.views import Feed
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from blog.models import Post, Category
from projects.models import Project


class HomeView(TemplateView):
    """Anasayfa view'ı"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Son blog yazıları
        context['latest_posts'] = Post.objects.filter(
            status='published'
        ).select_related('category').prefetch_related('tags')[:6]
        
        # Öne çıkan projeler
        context['featured_projects'] = Project.objects.filter(
            status='published',
            is_featured=True
        ).prefetch_related('tech_stack')[:4]
        
        # İstatistikler - gerçek verilerden
        context['total_posts'] = Post.objects.filter(status='published').count()
        context['total_projects'] = Project.objects.filter(status='published').count()
        context['total_views'] = Post.objects.filter(status='published').aggregate(
            total=Sum('view_count')
        )['total'] or 0
        context['categories_count'] = Category.objects.filter(is_active=True).count()
        
        return context


class AboutView(TemplateView):
    """Hakkımda sayfası view'ı"""
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Teknik yetenekler
        context['technical_skills'] = [
            {
                'category': 'Full-Stack Web Geliştirme',
                'skills': ['Django', 'Python', 'JavaScript', 'React', 'HTML5', 'CSS3', 'Bootstrap', 'Tailwind CSS'],
                'description': 'Dinamik ve modern web uygulamaları geliştirmek için Django backend framework\'ü ile birlikte HTML, CSS ve JavaScript kullanıyorum. Kullanıcı arayüzü (UI) oluşturmada ve interaktif front-end bileşenleri geliştirmede React kütüphanesine hakimim.'
            },
            {
                'category': 'Veri Analizi & Görselleştirme',
                'skills': ['Python', 'Pandas', 'NumPy', 'Scikit-learn', 'SQL', 'Power BI', 'Tableau'],
                'description': 'Python (Pandas, NumPy, Scikit-learn) ve SQL ile veri temizleme, analiz ve istatistiksel modelleme yapabiliyorum. Power BI ve Tableau kullanarak karmaşık veri kümelerini anlaşılır, etkileşimli gösterge panolarına ve raporlara dönüştürüyorum.'
            },
            {
                'category': 'İş Analizi & Süreç İyileştirme',
                'skills': ['Sistem Analizi', 'Proje Yönetimi', 'Süreç Optimizasyonu', 'İş Zekası', 'Stakeholder Yönetimi'],
                'description': 'Sistem analizi ve proje yönetimi altyapımdan güç alarak, karmaşık iş süreçlerini analiz ediyor, ihtiyaçları belirliyor ve teknoloji odaklı iyileştirme önerileri geliştiriyorum. Teknik çözümler ile iş gereksinimleri arasında köprü kurabiliyorum.'
            }
        ]
        
        return context


class BlogListView(TemplateView):
    """Blog listesi sayfası view'ı"""
    template_name = 'core/blog_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Yayınlanan blog yazıları
        posts = Post.objects.filter(status='published').select_related('category').prefetch_related('tags').order_by('-published_at')
        
        # Sayfalama
        paginator = Paginator(posts, 9)  # Sayfa başına 9 yazı
        page = self.request.GET.get('page', 1)
        context['posts'] = paginator.get_page(page)
        
        # Kategoriler
        context['categories'] = Category.objects.filter(is_active=True)
        
        return context


class ProjectListView(TemplateView):
    """Proje listesi sayfası view'ı"""
    template_name = 'core/project_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Yayınlanan projeler
        projects = Project.objects.filter(status='published').prefetch_related('tech_stack').order_by('-created_at')
        
        # Sayfalama
        paginator = Paginator(projects, 6)  # Sayfa başına 6 proje
        page = self.request.GET.get('page', 1)
        context['projects'] = paginator.get_page(page)
        
        return context


class ContactView(TemplateView):
    """İletişim sayfası view'ı"""
    template_name = 'core/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # İletişim bilgileri
        context['contact_info'] = {
            'email': 'ytrc13@gmail.com',
            'phone': '+90 XXX XXX XX XX',  # Telefon numaranızı buraya ekleyebilirsiniz
            'location': 'Türkiye',
            'linkedin': 'https://www.linkedin.com/in/yusuf-turgay-ciğer-557a32362',
            'github': 'https://github.com/ytrc13',  # GitHub profilinizi ekleyebilirsiniz
        }
        
        return context
    
    def post(self, request, *args, **kwargs):
        """İletişim formunu işle"""
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            try:
                # E-posta gönder
                full_message = f"""
Yeni İletişim Mesajı

Gönderen: {name}
E-posta: {email}
Konu: {subject}

Mesaj:
{message}
                """
                
                send_mail(
                    subject=f'[Portfolio Blog] {subject}',
                    message=full_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                
                messages.success(request, 'Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağım.')
                return redirect('core:contact')
                
            except Exception as e:
                messages.error(request, 'Mesaj gönderilirken bir hata oluştu. Lütfen daha sonra tekrar deneyin veya doğrudan e-posta gönderin.')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
        
        return self.get(request, *args, **kwargs)


class SearchView(TemplateView):
    """Arama view'ı"""
    template_name = 'core/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        
        if query:
            # Blog yazılarında arama
            posts = Post.objects.filter(
                Q(translations__title__icontains=query) |
                Q(translations__content__icontains=query) |
                Q(translations__summary__icontains=query),
                status='published'
            ).distinct().select_related('category')
            
            # Projelerde arama
            projects = Project.objects.filter(
                Q(translations__title__icontains=query) |
                Q(translations__description__icontains=query) |
                Q(translations__summary__icontains=query),
                status='published'
            ).distinct()
            
            # Sayfalama
            post_paginator = Paginator(posts, 10)
            project_paginator = Paginator(projects, 10)
            
            page = self.request.GET.get('page', 1)
            context['posts'] = post_paginator.get_page(page)
            context['projects'] = project_paginator.get_page(page)
            context['total_results'] = posts.count() + projects.count()
        else:
            context['posts'] = []
            context['projects'] = []
            context['total_results'] = 0
        
        context['query'] = query
        
        # AJAX isteği için JSON response
        if self.request.GET.get('ajax'):
            results = []
            
            for post in context['posts'][:5]:
                results.append({
                    'title': post.title,
                    'summary': post.summary[:150] + '...',
                    'url': post.get_absolute_url(),
                    'type': 'post'
                })
            
            for project in context['projects'][:5]:
                results.append({
                    'title': project.title,
                    'summary': project.summary[:150] + '...',
                    'url': project.get_absolute_url(),
                    'type': 'project'
                })
            
            return JsonResponse({'results': results})
        
        return context


class SitemapView(TemplateView):
    """XML Sitemap view'ı"""
    template_name = 'core/sitemap.xml'
    content_type = 'application/xml'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['posts'] = Post.objects.filter(status='published')
        context['projects'] = Project.objects.filter(status='published')
        
        return context


class RobotsView(TemplateView):
    """Robots.txt view'ı"""
    template_name = 'core/robots.txt'
    content_type = 'text/plain'


class RSSFeedView(Feed):
    """RSS Feed view'ı"""
    title = "Portfolio Blog"
    link = "/rss/"
    description = "Latest blog posts and projects"
    
    def items(self):
        return Post.objects.filter(status='published').order_by('-published_at')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.summary
    
    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.published_at
