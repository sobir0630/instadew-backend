from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Tizimdagi foydalanuvchilarni boshqarish uchun maxsus foydalanuvchi modeli.
    
    Elektron pochta va foydalanuvchi nomi orqali autentifikatsiyani qo'llab-quvvatlaydi.
    AbstractBaseUser parollarni boshqarishni, PermissionsMixin esa 
    guruhlar va ruxsatnomalar tizimini ta'minlaydi.

    Attributes:
        email (EmailField): Foydalanuvchining noyob elektron pochta manzili.
        username (CharField): Foydalanuvchining noyob identifikatori.
        full_name (CharField): Foydalanuvchining to'liq ismi (ixtiyoriy).
        password (CharField): Foydalanuvchining paroli.
        cnf_password (CharField): Parolni tasdiqlash maydoni.
        is_staff (BooleanField): Foydalanuvchining admin panelga kirish huquqi.
        is_active (BooleanField): Foydalanuvchi hisobi faollik holati.
        created_at (DateTimeField): Ro'yxatdan o'tgan vaqti.
    """
    email        = models.EmailField(unique=True)
    username     = models.CharField(max_length=50, unique=True)
    full_name    = models.CharField(max_length=150, null=True, blank=True)
    password     = models.CharField(max_length=130)
    # Ijtimoiy tarmoq uchun kerakli maydonlar
    avatar = models.ImageField(upload_to='avatars/user/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)
    # Statistika (Bularni bazada saqlash yuklamani kamaytiradi)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)
    # Qo'shimcha ma'lumotlar
    is_private = models.BooleanField(default=False)
    active_status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    # custom user sozlamalari
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "full_name"]

class UserLogin(models.Model):
    """_
        Foydalanuvchi login ma'lumotlarini saqlash uchun model.
    Args:
        username (CharField): Foydalanuvchining login uchun ishlatiladigan nomi.
        password (CharField): Foydalanuvchining login uchun ishlatiladigan paroli.
    """
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=130)
