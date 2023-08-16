from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('iin', 'first_name', 'email', 'city', 'phone', 'avatar')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('iin', 'first_name', 'email', 'city', 'phone', 'avatar')