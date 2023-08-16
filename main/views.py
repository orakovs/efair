from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *


def homeView(request):
    return render(request, 'home.html')


def cabinetView(request):
    user = request.user
    context = {
        'user': user,
        'this_url': 'cabinet_url',
    }
    return render(request, 'cabinet.html', context)


def logoutView(request):
    logout(request)
    return redirect('home_url')


def loginView(request):
    if request.method == 'GET':
        context = {
            'this_url': 'cabinet_url',
        }
    else:
        iin = request.POST.get('iin')
        password = request.POST.get('password')
        user = authenticate(iin=iin, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_url')
        else:
            error_message = 'Неверные имя пользователя или пароль!'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html', context)
            

def signupView(request):
    if request.method == 'POST':
        iin = request.POST.get('iin')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        avatar = request.POST.get('avatar')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not iin or not first_name or not last_name or not email or not city or not phone:
            return render(request, 'signup.html', {'error_message': 'Заполните все поля!'})
        
        if password1 != password2:
            return render(request, 'signup.html', {'error_message': 'Введенные пароли не совпадают!'})

        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(iin=iin, password=password1)
                        
        return redirect('login_url')
    
    else:
        context = {'form': CustomUserCreationForm(), }
        return render(request, 'signup.html', context)