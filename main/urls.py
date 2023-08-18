from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', homeView, name='home_url'),
    path('signup', signupView, name='signup_url'),
    path('cabinet', cabinetView, name='cabinet_url'),
    path('login', loginView, name='login_url'),
    path('logout', logoutView, name='logout_url'),
    path('edit_profile', editProfileView, name='edit_profile_url'),
    path('offers/', offersView, name='offers_url'),
    path('offers/<int:category_id>/', offersView, name='offers_url'),
    path('offer/<int:offer_id>/', offerDetailView, name='offer_url'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)