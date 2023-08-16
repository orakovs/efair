from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, iin, password, **additional_fields):
        if not iin:
            raise ValueError('Введите имя пользователя')
        user = self.model(iin=iin, **additional_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, iin, password, **additional_fields):
        additional_fields.setdefault('is_staff', True)
        additional_fields.setdefault('is_superuser', True)
        return self.create_user(iin, password, **additional_fields)