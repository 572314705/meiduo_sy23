from django.db import models


from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # 继承后默认的属性和方法都有
    """自定义用户模型类"""
    #　手机类
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    class Meta:
        #  指定表名
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name