# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:33:02 2024

@author: HONGHAE
"""

import folium
folium.__version__
import pandas as pd
import json

# 데이터 불러오기
df = pd.read_csv('E:\workspace(Honghae)\python\project\요인별 위험지수(ECLO 추가).csv', encoding='cp949')
df.head()
df['구'] = '수원시'+' ' + df['구']

#%%

with open('29.수원시_법정경계(시군구).geojson', encoding='utf-8') as f:
    data = json.load(f)


#%%

# 수원시 중심부의 위도, 경도
center = [37.2636, 127.0286]

# 맵이 center에 위치하고, zoom 레벨은 11로 시작하는 맵 m 생성
m = folium.Map(location=center, zoom_start=10)

# Choropleth 레이어를 만들고, 맵 m에 추가
folium.Choropleth(
    geo_data= data,
    data = df,
    columns=('구','eclo_risk_mul'),
    key_on='feature.properties.SIG_KOR_NM',
    fill_color='BuPu',
    legend_name='ECLO',
    ).add_to(m)

# 맵 m을 출력
m

# 맵 m을 저장
m.save('map.html')
