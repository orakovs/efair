from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    model = CustomUser
    list_display = ('iin', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('iin', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('iin', 'password', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('iin', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')
        })
    )
    search_fields = ('iin', 'date_joined',)
    ordering = ('iin', 'date_joined',)
        

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(OfferSale)
admin.site.register(OfferBuy)
admin.site.register(Manufactuter)
admin.site.register(OfferModel)
admin.site.register(Unit)