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
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{11}$',
        message='Номер телефона должен быть в международном формате: +77011234567'
    )
    phone = models.CharField(validators=[phone_regex], max_length=12)
    avatar = models.ImageField(upload_to='static\profile_photo', default='img\default_avatar.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name 
    
    USERNAME_FIELD = 'iin'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()


class Category(models.Model):
    name = models.CharField(max_length=64)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.category


class OfferSale(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now=True)
    in_activ = models.BooleanField(default=True)
    salesman = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'    
    
    def __str__(self):
        return self.offer_name


class OfferBuy(models.Model):
    sale = models.ForeignKey(OfferSale, on_delete=models.CASCADE)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    datetime = models.DateTimeField(auto_now=True)
