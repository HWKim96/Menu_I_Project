from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import easyocr
import numpy as np
import requests
import json
import mysql.connector
# from googleapiclient.discovery import build
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
        
        text = [] # text가 인식된 언어들 묶여있음 ex)['군고구마', '1개', '1900원', '1봉지3개) 5000원'] 대체로 언어들도 잘 인식함
        for i in range(len(ocr)):
            text.append(ocr[i][1])
        # item 변수의 두번째 요소 출력 
        # item.0은 텍스트 좌표, item.1은 출력 text, item.2는 신뢰도(정확도)
        pattern = re.compile(r'^[가-힣\s]+$') #글자와 공백으로만 구성된 요소가 나오게 정규식 작성
        text_str = [item for item in text if pattern.match(item)]
        # join_str = ''.join(text_str) #text 리스트안의 요소를 하나로 합치고 리스트한에 있지도 않고 그냥 str나옴
        # join_str = text_str[0] # 테스트용
        join_str = text_str # 테스트용
        # join_str = join_str.replace(' ', '') #리스트로 묶이면 공백 제거 안됨 포문 돌려서 공백 제거하자
        join_str = [item.replace(' ', '') for item in join_str] # 공백 제거 코드
        # print(join_str) # ocr 인식 결과
        
        #---------------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        # 번역 api 기능 추가
        client_id = "NkW4rbvtGrF5MVmXZxwI"
        client_secret = "m72SSS_JtB"
        url = "https://openapi.naver.com/v1/papago/n2mt"
        # Naver Developers에서 papago api를 불러와 사용하기
        
        source = "ko"  # 번역할 언어
        
        # 번역할 파파고 언어: ko(한국어), en(영어), ja(일본어), zh-CN(중국어-간체))
        # target = "ja" 
        
        # 가져올 SQL 언어: ko(한국어), en(영어), ja(일본어), cn(중국어)
        # lang = 'ja'
        language = request.POST.get('language')
        if language == 'en':
            target = 'en'
            lang = 'en'
        elif language == 'ja':
            target = 'ja'
            lang = 'ja'
        elif language == 'cn':
            target = 'zh-CN'
            lang = 'cn'
        
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
        translated_text = translated_text.replace('、', ',')
        translated_text = translated_text.split(",")
        # print(translated_text)
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------#
        search_engine_id = '24ce2daf3f88f4e84' 
        api_key = 'AIzaSyAjJPW-7MQO3mou1wQ_xfmsfQaUTZ-PB0M'
        join_str
        
        url_pattern = re.compile(r'.+\.jpg$')

        error_message = None
        
        # MySQL에서 DB 정보 가져오기
        
        # MySQL Connection
        conn = mysql.connector.connect(user='menui', password='0000', 
                                        host='localhost', database='menui',
                                        port='3306')
        
        # Connection으로부터 Cursor 생성
        cur = conn.cursor()
        
        sql_name_list = []
        sql_info_list = []
        images_link = []
    
        for text in join_str:
            # SQL 정보 가져오기
            # menu table에서 음식(join_str) 정보 가져오기   
            # 만약 MySQL에서 정보가 있다면 DB에서 가져오고 없다면 except를 통해 예외처리
            try:
                # 선택된 언어에 대한 이름과 재료 정보 가져옴
                # lang은 번역 api 추가하는 부분에서 변수 할당함 line.45
                cur.execute(f"SELECT menu_name_{lang}, menu_explain_{lang} FROM menu WHERE menu_name_ko='{text}'")
                # print(query)

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
            
            # 이미지 링크 변수 할당
            query_url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={text}&searchType=image'
            
            # 이 과정이 있어야 이미지의 대한 정보를 가져올 수 있음
            img_response = requests.get(query_url).json()
            
            try:
                # json은 딕셔너리의 형태를 가지고 있음 img_response의 keys 중 items의 요소 내에서
                # item['link'] keys의 대한 value가 image_link에 해당함
                items_list = img_response['items']
                img_links = [item['link'] for item in items_list if url_pattern.match(item['link'])][:3]
                images_link.append(img_links)
                
            except KeyError:
                error_message = f'{text}에 해당하는 링크를 찾지 못했습니다.'
            
            sql_name_list.append(sql_menu_name)
            sql_info_list.append(sql_menu_info)
            # print(sql_name_list)
            # print(sql_info_list)
            # print(images_links)
            
            # 아직까지는 음식 하나에 대한 정보만 추출하는 방법을 사용함
            # 메뉴판에서 여러 음식에 대한 정보를 가져오게 될 경우 방법을 수정
            # for문 이용해야할 것
            zip_result = list(zip(join_str, translated_text, sql_name_list, sql_info_list, images_link))
            # print(zip_result)
        
        return render(request, 'ocr/result.html', 
                    {'zip_result': zip_result, 'error_message': error_message})
                    # join_str과 translated_text를 dict 형태로 result.html로 return
                    # 추가 변수를 return할 때 뒤에 key, value 형식으로 추가하면 됨
    else:
        return HttpResponse('잘못된 요청입니다.')
        # POST 요청이 아닐 경우 출력