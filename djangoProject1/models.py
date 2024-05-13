
import random as rnd
from django.db import models
from django.contrib.auth.models import User,AbstractUser


class Account(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    bonuces = models.IntegerField(default=0)
    t2 = models.BooleanField(default=0)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)




    def __str__(self):
        return self.login  # Возвращает login в админке Django

    class Meta:
        db_table = 'account'  # Имя таблицы в базе данных



def gen_code(email):

    code = rnd.randrange(100,1000)
    print(f"Код для {email}: {code}")
    return code





class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='img/',default='img/default.jpg')

