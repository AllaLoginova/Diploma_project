from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, \
    HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from .forms import AddPostForm, UploadFileForm, PostFilterForm
from .models import Recipes, Category, TagPost, UploadFiles
from .utils import DataMixin


class RecipesHome(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        # Базовый запрос
        queryset = Recipes.published.all().select_related('cat')

        # Получаем параметры из GET-запроса
        order = self.request.GET.get('order')

        # Фильтрация и сортировка
        if order == 'with_photo':
            queryset = queryset.filter(~Q(photo=''))  # Посты с фото
        elif order == 'without_photo':
            queryset = queryset.filter(photo='')  # Посты без фото
        elif order == 'new':
            queryset = queryset.order_by('-time_create')  # Новые посты (сначала свежие)
        elif order == 'old':
            queryset = queryset.order_by('time_create')  # Старые посты (сначала старые)

        return queryset

    def get_context_data(self, **kwargs):
        # Добавляем форму в контекст
        context = super().get_context_data(**kwargs)
        context['show_filter_form'] = True
        context['filter_form'] = PostFilterForm(self.request.GET)
        return context


def search(request):
    query = request.GET.get('q')  # Получаем поисковый запрос
    title = query.capitalize()
    if query:
        # Ищем рецепты
        results = Recipes.objects.filter(Q(title__icontains=title))
    else:
        results = Recipes.objects.none()  # Если запрос пустой, возвращаем пустой результат

    return render(request, 'recipes/search_results.html', {'results': results, 'query': query})


class ShowPost(DataMixin, DetailView):
    template_name = 'recipes/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Recipes.published, slug=self.kwargs[self.slug_url_kwarg])


# class AddPage(LoginRequiredMixin, DataMixin, CreateView):
#     """Класс AddPage обрабатывает
#         создание нового рецепта,
#         связывая его с автором и
#         обеспечивая доступ только
#         для авторизованных пользователей"""
#
#     form_class = AddPostForm # Указывает, что для создания нового рецепта будет использоваться форма AddPostForm
#     template_name = 'recipes/addpage.html' # Определяет шаблон, который будет использоваться для отображения страницы добавления рецепта
#     title_page = 'Добавление рецепта' # Переменная для хранения заголовка страницы, который можно использовать в шаблоне
#
#     def form_valid(self, form): # Метод, который вызывается, когда форма успешно прошла валидацию.
#         w = form.save(commit=False) # Создает новый объект рецепта, но не сохраняет его в базе данных сразу
#         w.author = self.request.user # Устанавливает автора рецепта как текущего пользователя.
#         return super().form_valid(form) # Вызывает метод родительского класса для завершения процесса сохранения и перенаправления.


class AddPage(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'recipes/addpage.html'
    title_page = 'Добавление рецепта'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        w.save()

        # Добавляем сообщение об успешном добавлении
        messages.success(self.request, 'Рецепт был успешно добавлен!')

        # Если это AJAX-запрос, возвращаем JSON
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'post_id': w.id})

        # Возвращаем пустую форму в контексте
        return self.render_to_response(self.get_context_data(form=AddPostForm()))

    def form_invalid(self, form):
        # Проверяем, является ли запрос AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

        return super().form_invalid(form)


class UpdatePage(DataMixin, UpdateView):
    model = Recipes
    fields = ['title', 'content', 'photo', 'is_published', 'cat', 'tags']
    template_name = 'recipes/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование рецепта'

class DeletePost(DataMixin, DeleteView):
    model = Recipes
    template_name = 'recipes/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')
    title_page = 'Удаление рецепта'


@login_required
def about(request):
    contact_list = Recipes.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recipes/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})


@login_required
def user_posts(request):

    posts = Recipes.objects.filter(author_id=user_id)
    return render(request, 'recipes/user_posts.html', {'posts': posts})


def login(request):
    return HttpResponse("Авторизация")


class RecipesCategory(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Recipes.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class TagPostList(DataMixin, ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Recipes.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

