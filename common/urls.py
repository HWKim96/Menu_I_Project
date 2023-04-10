from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

# Django의 namespace 기능을 사용하기 위해 app_name 변수에 'common' 지정
app_name = 'common'
# URL 패턴에 대한 경로 및 뷰 함수 지정
urlpatterns = [
     # 로그인 페이지에 대한 URL 패턴
    # auth_views.LoginView를 사용하여 로그인 뷰 처리
    # template_name 인수로 common/login.html 템플릿 파일 사용
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # 로그아웃 페이지에 대한 URL 패턴
    # auth_views.LogoutView를 사용하여 로그아웃 뷰 처리
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 회원 가입 페이지에 대한 URL 패턴
    # views.signup 뷰 함수를 사용하여 회원 가입 처리
    path('signup/', views.signup, name='signup'),
] 
