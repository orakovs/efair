from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


# все что связано с отображением страниц
def homeView(request):
    return render(request, 'home.html')


def cabinetView(request):
    user = request.user
    context = {
        'user': user,
        'this_url': 'cabinet_url',
    }
    return render(request, 'cabinet.html', context)


def offersView(request, category_id=None):
    categories = Category.objects.all()
    selected_category = None
    offers = OfferSale.objects.all()
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        offers = offers.filter(category=selected_category)
    context = {
        'categories': categories,
        'offers': offers,
        'selected_category': selected_category
        }
    return render(request, 'offers.html', context)


def offerDetailView(request, offer_id):
    offer = get_object_or_404(OfferSale, pk=offer_id)
    context = {
        'offer': offer
        }
    return render(request, 'offer_detail.html', context)


# все что связано с пользователем
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
            return redirect('cabinet_url')
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
        country = request.POST.get('country')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        avatar = request.POST.get('avatar')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not iin or not first_name or not last_name or not email or not country or not city or not phone:
            return render(request, 'signup.html', {'error_message': 'Заполните все поля!'})
        
        if password1 != password2:
            return render(request, 'signup.html', {'error_message': 'Введенные пароли не совпадают!'})

        CustomUser = get_user_model()
        user = CustomUser.objects.create_user(
            iin=iin, 
            first_name=first_name,
            last_name=last_name,
            email=email,
            country=country,
            city=city,
            phone=phone,
            password=password1
            )
                        
        return redirect('login_url')
    
    else:
        context = {'form': CustomUserCreationForm(), }
        return render(request, 'signup.html', context)

@login_required
def editProfileView(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('cabinet_url')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'edit_profile.html', {'form': form})