# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:30:05 2024

@author: soyoung
"""
"""
1. 기상청에서 가져온 데이터로 조회시점의 '기상상태' 값 생성
2. '기상상태' 값 기준 '노면상태' 값 생성"""

#%%
#노면상태 (건조, 기타, 서리/결빙, 적설, 젖음/습기)
#기상상태 (맑음, 기타, 비, 흐림, 눈)

#습도
"""
건조: 10% 미만
약간 젖음: 10% ~ 30%
적당히 젖음: 30% ~ 60%
매우 젖음: 60% 이상 """

#온도
"""
영하 2°C 이하: 노면이 결빙되어 미끄러울 가능성이 높음.                   
영하 2°C ~ 4°C: 노면이 간헐적으로 결빙될 수 있으며, 주의가 필요함.
4°C ~ 10°C: 노면이 습할 가능성이 높음.
10°C 이상: 노면이 건조할 가능성이 높음 """


#풍속
"""
풍속 10m/s 이상: 차량 운전에 어려움을 겪을 수 있으며, 교통 사고 위험 증가.
풍속 15m/s 이상: 강풍으로 인해 도로 위의 물체가 날아다닐 수 있음.
풍속 20m/s 이상: 매우 강한 바람으로 인해 차량 운전 매우 위험. """

#강수량
"""
눈 5cm 이상: 도로가 미끄러울 가능성 높음이며, 특히 언덕이나 구불구불한 도로에서는 더욱 위험.
비 20mm 이상: 도로가 젖어 미끄러울 가능성 높음이며, 시야 저하로 인해 운전에 어려움 겪을 수 있음 """

#%%

import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
from matplotlib import font_manager, rc
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font_name)

df = pd.read_excel('D:\Workspace\Python\mini\The elderly driver traffic accidents(suwon).xlsx')

#기상상태기준 노면상태 분포
df_grouped = df.groupby(['기상상태', '노면상태']).size().reset_index(name='count')

print(df_grouped)
"""
   기상상태   노면상태  count
0    기타     건조       5
1    기타  젖음/습기     1
2     눈  서리/결빙      3
3     눈     적설        2
4     눈  젖음/습기      2
5    맑음     건조      1666
6    맑음     기타       6
7    맑음  서리/결빙     5
8    맑음     적설       1
9    맑음  젖음/습기     6
10    비  젖음/습기     119
11   흐림     건조      40
12   흐림     적설       1
13   흐림  젖음/습기     23     """

#노면상태기준 기상상태 분포
df_grouped = df.groupby(['노면상태', '기상상태']).size().reset_index(name='count')

print(df_grouped)
"""
     노면상태 기상상태  count
0      건조   기타       5
1      건조   맑음       1666
2      건조   흐림       40
3      기타   맑음        6
4   서리/결빙    눈       3
5   서리/결빙   맑음      5
6      적설    눈         2
7      적설   맑음        1
8      적설   흐림        1
9   젖음/습기   기타      1
10  젖음/습기    눈       2
11  젖음/습기   맑음      6
12  젖음/습기    비      119
13  젖음/습기   흐림     23   """


