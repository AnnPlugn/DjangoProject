from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError



def newsignup(request):
    if request.method == "POST":
        if request.POST.get('password1') == request.POST.get('password2'):
            try:

                saveuser = User.objects.create_user(request.POST.get('username'), password=request.POST.get('password1'))
                saveuser.save()
                return render(request, 'Index.html', {"form": UserCreationForm(), "info": "The User " + request.POST.get(
                'username') + "is Created Successfully...!"})
            except IntegrityError:
                return render(request, 'Index.html',
                              {"form": UserCreationForm(), "error": "The User " + request.POST.get(
                                  'username') + "is Already Exist ...!"})
        else:
            return render(request, 'Index.html',
                          {"form": UserCreationForm(), "error": "The Passwords are not matching"})
    else:
        return render(request, 'Index.html', {"form": UserCreationForm})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'Index.html', {"form": AuthenticationForm(), "info": "Login Successful"})
        else:
            return render(request, 'Index.html', {"form": AuthenticationForm(), "error": "Invalid username or password"})
    else:
        return render(request, 'Index.html', {"form": AuthenticationForm()})

