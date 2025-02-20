# from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.core.validators import RegexValidator
# from django.db import models
#
#
# from django.contrib.auth.models import PermissionsMixin, Group, Permission
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.core.validators import RegexValidator
# from django.db import models
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, phone, password=None, **extra_fields):
#         if not phone:
#             raise ValueError('The Phone number must be set')
#         user = self.model(phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, phone, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_admin', True)
#         extra_fields.setdefault('is_superuser', True)  # to'g'ri qiymat qo'yildi
#         return self.create_user(phone, password, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
#                                  message="Phone number must be entered in the format: '998900404001'. Up to 14 digits allowed.")
#     phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_user = models.BooleanField(default=False)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     username = None
#
#     groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
#     user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)
#
#     USERNAME_FIELD = 'phone'
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.phone
#
#     def has_perm(self, perm, obj=None):
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         return self.is_admin
#
#
# class Movie(models.Model):
#     name = models.CharField(max_length=150)
#     year = models.IntegerField()
#     imdb = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
#     genre = models.CharField(max_length=50, )
#     actor = models.ManyToManyField('Actor')
#
#     def __str__(self):
#         return self.name
#
#
# class Actor(models.Model):
#     gender = (
#         ('m', 'man'),
#         ('w', 'woman'),
#     )
#
#     name = models.CharField(max_length=150)
#     birthdate = models.DateField()
#     gender = models.CharField(max_length=10, choices=gender, default='man')
#
#     def __str__(self):
#         return self.name
#
#
# class Comment(models.Model):
#     movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField()
#     create_date = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.text

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


# User model
class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '9989012345678'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=18, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class User2(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class TokenModel(models.Model):
    date = models.DateField()
    token = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)


from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Movie(models.Model):
    name = models.CharField(max_length=150)
    year = models.IntegerField()
    imdb = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    genre = models.CharField(max_length=50, )
    actor = models.ManyToManyField('Actor')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Movie"
        verbose_name_plural = "Movies"


class Actor(models.Model):
    gender = (
        ('m', 'man'),
        ('w', 'woman'),
    )

    name = models.CharField(max_length=150)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices=gender, default='man')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"


class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
