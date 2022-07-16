from django.contrib.auth import logout,login
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, ListView, DetailView


from blog.models import *
from blog.forms import AddPostForm, LoginUserForm, RegisterUserForm
from blog.utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


def skip(request):
    return redirect('blog/')

class LoginUser(DataMixin, LoginView):
    from_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

class BlogHome(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context
    def get_queryser(self):
        return Post.objects.filter(is_published=True)


class Contact(ListView):
    model = Post
    template_name = 'blog/contact.html'
    extra_context = {'title': 'Связь с нами'}


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context


class PostCategory(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False
    

    def get_queryset(self):
        return Post.objects.filter(cat__slug =self.kwargs['cat_slug'], is_published=True)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = context['posts'][0].cat_id
        return context


class About(ListView):
    model = Post
    template_name = 'blog/about.html'
    context_object_name = 'posts'
    extra_context = {'title': 'О нас'}


class ShowPost(DataMixin, DetailView):
    model = Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    #pk_url_kwarg = 'post_pk'
    conext_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


def about(request): #HttpRequest
    return render(request, 'blog/about.html', {'title': 'О нас'})

def categories(request, cat):
    if(request.GET):
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям<h1><p>{cat}</p>")


def archive(request, year):
    if int(year) > 2022:
        return redirect('home', permanent=True)
    return HttpResponse(f"<h1>Архив по годама</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


