
from django.core.paginator import Paginator
import time
from django.contrib.auth.models import Group, Permission

from django.http import JsonResponse
from django.views.generic import ListView, TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from firstblog.neyronka import train_xgboost
from .polinomregression import train_polynomial_regression_model
from .models import Post
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render
from firstblog.gradient import train_sql, visualize_sql

class BlogListView(ListView):
    model = Post
    template_name = 'blog/home.html'


class PostView(View):
    """"вывод записей"""

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/home.html', {'post_list': posts})


class AboutPageView(TemplateView):
    template_name = 'blog/about.html'


class InputPageView(TemplateView):
    template_name = 'blog/imput.html'

class PolinomView(TemplateView):
    template_name = 'result.html'

class XGBoostTrainView(View):
    def get(self, request):
        result = train_xgboost()
        return JsonResponse(result)

class PolinomTrainView(View):
    def get(self, request):
        result = train_polynomial_regression_model()
        return JsonResponse(result)
class GradientTrainView(View):
    def get(self, request):
        result = train_sql()
        return JsonResponse(result)
class GradientTrainView(View):
    def get(self, request):

        train_result = train_sql()
        res = visualize_sql()
        return JsonResponse(train_result)
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')

        # Validate form data
        if not username or not email or not password:
            return render(request, 'register.html')

        # Ensure password is properly hashed
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)

        if status == 'admin':
            group = Group.objects.get(name='Authors')  # Assuming 'Authors' group already exists
            user.groups.add(group)  # Add user to the 'Authors' group
            user.user_permissions.set(Permission.objects.all())


        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to the home page
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    return redirect('home')


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 1)  # Показывать по 1 записи на странице

    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'blog/home.html', {'page_obj': page_obj})


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        author = request.POST.get('author')
        date = request.POST.get('date')

        post = Post(title=title, description=description, author=author, date=date)
        post.save()

        return redirect('home')  # Перенаправление на страницу успешного добавления записи

    return render(request, 'blog/create.html')