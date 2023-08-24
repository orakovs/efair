from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpRequest, JsonResponse
from .forms import *
from .models import *


# все что связано с отображением страниц
def homeView(request):  #, offer_id=None
    # offer = None
    offers = OfferSale.objects.all().order_by('-datetime')
    paginator = Paginator(offers, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})
    
    # data = [{
    #     'image': offer.image,
    #     'title': offer.title,
    #     'description': offer.description,
    #     'amount': offer.amount,
    #     'price': offer.price,
    #     } for offer in offers]
    
    # if offer_id is not None:
    #     offer = get_object_or_404(OfferSale, pk=offer_id)
    
    # if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    #     return JsonResponse(data, safe=False)
    
    # return render(request, 'home.html', {'offers': offers, 'offer': offer})
 

# def latestOffer(request):
#     offers = OfferSale.objects.order_by('-datetime')
#     paginator = Paginator(offers, 3)
    
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'home.html', {'page_obj': page_obj})


@login_required(login_url='login_url')
def cabinetView(request):
    user = request.user
    offers = OfferSale.objects.filter(salesman=user).order_by('-datetime')
    for offer in offers:
        offer.count = len(OfferBuy.objects.filter(sale=offer).filter(in_active=True))
    context = {
        'user': user,
        'this_url': 'cabinet_url',
        'offers': offers,
    }
    return render(request, 'cabinet.html', context)


def offersView(request, category_id=None):
    categories = Category.objects.all()
    selected_category = None
    offers = OfferSale.objects.all().order_by('-datetime')
    
    query = request.GET.get('q')
    
    if query:
        offers = offers.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        offers = offers.filter(category=selected_category)
    context = {
        'categories': categories,
        'offers': offers,
        'selected_category': selected_category,
        'search_query': query
        }
    return render(request, 'offers.html', context)


def offerDetailView(request, offer_id):
    offer = get_object_or_404(OfferSale, pk=offer_id)
    categories = Category.objects.all()
    context = {
        'offer': offer,
        'categories': categories
        }
    return render(request, 'offer_detail.html', context)


@login_required
def createOfferView(request):
    if request.method == 'POST':
        form = OfferSaleCreationForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.salesman = request.user
            form.save()
            return redirect('cabinet_url')
    else:
        form = OfferSaleCreationForm()
    context = {
        'form': form,
        }
    return render(request, 'offer_create.html', context)


@login_required
def deleteOfferView(request, offer_id):
    offer = get_object_or_404(OfferSale, pk=offer_id)
    if request.user == offer.salesman:
        if request.method == 'POST':
            offer.delete()
            return redirect('offers_url')
        return render(request, 'offer_delete.html', {'offer': offer})


@login_required
def editOfferView(request, offer_id):
    offer = get_object_or_404(OfferSale, pk=offer_id)
    if request.user == offer.salesman:
        if request.method == 'POST':
            form = OfferSaleChangeForm(request.POST, request.FILES, instance=offer)
            if form.is_valid():
                form.save()
                return redirect('offer_url', offer_id=offer_id)
        else:
            form = OfferSaleChangeForm(instance=offer)
        context = {
            'form': form,
            'offer': offer,
            }
        return render(request, 'offer_edit.html', context)


def createOfferBuyView(request, offer_id):
    offer = get_object_or_404(OfferSale, pk=offer_id)
    
    if request.method == 'POST':
        form = OfferBuyForm(request.POST)
        if form.is_valid():
            offer_buy = form.save(commit=False)
            offer_buy.sale = offer
            offer_buy.buyer = request.user
            offer_buy.save()
            return redirect('offers_url')  # Измените на нужный URL
    else:
        form = OfferBuyForm()
    
    context = {'form': form, 'offer': offer}
    return render(request, 'offer_buy_create.html', context)


def offerBuyView(request, offer_id):
    offer_sale = get_object_or_404(OfferSale, pk=offer_id)
    offers_buy = OfferBuy.objects.filter(sale=offer_sale).filter(in_active=True).order_by('-datetime')
    
    return render(request, 'offers_buy.html', {'offers_buy': offers_buy})


def offerAccept(request):
    if request.method == 'POST':
        offer_buy = OfferBuy.objects.get(id=request.POST.get('offer_buy_id'))
        offer_sale = OfferSale.objects.get(id=request.POST.get('offer_buy_id'))
        offer_buy.in_active = False
        offer_buy.save()
    return redirect('offers_buy_url', offer_id=request.POST.get('offer_sale_id'))


def offerDecline(request):
    if request.method == 'POST':
        offer = OfferBuy.objects.get(id=request.POST.get('offer_buy_id'))
        offer.in_active = False
        offer.save()
    return redirect('cabinet_url')


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
        street = request.POST.get('street')
        home_number = request.POST.get('home_number')
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
            street=street,
            home_number= home_number,
            phone=phone,
            password=password1
            )
                        
        return redirect('login_url')
    
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form,})

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