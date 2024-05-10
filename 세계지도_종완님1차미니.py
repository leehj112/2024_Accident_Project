# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 20:37:20 2024

@author: totoz
"""
import folium

# 다섯 개국의 이름, 위도, 경도, 인구
countries = {
    "프랑스"  : (48.8032, 02.3511, 15,"guZazCqmpfc"),
    "영국"    : (51.3096, 00.0739, 31,"lJ7M9gF3iE"),
    "독일"    : (52.5200, 14.4049, 23,"EM__GI7sw9w"),
    "이탈리아": (41.5333, 12.2857, 12,"XjxMLaTNjmE"),
    "스페인"  : (40.2300, 03.4300, 13,"XUSeybFhcro")
}

# 지도 객체 생성
world_map = folium.Map(location=[50, 10], zoom_start=5)


fmt = '<iframe width="560" height="315" src="https://www.youtube.com/embed/{}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

# 다섯 개국의 위치에 마커와 인구 정보 추가
for country, data in countries.items():
    popup_fmt = fmt.format(data[3])
    popup_text = f"<span style='color: red;'>{country}: {data[2]}명</span>"
    folium.Marker(location=[data[0], data[1]],  popup=popup_fmt,
                  icon=folium.DivIcon(html=f"<div>{popup_text}</div>")).add_to(world_map)
   

# 지도를 HTML 파일로 저장
world_map.save("world_population_map1.html")

