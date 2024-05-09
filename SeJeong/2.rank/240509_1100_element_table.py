# -*- coding: utf-8 -*-
"""
Created on Thu May  9 10:29:05 2024

@author: ksj
"""

import pandas as pd

#%%
###############################################################################
# 요인의 모든 조합 df 생성
###############################################################################
# 주야간
time_list = ['주간', '야간']
# 구
gu_list = ['권선구', '장안구', '팔달구', '영통구']
# 노면상태
road_list = ['건조', '서리/결빙', '젖음/습기', '기타', '적설']
# 기상상태
weather_list = ['맑음', '눈', '흐림', '기타', '비']

# 요인df 생성
time = []
for x in time_list :
    for _ in range(len(gu_list) * len(road_list) * len(weather_list)) :
        time.append(x)

gu = []
for x in gu_list :
    for _ in range(len(road_list) * len(weather_list)) :
        gu.append(x)
gu = gu * len(time_list)

road = []
for x in road_list :
    for _ in range(len(weather_list)) :
        road.append(x)
road = road * len(time_list) * len(gu_list)

weather = weather_list.copy()
weather = weather * len(time_list) * len(gu_list) * len(road_list)

element_df = pd.DataFrame({'주야간': time, '구': gu, '노면상태': road, '기상상태': weather })

print(element_df)
""" 2 * 4 * 5 * 5 = 200
    주야간    구 노면상태 기상상태
0    주간  권선구   건조   맑음
1    주간  권선구   건조    눈
2    주간  권선구   건조   흐림
3    주간  권선구   건조   기타
4    주간  권선구   건조    비
..   ..  ...  ...  ...
195  야간  영통구   적설   맑음
196  야간  영통구   적설    눈
197  야간  영통구   적설   흐림
198  야간  영통구   적설   기타
199  야간  영통구   적설    비

[200 rows x 4 columns]
"""

#%%
###############################################################################
# 각 요인 위험지수(순위)
###############################################################################
# ## 데이터
df = pd.read_excel('./The elderly driver traffic accidents(suwon).xlsx')


# ## 전처리
# [사고일시] -> datetime
df['사고일시'] = pd.to_datetime(df['사고일시'], format='%Y년 %m월 %d일 %H시')  ## 2023-01-01 00:00:00
#   시간(int)
df['시간'] = df['사고일시'].dt.hour                                            ## 0

# [시군구] -> 구/ 동
gu = []
dong = []
for i in range(len(df)) :
    gu.append(df['시군구'].str.split(' ')[i][2])
    dong.append(df['시군구'].str.split(' ')[i][3])
df['구'] = gu 
df['동'] = dong

# 시간대 -> 주간/야간
""" 기준
주간: 오전 7시부터 오후 8시까지 (13시간)
야간: 오후 8시부터 다음 날 오전 7시까지 (11시간)
"""
df['주야간'] = df['시간'].apply(lambda x: '주간' if 7 <= x <= 20 else '야간')

# 사고건수
df['사고건수'] = 1


# ## 필요한 열만 추출
df_table = df.loc[:, ['주야간', '구', '노면상태', '기상상태', '사고건수']]

# ## 랭크 함수
#   - 사고건수가 많은 요인의 값이 크도록 'ascending=True' 설정
def rank_score(df, element) :
    rank_df = df[element].value_counts().rank(ascending=True).astype('int64')
    return rank_df

# ## 각 요인의 위험지수(순위 역순) df 생성
rank_time = rank_score(df_table, '주야간')
"""
주야간
주간    2
야간    1
Name: count, dtype: int64
""" 
rank_area = rank_score(df_table, '구')
"""
구
권선구    4
팔달구    3
장안구    2
영통구    1
Name: count, dtype: int64
"""
rank_road = rank_score(df_table, '노면상태')
"""
노면상태
건조       5
젖음/습기    4
서리/결빙    3
기타       2
적설       1
Name: count, dtype: int64
"""
rank_weather = rank_score(df_table, '기상상태')
"""
기상상태
맑음    5
비     4
흐림    3
눈     2
기타    1
Name: count, dtype: int64
"""

#%%
###############################################################################
# 요인별 위험지수 병합
###############################################################################
element_risk = element_df.copy()

for x in time_list :
    element_risk.loc[element_risk['주야간'] == x, '주야간_risk'] = rank_time[x]
    
for x in gu_list :
    element_risk.loc[element_risk['구'] == x, '구_risk'] = rank_area[x]

for x in road_list :
    element_risk.loc[element_risk['노면상태'] == x, '노면상태_risk'] = rank_road[x]

for x in weather_list :
    element_risk.loc[element_risk['기상상태'] == x, '기상상태_risk'] = rank_weather[x]

print(element_risk)
"""
    주야간    구 노면상태 기상상태  주야간_risk  구_risk  노면상태_risk  기상상태_risk
0    주간  권선구   건조   맑음       2.0     4.0        5.0        5.0
1    주간  권선구   건조    눈       2.0     4.0        5.0        2.0
2    주간  권선구   건조   흐림       2.0     4.0        5.0        3.0
3    주간  권선구   건조   기타       2.0     4.0        5.0        1.0
4    주간  권선구   건조    비       2.0     4.0        5.0        4.0
..   ..  ...  ...  ...       ...     ...        ...        ...
195  야간  영통구   적설   맑음       1.0     1.0        1.0        5.0
196  야간  영통구   적설    눈       1.0     1.0        1.0        2.0
197  야간  영통구   적설   흐림       1.0     1.0        1.0        3.0
198  야간  영통구   적설   기타       1.0     1.0        1.0        1.0
199  야간  영통구   적설    비       1.0     1.0        1.0        4.0

[200 rows x 8 columns]
"""

# 요인 위험지수 총계
element_risk['total_risk'] = element_risk.iloc[:, -4:].sum(axis=1)

element_risk = element_risk.sort_values(by='total_risk', ascending=False).reset_index(drop=True)

print(element_risk)
"""
    주야간    구   노면상태 기상상태  주야간_risk  구_risk  노면상태_risk  기상상태_risk  total_risk
0    주간  권선구     건조   맑음       2.0     4.0        5.0        5.0        16.0
1    주간  권선구     건조    비       2.0     4.0        5.0        4.0        15.0
2    주간  팔달구     건조   맑음       2.0     3.0        5.0        5.0        15.0
3    주간  권선구  젖음/습기   맑음       2.0     4.0        4.0        5.0        15.0
4    야간  권선구     건조   맑음       1.0     4.0        5.0        5.0        15.0
..   ..  ...    ...  ...       ...     ...        ...        ...         ...
195  주간  영통구     적설   기타       2.0     1.0        1.0        1.0         5.0
196  야간  영통구     기타   기타       1.0     1.0        2.0        1.0         5.0
197  야간  장안구     적설   기타       1.0     2.0        1.0        1.0         5.0
198  야간  영통구     적설    눈       1.0     1.0        1.0        2.0         5.0
199  야간  영통구     적설   기타       1.0     1.0        1.0        1.0         4.0

[200 rows x 9 columns]
"""
