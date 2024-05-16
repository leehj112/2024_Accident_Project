# 경기도 지도 만들기 예시
    
import folium

# 경기도의 시 이름과 중심 좌표
cities = [
    {"name": "수원시", "location": [37.2636, 127.0286]},
    {"name": "성남시", "location": [37.4202, 127.1269]},
    {"name": "고양시", "location": [37.6584, 126.8354]},
    {"name": "용인시", "location": [37.2411, 127.1775]},
    {"name": "부천시", "location": [37.5033, 126.7663]},
    {"name": "안산시", "location": [37.3218, 126.8309]},
    {"name": "안양시", "location": [37.3904, 126.9261]},
    {"name": "평택시", "location": [36.9908, 127.0988]},
    {"name": "의정부시", "location": [37.7384, 127.0334]},
    {"name": "시흥시", "location": [37.3804, 126.8000]},
    {"name": "파주시", "location": [37.7599, 126.7800]},
    {"name": "광명시", "location": [37.4788, 126.8644]},
    {"name": "김포시", "location": [37.6154, 126.7156]},
    {"name": "광주시", "location": [37.4290, 127.2555]},
    {"name": "군포시", "location":  [37.3616, 126.9337]},
    {"name": "이천시", "location": [37.2722, 127.4350]},
    {"name": "양주시", "location": [37.7749, 127.2095]},
    {"name": "오산시", "location": [37.1503, 127.0701]},
    {"name": "구리시", "location": [37.5948, 127.1293]},
    {"name": "안성시", "location": [37.0104, 127.2791]}
]


# 경기도 중심 좌표
center = [37.4132949, 127.5183043]

# folium 맵 생성
m = folium.Map(location=center, zoom_start=10)

# 경기도의 경계를 선으로 표시 (예시 데이터)
gyeonggi_boundary = [
    [37.5, 126.6], # 서울과 경기도 경계를 나타내는 예시 데이터입니다.
    [37.5, 127.8], # 서울과 경기도 경계를 나타내는 예시 데이터입니다.
    [37.9, 127.8], # 서울과 경기도 경계를 나타내는 예시 데이터입니다.
    [37.9, 126.6], # 서울과 경기도 경계를 나타내는 예시 데이터입니다.
    [37.5, 126.6]  # 서울과 경기도 경계를 나타내는 예시 데이터입니다.
]
folium.PolyLine(gyeonggi_boundary, color="red", weight=4.5).add_to(m)


# 각 시에 마커 추가
for city in cities:
    name = city["name"]
    location = city["location"]
    folium.Marker(location=location, popup=name).add_to(m)

# HTML 파일로 저장
m.save('gyeonggi_map_with_boundary.html')