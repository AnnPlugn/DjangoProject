from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Compound, ModelTraining
from .forms import RegistrationForm, LoginForm
from .scraper.utils import extract_property_data, is_valid_url
from .predictor.predictor import predict_price
import pandas as pd

def home(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data', '')
        # Placeholder: Replace with actual model inference logic
        model_output = f"Анализ данных: {input_data}"
        return render(request, 'blog/home.html', {'model_output': model_output})
    return render(request, 'blog/home.html')

def about(request):
    return render(request, 'blog/about.html')

@login_required
def result(request):
    return render(request, 'result.html')

@csrf_exempt
def invoke_model(request):
    if request.method == 'POST':
        input_data = request.POST.get('input_data', '')
        # Placeholder: Replace with actual model inference logic
        model_output = f"Результат модели для: {input_data}"
        Compound.objects.create(
            name=input_data[:50],
            formula='N/A',
            description=model_output
        )
        return JsonResponse({'message': model_output})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def train_polynomial_regression_model(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        if not url:
            return render(request, 'blog/home.html', {'model_output': 'URL is required'})

        # Validate URL
        if not is_valid_url(url):
            return render(request, 'blog/home.html', {'model_output': 'Invalid URL format'})

        # Extract property data using the scraper
        property_data = extract_property_data(url)
        if property_data is None:
            return render(request, 'blog/home.html', {'model_output': 'Failed to scrape property data (possibly CAPTCHA or invalid page)'})

        # Convert scraped data to DataFrame for prediction
        df = pd.DataFrame([property_data])

        # Predict price
        predicted_price = predict_price(df)

        # Log the scraped data and prediction in ModelTraining
        ModelTraining.objects.create(
            model_type='Property Scraper with Prediction',
            metrics={
                'scraped_data': property_data,
                'predicted_price': predicted_price
            },
            dataset_info='CIAN Property Data'
        )

        # Render result page with data
        return render(request, 'result.html', {
            'data': property_data,
            'predicted_price': predicted_price
        })
    return render(request, 'blog/home.html')

@csrf_exempt
def train_sql(request):
    # Placeholder: Replace with actual training logic
    metrics = {'accuracy': 0.88, 'loss': 0.12}
    ModelTraining.objects.create(
        model_type='Gradient Boosting',
        metrics=metrics,
        dataset_info='Pharma dataset'
    )
    return JsonResponse({'message': 'Модель градиентного бустинга обучена'})

@csrf_exempt
def train_xgboost(request):
    # Placeholder: Replace with actual training logic
    metrics = {'accuracy': 0.90, 'loss': 0.10}
    ModelTraining.objects.create(
        model_type='XGBoost',
        metrics=metrics,
        dataset_info='Pharma dataset'
    )
    return JsonResponse({'message': 'Модель XGBoost обучена'})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            status = form.cleaned_data['status']
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                if status == 'admin':
                    group, _ = Group.objects.get_or_create(name='Admins')
                    user.groups.add(group)
                user.save()
                auth_login(request, user)
                return redirect('firstblog:home')
            except Exception as e:
                form.add_error(None, str(e))
        return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Set session expiry based on "remember me"
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires on browser close
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                return redirect('firstblog:home')
            else:
                form.add_error(None, 'Неверный логин или пароль')
                # Добавляем флаг для отображения ссылки на регистрацию
                return render(request, 'login.html', {'form': form, 'show_register': True})
        return render(request, 'login.html', {'form': form, 'show_register': True})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('firstblog:home')