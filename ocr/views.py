from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import easyocr
import numpy as np
import requests
import json


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
        ocr = reader.readtext(img_np)
        
        # 문자열 병합과정 여러개로 떨어진 하나의 음식 음절을 붙이는 과정
        text = []
        for i in range(len(ocr)):
            text.append(ocr[i][1])
        # item 변수의 두번째 요소 출력 
        # item.0은 텍스트 좌표, item.1은 출력 text, item.2는 신뢰도(정확도)
        
        join_str = ''.join(text)
        print(join_str)
        
        # 번역 api 기능 추가
        client_id = "Naver Developers_Papago_api_ID"
        client_secret = "Naver Developers_Papago_api_password"
        url = "https://openapi.naver.com/v1/papago/n2mt"
        # Naver Developers에서 papago api를 불러와 사용하기
        
        source = "ko"  # 번역할 언어
        target = "en"  # 번역 결과 언어, 현재는 영어 선택이지만 차후 연동할 것
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        } # 여기는 요청 클라이언트 ID, Secret 받는 곳, key : value dict 형태로 Id, Secret 입력

        data = {
            "source": source,
            "target": target,
            "text": join_str,
        } # 번역 언어, text를 data dict 형태로 지정
        
        response = requests.post(url, headers=headers, data=data)
        # request를 통해서 json 형식으로 파일 받아옴
        result = json.loads(response.text)
        translated_text = result["message"]["result"]["translatedText"]
        # result 안에 message 객체 안 result 객체 안 translatedText (결과) 가져옴

        return render(request, 'result.html', 
                    {'join_str': join_str, 'translated_text': translated_text})
                    # join_str과 translated_text를 dict 형태로 result.html로 return
                    # 추가 변수를 return할 때 뒤에 key, value 형식으로 추가하면 됨
    else:
        return HttpResponse('잘못된 요청입니다.')
        # POST 요청이 아닐 경우 출력