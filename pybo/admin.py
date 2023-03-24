from django.contrib import admin

# Register your models here.
from .models import Question, Answer
# from common.models import User




class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']  # 제목으로 질문을 검색 할 수 있도록 검색항목 추가


admin.site.register(Question, QuestionAdmin)# admin페이지에 질문 칸 넣기?
admin.site.register(Answer)
# admin.site.register(User)
