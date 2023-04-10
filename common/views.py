from django.shortcuts import render, redirect # Django에서 제공하는 함수들을 불러옵니다.
# from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login # Django에서 제공하는 인증 관련 함수들을 불러옵니다.
from common.models import User # User 모델을 불러옵니다.
from common.forms import UserForm # UserForm 폼을 불러옵니다.
 

from django.contrib.auth.hashers import make_password # 비밀번호 해싱을 위한 함수를 불러옵니다.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST) # UserForm에서 클라이언트가 보낸 데이터를 가져옵니다.
        if form.is_valid(): # 폼형식이 맞으면 
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
            user.set_password(form.cleaned_data.get('password1')) # 비밀번호 설정
            user.save()  # User 모델 객체를 데이터베이스에 저장합니다.

            # 사용자 인증 및 로그인
            authenticate_and_login(request, user) # 사용자를 인증하고 로그인합니다.

            return redirect('home') # 회원가입이 완료되면 'home'으로 이동합니다.
    else:
        form = UserForm() # 클라이언트가 GET 요청을 보낸 경우, 빈 회원가입 폼을 생성합니다.
    return render(request, 'common/signup-index.html', {'form': form}) # 회원가입 폼을 렌더링하여 반환합니다.

def authenticate_and_login(request, user):
    # 입력받은 정보를 인증하고 로그인을 시도함
    authenticated_user = authenticate(request, username=user.username, password=request.POST['password1'])
    if authenticated_user is not None: # 사용자 인증에 성공한 경우
        login(request, authenticated_user) # 로그인
        
        
'''
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
            user = authenticate(request, username=user.username, password=user.password)
            login(request, user)

            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'common/signup-index.html', {'form': form})
'''


