from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from .validators import *
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        error_messages={'unique': "이미 사용중인 닉네임입니다."},
        validators=[validate_no_special_characters]
    )

    kakao_id = models.CharField(
        max_length=20,
        null=True,
        validators=[validate_no_special_characters]
    )

    address = models.CharField(
        max_length=40,
        null=True,
        validators=[validate_no_special_characters]
    )

    def __str__(self):
        return self.email


class Post(models.Model):
    title = models.CharField(max_length=60)
    item_price = models.IntegerField()

    CONDITION = [
        (1, '새제품'),
        (2, '최상'),
        (3, '상'),
        (4, '중'),
        (5, '하'),
    ]

    item_condition = models.IntegerField(choices=CONDITION)
    item_details = models.TextField(null=True)
    image1 = models.ImageField(upload_to='item_pics')
    image2 = models.ImageField(upload_to='item_pics', blank=True)
    image3 = models.ImageField(upload_to='item_pics', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
