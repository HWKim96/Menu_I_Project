from django.db import models
from datetime import datetime # 현재시각 집어넣기
from django.contrib.auth.models import AbstractUser #Django에서 제공하는 모델 클래스 사용자 인증(authentication)과 관련된 필드

# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **kwargs):
#         user = self.model(username=username, **kwargs)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password, **kwargs):
#         user = self.create_user(username, password, **kwargs)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    birth = models.DateField(default=datetime.today)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username' #인증 시스템에서 사용자를 식별하기 위한 필드를 지정하는 클래스 변수

    # # objects = UserManager()

    # def __str__(self):
    #     return self.username

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     return self.is_admin
