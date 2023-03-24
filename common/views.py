from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from common.models import User
from common.forms import UserForm


from django.contrib.auth.hashers import make_password

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 폼에서 입력받은 데이터를 새로운 User 모델 객체에 저장
            user = User(
                username=form.cleaned_data.get('username'),
                password=make_password(form.cleaned_data.get('password1')),  # 비밀번호 해싱
                birth=form.cleaned_data.get('birth'),
                email=form.cleaned_data.get('email'),
                number=form.cleaned_data.get('number'),
                address=form.cleaned_data.get('address'),
                detail_address=form.cleaned_data.get('detail_address'),
            )
            user.save()  # 저장

            # 사용자 인증 및 로그인
            authenticate_and_login(request, user)

            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'common/signup-index.html', {'form': form})

def authenticate_and_login(request, user):
    authenticated_user = authenticate(request, username=user.username, password=user.password)
    if authenticated_user is not None:
        login(request, authenticated_user)


