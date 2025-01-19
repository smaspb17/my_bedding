from django.apps import apps
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создание и сохранение пользователя с уникальным email
        """
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Ленивая загрузка модели Profile
        Profile = apps.get_model('users', 'Profile')
        Profile.objects.create(user=user)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создание суперпользователя с email и паролем
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)