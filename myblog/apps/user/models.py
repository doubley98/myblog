from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Users(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号码")

    class Meta:
        db_table = "users"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
