from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.utils import timezone
from .managers import CustomUserManager
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser, PermissionsMixin):
    iin = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=128)
    city = models.CharField(max_length=64)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{12}$',
        message='Номер телефона должен быть в международном формате: +77011234567'
    )
    phone = models.CharField(validators=[phone_regex], max_length=12)
    avatar = models.ImageField(upload_to='static\profile_photo', default='img\default_avatar.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()