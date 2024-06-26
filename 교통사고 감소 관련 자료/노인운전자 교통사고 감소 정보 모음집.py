'''
노인운전자 교통사고 감소를 위한 빅데이터 분석 자료 정리집
<차례>
<차례>
1.	타사 분석관련 유튜브 정보
2.	타사 교통사고 분석 참고 사이트
3.	뉴스 자료 참고 사이트 
4.	도로 데이터 조사 사이트
5.	날씨 정보 조사 사이트 
6.	경기도 운전면허증 소지 자료(출처)
7.	노인 자동차 운전자들의 운전실태, 운전 습관 및 안전성 자료(출처)
8.	주민등록인구현황 자료(출처)
9.	지도 시각화-수원시 자료(출처)
10.	선행기술 정보 


1. 타사 분석관련 유튜브 정보

> [1-12 컴공종설] 데이버분석을 통한 교통사고 예측(라온힐조)
https://youtube.com/watch?v=5nWHeKsP17I&si=C9R3Kr0hzB0DSk9l

> 서울시 빅데이터 캠퍼스 공모전, 빅데이터 및 AI 기반 어린이 교통 사고 예방을 위한 신 어린이 보호 구역 제안
https://youtube.com/watch?v=hPwa6K7rfxg&si=J8ncdujs6uwVO0JF

> [2021 빅데이터캠퍼스 공모전 - 우수상] 이륜차 사고 데이터 분석을 통한 사고발생구역 및 취약지 예측
https://youtube.com/watch?v=ojJfsRzSEM8&si=48sxWL6Pt21Lypol



2. 타사 교통사고 분석 참고 사이트

> 교통사고예보 라고 아시나요? | 한국 자동차 감정원
https://koreacars.org/carcast/

> 고속도로 교통정보 ROADPLUS(정체예보)
http://www.roadplus.co.kr/forecast/stagnation/selectStagnationView.do

> TAAS 교통사고 분석 시스템
https://taas.koroad.or.kr/web/shp/mik/main.do?menuId=WEB_KMP



3. 뉴스 자료 참고 사이트

> 매일경제 – 빅데이터로 교통사고 예보를 할 수 있지 않을까?
https://www.mk.co.kr/news/it/7692551

> 고령자 면허 반납 ‘지원금 상향’ 자치구 늘어
https://www.gov.kr/portal/gvrnPolicy/view/H2404000001073199?policyType=G00301&srchTxt=%EB%A9%B4%ED%97%88%EC%A6%9D



4. 도로 데이터 조사 사이트

> 도시교통정보센터(UTIS)
http://www.utic.go.kr/map/map.do?menu=incident

> 수원교통정보
http://its.suwon.go.kr/

> 경기도교통정보센터
https://gits.gg.go.kr/web/main/index.do

> 국토교통부
https://bti.kict.re.kr/bti/publicMain/main.do

> 토지e음
https://www.eum.go.kr/web/mp/mpMapDet.jsp#none;

> 국토정보플랫폼
https://map.ngii.go.kr/ms/pblictn/preciseRoadMap.do



5. 날씨 정보 조사 사이트

> 웨더아이(날씨 일별 지역별 자료)
https://www.weatheri.co.kr/bygone/bygone01.php

> AccuWeather(구별 정도 있음)
https://www.accuweather.com/ko/kr/gwonseon-gu/2330404/weather-forecast/2330404


6. 경기도 운전면허증 소지 정보
> 정보공개청구(직접 정보공개 신청)
https://www.open.go.kr/com/main/mainView.do

- 도로교통공단-도로교통공단_월별_기상상태별 교통사고 현황_20191231.xlsx(외 5개 파일)

# 이미지 불러오기
from PIL import Image

# 이미지 파일 경로 설정
image_path = "정보공개요청자료.PNG"

# 이미지 불러오기
image = Image.open(정보공개요청자료.PNG)

# 이미지 보기
image.show()


7. 노인 자동차 운전자들의 운전 실태, 운전 습관 및 안전성 자료(출처)
> 대한재활의학회지 2010;34(5):570-576.
> Annals of Rehabilitation Medicine 발췌
고령 운전자의 운전 상태, 습관 및 안전. (e-arm.org)


8. 주민등록인구현황 자료 
> 통계청(KOSIS)
서울특별시(읍면동)별/5세별 주민등록인구(2011년~) (kosis.kr)


9. 지도 시각화-수원시 자료
> 지도 시각화 자료 출처
- 29.수원시_법정경계(시군구).geojson
- 30.수원시_법정경계(시군구).geojson
COMPAS (lh.or.kr)


10. 선행기술 정보
> TAAS 도로위험도지수
https://taas.koroad.or.kr/web/shp/sbm/initRiskRoadFrcstSys.do?menuId=WEB_KMP_TAI_AFS
> 한국ITS학회 – 안전성능함수(2.안전성능함수)
http://journal.kits.or.kr/journal/article.php?code=81507
> 한국ITS학회논문지- 안전성능함수(15페이지 中 4페이지)
https://koreascience.kr/article/JAKO201931663568980.pdf
> 기상정보와 연계한 교통안전예보지수 개발 및 활용방안(10페이지 中 4페이지)
https://koreascience.kr/article/JAKO201413361962473.pdf
> Federal Highway Administration (FHWA)-미국도로관리  
https://highways.dot.gov/safety/data-analysis-tools/rsdp/data-driven-safety-analysis-ddsa
'''

