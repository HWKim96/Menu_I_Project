from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import easyocr
import numpy as np
import requests
import json
import mysql.connector
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re

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
        # print(ocr)
        # 문자열 병합과정 여러개로 떨어진 하나의 음식 음절을 붙이는 과정
        text = []
        for i in range(len(ocr)):
            text.append(ocr[i][1])
        # item 변수의 두번째 요소 출력 
        # item.0은 텍스트 좌표, item.1은 출력 text, item.2는 신뢰도(정확도)
        
        join_str = ''.join(text)
        join_str = join_str.replace(' ', '')
        print(join_str) # ocr 인식 결과
        
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        # 번역 api 기능 추가
        client_id = "id"
        client_secret = "pw"
        url = "https://openapi.naver.com/v1/papago/n2mt"
        # Naver Developers에서 papago api를 불러와 사용하기
        
        source = "ko"  # 번역할 언어
        # 번역할 파파고 언어: ko(한국어), en(영어), ja(일본어), zh-CN(중국어-간체))
        target = "ja" 
        # 가져올 SQL 언어: ko(한국어), en(영어), ja(일본어), cn(중국어)
        lang = 'ja'
        
        
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
        # print(result)
        translated_text = result["message"]["result"]["translatedText"]
        # result 안에 message 객체 안 result 객체 안 translatedText (결과) 가져옴
        print(translated_text)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------#
        search_engine_id = 'id'
        api_key = 'key'
        query = join_str
        url_pattern = re.compile(r'.+\.jpg$')
        query_url = f'https://www.googleapis.com/customsearch/v1?key={"AIzaSyC7_uu_Oo1YDBf7A5KreKuSmsIp57NnqJM"}&cx={"823d1386e3906483b"}&q={query}&searchType=image'
        img_response = requests.get(query_url).json()
        
        image_links = []
        error_message = ""
        try:
            for item in img_response['items']:
                image_link = item['link']
                if url_pattern.match(image_link):
                    image_links.append(image_link)
                if len(image_links) >= 3:
                    break
        except KeyError:
            error_message = "Google doesn't have an image. There is a possibility that the character recognition is incorrect. Please take a picture again."
                

        print(image_links)
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------#
        # MySQL에서 DB 정보 가져오기
        
        # MySQL Connection
        conn = mysql.connector.connect(user='menui', password='0000', 
                                        host='localhost', database='menui',
                                        port='3306')
        
        # Connection으로부터 Cursor 생성
        cur = conn.cursor()
        
        
        # menu table에서 음식(join_str) 정보 가져오기
        
        
        # 만약 MySQL에서 정보가 있다면 DB에서 가져오고 없다면 except를 통해 예외처리
        try:
            # 선택된 언어에 대한 이름과 재료 정보 가져옴
            # lang은 번역 api 추가하는 부분에서 변수 할당함 line.45
            cur.execute(f"SELECT menu_name_{lang}, menu_explain_{lang} FROM menu WHERE menu_name_ko='{join_str}'")

            # 결과값 전부 가져오기
            rows = cur.fetchall()
            # print(rows)

            # 두 결과값에 대한 변수 할당, 0번 자리에 튜플로 되어있음
            sql_menu_name = rows[0][0]
            sql_menu_info = rows[0][1]
        
        except:
            sql_menu_name = None
            sql_menu_info = None
            # 만약 SQL에 DB가 없어 에러가 발생했을 경우에 예외처리를 통해 None 할당
        
        
        # 아직까지는 음식 하나에 대한 정보만 추출하는 방법을 사용함
        # 메뉴판에서 여러 음식에 대한 정보를 가져오게 될 경우 방법을 수정
        # for문 이용해야할 것


        return render(request, 'ocr/result.html', 
                    {'join_str': join_str, 'translated_text': translated_text,
                    'sql_menu_name': sql_menu_name, 'sql_menu_info': sql_menu_info, 'image_links': image_links, 'error_message': error_message})
                    # join_str과 translated_text를 dict 형태로 result.html로 return
                    # 추가 변수를 return할 때 뒤에 key, value 형식으로 추가하면 됨
    else:
        return HttpResponse('잘못된 요청입니다.')
        # POST 요청이 아닐 경우 출력