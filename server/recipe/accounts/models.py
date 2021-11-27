from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValidationError('User must have an Email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        if not email:
            raise ValidationError('User must have an Email address')
        user = self.create_user(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if not email:
            raise ValidationError('User must have an Email address')
        user = self.create_user(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(verbose_name='Email Address', unique=True)
    username = models.CharField(verbose_name='Username', max_length=40, blank=True, null=True)
    first_name = models.CharField(verbose_name='First Name', max_length=40)
    last_name = models.CharField(verbose_name='Last Name', max_length=40, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='Date Joined', auto_now_add=True)
    is_admin = models.BooleanField(verbose_name='Admin User', default=False)
    is_staff = models.BooleanField(verbose_name='Staff User', default=False)
    is_superuser = models.BooleanField(verbose_name='Super User', default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True 
    
    def save(self, *args, **kwargs):
        self.username = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)

    @property
    def get_fullname(self):
        self.last_name = self.last_name if self.last_name else ''
        return f'{self.first_name} {self.last_name}'