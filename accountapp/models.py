from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        email = email.lower()
        first_name = first_name.title()

        user = self.model(email=self.normalize_email(email), first_name=first_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None):
        user = self.create_user(email=email, first_name=first_name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=255, verbose_name='Fast Name')
    hobby = models.CharField(max_length=255, verbose_name='Hobby')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name',)
    objects = CustomUserManager()

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        verbose_name_plural = 'Users'



