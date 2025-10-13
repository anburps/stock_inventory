from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email=None,phone_number=None,password=None,**extra_fields):
        if not email and not phone_number:
            raise ValueError('Email or phone number is required')
        user = self.model(email=email,phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email=None,phone_number=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email=email,phone_number=phone_number,password=password,**extra_fields)
    

class User(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=15,unique=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']
    
    objects = UserManager()     
    
    def __str__(self):
        return self.email or self.phone_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.username or self.user.email
