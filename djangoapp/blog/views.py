from typing import Any
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render
from blog.models import Post,Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

PER_PAGE = 9

# https://docs.djangoproject.com/pt-br/4.2/ref/class-based-views/ Documentação


class PostListView(ListView):
    model = Post
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'    
    ordering = '-pk',
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(is_published =True)        
    #     return queryset
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'page_title': 'Home - ',
        })        
        return context

def index(request):
    posts = Post.objects.get_published()
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'Home - ',
        }
    )


def page(request, slug):    
    
    page_object = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )
    
    if page_object is None:
        raise Http404()


    page_title =  f'{page_object.title} - Página - '
    
    return render(
        request,
        'blog/pages/page.html',
        {
            'page': page_object,
            'page_title': page_title,
        }
    )

def post(request, slug):
    post_object = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
    )
    
    if post_object is None:
       raise Http404()

    page_title =  f'{post_object.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
              'post': post_object,
              'page_title': page_title,
        }
    )
    
def created_by(request, author_pk):
    
    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()
    
    posts = Post.objects.get_published()\
        .filter(created_by__pk=author_pk)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    user_full_name = user.username
    
    page_title = 'Posts de ' + user_full_name + ' - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def category(request, slug):
    posts = Post.objects.get_published()\
        .filter(category__slug=slug)       
        
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj)==0:
        raise Http404        
    
    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def tag(request, slug):
    posts = Post.objects.get_published()\
        .filter(tags__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj)==0:
        raise Http404        
    
    page_title = f'{page_obj[0].tags.first().name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )    

def search(request):
    search_value = request.GET.get('search', '').strip()

    posts = (
        Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]
    )
    
    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )    