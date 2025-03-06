from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy

from recipes.models import Recipes
from users.forms import LoginUserForm, RegisterUserForm


def user_home(request):
    user_name = request.user.username
    user_id = request.user.pk
    posts = Recipes.objects.filter(author=user_id)

    return render(request, 'users/user_home.html', {'posts': posts, 'name': user_name})

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return render(request, 'users:user_home')


# def login_user(request):
#
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user and user.is_active:
#                 login(request, user)
#                 return reverse_lazy('home')
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
