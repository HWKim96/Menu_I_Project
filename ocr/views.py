from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import easyocr
import numpy as np


def upload(request):
    if request.method == 'POST':
        # POST 요청 확인, 이미지 파일을 request.FILES에서 가져옴
        # POST는 클라이언트가 서버로 데이터 제출하는 것
        image = request.FILES['image']
        
        # Pillow 라이브러리
        img = Image.open(image)
        img_np = np.array(img)  # PIL Image 객체를 numpy 배열로 변환
        
        # easyocr 라이브러리
        reader = easyocr.Reader(['ko'])
        result = reader.readtext(img_np)
        
        text = []
        for i in range(len(result)):
            text.append(result[i][1])
        # item 변수의 두번째 요소 출력 
        # item.0은 텍스트 좌표, item.1은 출력 text, item.2는 신뢰도(정확도)
        
        join_str = ''.join(text)
        

        return render(request, 'result.html', {'result': join_str})
    else:
        return HttpResponse('잘못된 요청입니다.')