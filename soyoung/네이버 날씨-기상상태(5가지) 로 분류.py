# -*- coding: utf-8 -*-
"""
Created on Thu May  9 09:14:14 2024

@author: soyoung
"""

#기상청 날씨 스크래이핑

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

location = "수원시 영통구 영통동"
search_query = location + " 날씨"
search_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query="
url = search_url + search_query

html_weather = requests.get(url).text
soup_weather = BeautifulSoup(html_weather, "lxml")
print(url,'\n')


# 현재 온도
current_temperature = soup_weather.find("div", {"class": "temperature_text"}).text

# 현재 날씨
current_weather_condition = soup_weather.find("p", {"class": "summary"}).text

# 현재 시간
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 현재 체감 온도, 습도, 풍속
current_bodily_sensation = soup_weather.select('div.sort dd')
[sensation, humidity, wind_speed] = [x.get_text() for x in current_bodily_sensation]

print("날씨 정보")
print("현재시간:", current_time)
print("지역:", location)
print("현재 온도:", current_temperature)
print("현재 날씨:", current_weather_condition)
print(f"체감 온도: {sensation}, 현재 습도: {humidity}, 풍속: {wind_speed}")

#%%

location = "수원시 장안구 영화동"
search_query = location + " 날씨"
search_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query="
url = search_url + search_query

html_weather = requests.get(url).text
soup_weather = BeautifulSoup(html_weather, "lxml")
print(url,'\n')

# 현재 온도
current_temperature = soup_weather.find("div", {"class": "temperature_text"}).text

# 현재 날씨
current_weather_condition = soup_weather.find("p", {"class": "summary"}).text

# 현재 시간
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 현재 체감 온도, 습도, 풍속
current_bodily_sensation = soup_weather.select('div.sort dd')
[sensation, humidity, wind_speed] = [x.get_text() for x in current_bodily_sensation]

print("날씨 정보")
print("현재시간:", current_time)
print("지역:", location)
print("현재 온도:", current_temperature)
print("현재 날씨:", current_weather_condition)
print(f"체감 온도: {sensation}, 현재 습도: {humidity}, 풍속: {wind_speed}")

#%%

location = "수원시 권선구 고색동"
search_query = location + " 날씨"
search_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query="
url = search_url + search_query

html_weather = requests.get(url).text
soup_weather = BeautifulSoup(html_weather, "lxml")
print(url,'\n')

# 현재 온도
current_temperature = soup_weather.find("div", {"class": "temperature_text"}).text

# 현재 날씨
current_weather_condition = soup_weather.find("p", {"class": "summary"}).text

# 현재 시간
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 현재 체감 온도, 습도, 풍속
current_bodily_sensation = soup_weather.select('div.sort dd')
[sensation, humidity, wind_speed] = [x.get_text() for x in current_bodily_sensation]

print("날씨 정보")
print("현재시간:", current_time)
print("지역:", location)
print("현재 온도:", current_temperature)
print("현재 날씨:", current_weather_condition)
print(f"체감 온도: {sensation}, 현재 습도: {humidity}, 풍속: {wind_speed}")

#%%

location = "수원시 팔달구 매산동"
search_query = location + " 날씨"
search_url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query="
url = search_url + search_query

html_weather = requests.get(url).text
soup_weather = BeautifulSoup(html_weather, "lxml")
print(url,'\n')

# 현재 온도
current_temperature = soup_weather.find("div", {"class": "temperature_text"}).text

# 현재 날씨
current_weather_condition = soup_weather.find("p", {"class": "summary"}).text

# 현재 시간
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 현재 체감 온도, 습도, 풍속
current_bodily_sensation = soup_weather.select('div.sort dd')
[sensation, humidity, wind_speed] = [x.get_text() for x in current_bodily_sensation]

print("날씨 정보")
print("현재시간:", current_time)
print("지역:", location)
print("현재 온도:", current_temperature)
print("현재 날씨:", current_weather_condition)
print(f"체감 온도: {sensation}, 현재 습도: {humidity}, 풍속: {wind_speed}")




#%%
#날씨분리
weather=current_weather_condition.split()[-1]


def weather_result(weather):
    print("네이버 날씨:",weather)
    
    if weather in ['맑음','구름조금','가끔비','가끔 비,눈','가끔 눈','흐린 후 갬','뇌우 후 갬','비 후 갬','눈 후 갬']:
        result='맑음'
    elif weather in ['구름많음','흐림','안개']:
        result='흐림'
    elif weather in ['약한비','비','강한비','소나기','흐려져 비']:
        result='비'
    elif weather in ['약한눈','눈','강한눈','진눈깨비','소낙눈','우박','흐려져 눈']:
        result='눈'
    else:
        result='기타'
        
    return print("기상상태:",result)

weather_result(weather)
