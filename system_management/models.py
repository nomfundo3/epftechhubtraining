from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from system_management import constants
from django.utils import timezone
from system_management import constants


class Usertype(models.Model):
    type = models.CharField(max_length=100)

class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('first_name', first_name)
        extra_fields.setdefault('last_name', last_name)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
 
        try:
            user_type_id = Usertype.objects.get(type=constants.ADMIN).id

        except ObjectDoesNotExist:
            raise ValueError(_('​{constants.ADMIN}​ role not found'))
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type_id', user_type_id)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email=email, password=password, **extra_fields)
        return user   
    

    
class User(AbstractUser):
    """A model that represents a user of the application."""

    username = None
    email = models.EmailField(max_length=255, unique=True)
    is_first_login = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    user_type = models.ForeignKey(Usertype, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + self.last_name

class Profile(models.Model):
    identity_number = models.CharField(max_length=13, unique=True, blank=True)
    passport_number = models.CharField(max_length=9, unique=True ,blank=True)
    date_of_birth = models.DateField(blank=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10, unique=True)
    is_suspended = models.BooleanField(default=False)
    is_profile_completed = models.BooleanField(default=False)
    gender = models.CharField(max_length=100)
    ethnicity = models.CharField(max_length=100)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Otp(models.Model):
    otp = models.CharField(max_length=4)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Type(models.Model):
    type = models.CharField(max_length=100)


class Attempts(models.Model):
    no_attempts = models.IntegerField(default=0)
    last_update = models.DateTimeField(auto_now=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ManagerClerk(models.Model):
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager')
    clerk = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clerk')


