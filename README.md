# Menu "I"
<br>

## 목차
- #### 프로젝트 개요
	- ##### 1. 팀 소개
	- ##### 1. 팀 소개
	- ##### 1. 팀 소개
- #### 모델 생성
- #### RMSE 분석

<br>

## predict future sales 분석

<p align="justify">

### 간트 차트

<img width="100%" src="https://user-images.githubusercontent.com/98474997/221078422-9b52b0bb-a385-439d-b0a3-9b014f8b8eaa.png"/>

<br>

### 프로젝트 개요

#### 1. 목적
- 과거 판매량 데이터를 기반으로 향후 판매량을 예측하는 것

#### 2. 목표
- 2013년 1월부터 2015년 10월까지의 물품 정보 및 판매량 분석
- 2015년 11월 물품의 판매량을 예측

#### 3. 팀내 역할
<table border="1">
	<th>이름</th>
	<th>역할</th>
	<tr>
	    <td>김현우(팀장)</td>
	    <td>모델링, 프로젝트 총괄</td>
	</tr>
	<tr>
	    <td>김하율(팀원)</td>
	    <td>모델링</td>
	</tr>
	<tr>
      	    <td>김동석(부팀장)</td>
	    <td>데이터 전처리</td>
	</tr>
	    <td>강무경(팀원)</td>
	    <td>데이터 전처리</td>
	<tr>
            <td>김동진(팀원)</td>
	    <td>데이터 전처리</td>
	</tr>
</table>
</p>

<p align="center">
</p>

<br>

## 기술 스택
<p>
	
#### Python
	
</p>
<br>

## 구현 특성

- #### 도시 정보
- #### 월별 판매갯수
- #### 개별(1,2), 분기(3), 상/하반기(6), 년(12) 이전 평균 판매갯수
- #### 아이템 카테고리
- #### 아이템 (메인/서브) 카테고리
- #### 날짜(년/월/일) 정보

<br>

## 모델링

- #### Light GBM
- #### XGBoost

<br>

### 결과

**Light GBM**

- training's rmse : 0.71708
- validation's rmse : 0870725

<img width="100%" src="https://user-images.githubusercontent.com/126048063/221100733-9b9d485c-61f8-4e18-94c3-9b0cc1965101.png"/>

**XGBoost**

- training's rmse : 0.72325
- validation's rmse : 0.86835

<img width="100%" src="https://user-images.githubusercontent.com/126048063/221100739-1cd3d19d-dc01-4f6b-965d-b794810d1081.png"/>

<br>

## 배운 점 & 아쉬운 점

<p align="justify">

#### 1. 더 많은 feature를 시도해보지 못한 점<br>
#### 2. 더 많은 모델을 적용해보지 못한 점<br>
#### 3. 과적합 해결을 하지 못한 점
<hr>

#### 1. 전처리의 전반적인 흐름을 배울 수 있었음<br>
#### 2. 모델링을 더욱 깊게 공부할 기회를 얻음<br>
#### 3. 협업의 중요성을 배울 수 있었음<br>

</p>

<br>
