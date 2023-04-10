from django.apps import AppConfig #AppConfig 클래스를 가져오기


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' # 데이터 타입 지정(64-bit 범위의 정수 값)
    name = 'common'
