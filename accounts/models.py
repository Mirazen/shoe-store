from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("guest", "гость"),
        ("client", "клиент"),
        ("manager", "менеджер"),
        ("admin", "администратор"),
    ]
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLES, default="client")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
