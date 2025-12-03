from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import check_password, make_password
class UserM(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('email req')
        user=self.model(email=email,**extra_fields)
        if password:
            user.password=make_password(password)
            user.save(using=self._db)
            return user
# Create your models here.
class RoleModel(models.Model):
    role_name = models.CharField(max_length=50)


class UserModel(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=128)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=UserM()
    @property
    def is_anonymous(self):
        return False
    @property
    def is_authenticated(self):
        return True
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self,raw_password):
        return check_password(raw_password,self.password)

    def __str__(self):
        return self.name

class NewsModel(models.Model):
    title = models.CharField(max_length=255)
    category=models.CharField(max_length=200)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
