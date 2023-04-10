from django.contrib import admin # 관리자사이트에 액세스
from common.models import User # common.models에서 user모델을 가져옴

# Register your models here.
admin.site.register(User) # 가져온 user 모델을 관리자사이트에 등록 이를 통해 관리자 사이트에서 user모델을 관리할 수 있음
