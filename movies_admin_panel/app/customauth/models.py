import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, user_name, password=None):
        if not user_name:
            raise ValueError('Users must have an user_name')

        user = self.model(user_name=user_name)
        if not password:
            password = self.make_random_password()
            # Тут можно отправить пароль по e-mail
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password=None):
        user = self.create_user(user_name=user_name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(verbose_name='Логин', max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)

    # строка с именем поля модели, которая используется в качестве уникального идентификатора
    USERNAME_FIELD = 'user_name'

    # менеджер модели
    objects = MyUserManager()

    def __str__(self):
        return f'{self.user_name} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
