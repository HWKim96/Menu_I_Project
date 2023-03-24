from django import forms
from django.contrib.auth.forms import UserCreationForm # 장고가 제공하는 기본적인 회원가입을 위한 폼
from .models import User

# 웹 애플리케이션에서 사용자로부터 입력을 받을 때, 
# 입력값의 유효성 검사나 처리를 위해서 사용되는 것을 '폼(Form)'이라고 합니다.

class UserForm(UserCreationForm):
    birth = forms.DateField(label="생년월일")
    email = forms.EmailField(label="이메일")
    number = forms.CharField(label="전화번호")
    address = forms.CharField(label="주소")
    detail_address = forms.CharField(label="상세주소")
    

    class Meta:
        model = User
        fields = ["username", "birth", "password1", "password2", "email", "number", "address","detail_address"]
        labels = {
            'username':'제목',
            'birth':'생년월일',
            'password1':'비밀번호',
            'password2':'비밀번호_확인',
            'email':'이메일',
            'number':'전화번호',
            'address':'주소',
            'detail_address':'상세주소',
            
        }