from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
# pybo는 게시판을 만드는 거래
class Question(models.Model): # 질문 모델 작성
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 계정이 삭제되면 질문도 삭제 
    subject = models.CharField(max_length=200) # 제목 최대 200자, max_length는 매개변수
    content = models.TextField() # 내용 
    create_date = models.DateTimeField() # 작성 일시 
    modify_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 계정이 삭제되면 질문도 삭제 
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # 질문이 삭제되면 답변도 삭제
    # 어떤 모델이 다른 모델의 속성을 이용하면 Foreignkey를 이용한다. 
    # cascade는 답변에 연결된 질문 삭제되면 답변도 삭제하라는 소리
    content = models.TextField() # 내용
    create_date = models.DateTimeField() # 작성일시
    modify_date = models.DateTimeField(null=True, blank=True)


# 모델을 변경한 후에는 반드시 makemigrations와 migrate를 통해 데이터베이스를 변경해 주어야 한다.  
