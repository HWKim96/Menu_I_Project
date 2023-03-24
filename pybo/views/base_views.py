from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from ..models import Question


# Create your views here.
def index(request):
    '''
    pybo 목록 출력
    '''
    # 입력인자
    page = request.GET.get('page','1') # 페이지
    # get방식 요청 >> localhost:8000/pybo/?page=1 이런식으로 뒤에 붙는 형식??
    
    # 조회
    question_list = Question.objects.order_by('-create_date')
    # Django에서 Question 모델을 가진 데이터베이스에서 
    # 모든 Question 객체를 create_date 속성의 역순으로 정렬하여 가져오는 쿼리셋을 생성합니다.
    
    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'question_list': page_obj}
    # context 는 render에 인자로 보낼 데이터를 변수로 저장하는 것
    # question_list 뷰 함수에서는 Question 모델에서 조회한 데이터를 page_obj로 페이징 처리하여 context 변수에 담아서 
    # render 함수의 인자로 전달합니다. 이렇게 전달된 context 변수는 pybo/question_list.html 템플릿에서
    # question_list 변수로 사용될 수 있습니다.
    #즉, context 변수는 뷰 함수에서 처리한 데이터나 조회한 데이터를 템플릿에서 사용할 수 있도록 전달하는 역할을 합니다.
    
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    return render(request, 'pybo/question_list.html', context)
    # question_list를 pybo/question_list.html에 적용하여 html코드로 변환해줌 render~
    # 장고는 pybo/question_list.html이런 파일을 템플릿이라 한다.
    
def detail(request, question_id):
    '''
    pybo 내용 출력
    '''
    question = get_object_or_404(Question, pk = question_id)
    # Django에서 Question 모델을 가진 데이터베이스에서 
    # question_id가 id인 Question 객체를 가져온다.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)