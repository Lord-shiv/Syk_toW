from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.contrib.auth.models import PermissionsMixin
from django_resized import ResizedImageField


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("User must have a username")
        user_obj = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user_obj.set_password(password)  # change user password
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, username, password):
        user_obj = self.create_user(
            email,
            username=username,
            password=password,
        )

        user_obj.is_staff = True
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, username, password):
        user_obj = self.create_user(
            email,
            username=username,
            password=password,
        )
        user_obj.is_admin = True
        user_obj.is_staff = True
        user_obj.is_active = True
        user_obj.save(using=self._db)
        return user_obj


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(
        max_length=255, null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=False)  # can login
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    is_admin = models.BooleanField(default=False)  # superuser
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(
        verbose_name='last login', auto_now=True, null=True, blank=True)
    profile_image = ResizedImageField(
        upload_to='images/profile_pics/', default='images/profile_pics/default_icon.png', quality=70, crop=['middle', 'center'], size=[320, 320], blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    hide_email = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_email(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True  # self.admin

    def has_module_perms(self, app_label):
        return True

    def get_profile_image_path(self):
        return 'media/' + str(self.profile_image)

    @property
    def _is_staff(self):
        return self.is_staff

    @property
    def _is_admin(self):
        return self.is_admin

    @property
    def _is_active(self):
        return self.is_active