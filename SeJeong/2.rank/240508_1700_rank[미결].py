# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:38:54 2024

@author: ksj
"""

import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
from matplotlib import font_manager, rc
font_path = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname = font_path).get_name()
rc('font', family = font_name)

df = pd.read_excel('./The elderly driver traffic accidents(suwon).xlsx')

#%% 전처리
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
"""
수도권:
주간: 오전 7시부터 오후 8시까지 (13시간)
야간: 오후 8시부터 다음 날 오전 7시까지 (11시간)
"""
df['주야간'] = df['시간'].apply(lambda x: '주간' if 7 <= x <= 20 else '야간')


# 사고건수
df['사고건수'] = 1

#%%
df.columns
"""
Index(['사고번호', '사고일시', '요일', '시군구', '사고내용', '사망자수', '중상자수', '경상자수', '부상신고자수',
       '사고유형', '법규위반', '노면상태', '기상상태', '도로형태', '가해운전자 차종', '가해운전자 성별',
       '가해운전자 연령', '가해운전자 상해정도', '피해운전자 차종', '피해운전자 성별', '피해운전자 연령',
       '피해운전자 상해정도', '시간', '구', '동', '주야간', '사고건수'],
      dtype='object')
"""

df_table = df.loc[:, ['주야간', '구', '노면상태', '기상상태', '사고건수']]

#%%
# 랭크 함수
def rank_score(df, element) :
    rank_df = df[element].value_counts().rank(ascending=True).astype('int64')
    for x in rank_df.index :
        score = rank_df[x]
        df.loc[df[element] == x, f'{element}_rank_score'] = score
    return df

#%% 
# 요인
element = ['주야간', '구', '노면상태', '기상상태']    

# 각 요인의 순위 열 추가
for i in element :
    rank_score(df_table, i)

# 각 요인의 순위 합계   
df_table['rank_score'] = df_table.iloc[:, -4:].apply(sum, axis=1)
    
df_table.sort_values(by='rank_score', ascending=False)
"""
     주야간    구   노면상태  ... 노면상태_rank_score  기상상태_rank_score  rank_score
1716  주간  권선구     건조  ...             5.0              5.0        16.0
1147  주간  권선구     건조  ...             5.0              5.0        16.0
1153  주간  권선구     건조  ...             5.0              5.0        16.0
419   주간  권선구     건조  ...             5.0              5.0        16.0
417   주간  권선구     건조  ...             5.0              5.0        16.0
  ..  ...    ...  ...             ...              ...         ...
1105  주간  팔달구     적설  ...             1.0              3.0         9.0
1231  야간  영통구  젖음/습기  ...             4.0              3.0         9.0
19    야간  영통구     건조  ...             5.0              1.0         8.0
1094  주간  장안구     적설  ...             1.0              2.0         7.0
1097  주간  장안구     적설  ...             1.0              2.0         7.0

[1880 rows x 10 columns]
"""

#%%
df_table.columns
"""
Index(['주야간', '구', '노면상태', '기상상태', '사고건수', '주야간_rank_score', '구_rank_score',
       '노면상태_rank_score', '기상상태_rank_score', 'rank_score'],
      dtype='object')
"""

#%%
# 요인 순위 합계 + '사고건수' 순위 
df_rank = df_table.groupby(['주야간', '구', '노면상태', '기상상태', '주야간_rank_score', '구_rank_score',
       '노면상태_rank_score', '기상상태_rank_score', 'rank_score'])['사고건수'].sum()
df_rank = df_rank.reset_index()

df_rank.sort_values(by='rank_score', ascending=False)
"""
   주야간    구   노면상태 기상상태  ...  노면상태_rank_score  기상상태_rank_score  rank_score  사고건수
21  주간  권선구     건조   맑음  ...              5.0              5.0        16.0   413
25  주간  권선구  젖음/습기   맑음  ...              4.0              5.0        15.0     1
1   야간  권선구     건조   맑음  ...              5.0              5.0        15.0    81
45  주간  팔달구     건조   맑음  ...              5.0              5.0        15.0   427
26  주간  권선구  젖음/습기    비  ...              4.0              4.0        14.0    33
35  주간  장안구     건조   맑음  ...              5.0              5.0        14.0   367
24  주간  권선구  서리/결빙   맑음  ...              3.0              5.0        14.0     1
15  야간  팔달구     건조   맑음  ...              5.0              5.0        14.0    70
22  주간  권선구     건조   흐림  ...              5.0              3.0        14.0     6
42  주간  장안구  젖음/습기   맑음  ...              4.0              5.0        13.0     3
10  야간  장안구     건조   맑음  ...              5.0              5.0        13.0    54
23  주간  권선구     기타   맑음  ...              2.0              5.0        13.0     3
46  주간  팔달구     건조   흐림  ...              5.0              3.0        13.0     7
28  주간  영통구     건조   맑음  ...              5.0              5.0        13.0   209
27  주간  권선구  젖음/습기   흐림  ...              4.0              3.0        13.0     1
51  주간  팔달구  젖음/습기    비  ...              4.0              4.0        13.0    19
4   야간  권선구  젖음/습기    비  ...              4.0              4.0        13.0     9
3   야간  권선구  서리/결빙   맑음  ...              3.0              5.0        13.0     1
2   야간  권선구     건조   흐림  ...              5.0              3.0        13.0     3
36  주간  장안구     건조   흐림  ...              5.0              3.0        12.0     9
43  주간  장안구  젖음/습기    비  ...              4.0              4.0        12.0    30
32  주간  영통구  젖음/습기   맑음  ...              4.0              5.0        12.0     2
39  주간  장안구  서리/결빙   맑음  ...              3.0              5.0        12.0     1
52  주간  팔달구  젖음/습기   흐림  ...              4.0              3.0        12.0     7
20  주간  권선구     건조   기타  ...              5.0              1.0        12.0     1
18  야간  팔달구  젖음/습기    비  ...              4.0              4.0        12.0     9
17  야간  팔달구  서리/결빙   맑음  ...              3.0              5.0        12.0     1
16  야간  팔달구     건조   흐림  ...              5.0              3.0        12.0     2
5   야간  권선구  젖음/습기   흐림  ...              4.0              3.0        12.0     4
7   야간  영통구     건조   맑음  ...              5.0              5.0        12.0    45
12  야간  장안구  젖음/습기    비  ...              4.0              4.0        11.0     7
50  주간  팔달구  젖음/습기    눈  ...              4.0              2.0        11.0     2
44  주간  장안구  젖음/습기   흐림  ...              4.0              3.0        11.0     2
11  야간  장안구     건조   흐림  ...              5.0              3.0        11.0     7
19  야간  팔달구  젖음/습기   흐림  ...              4.0              3.0        11.0     1
37  주간  장안구     기타   맑음  ...              2.0              5.0        11.0     1
0   야간  권선구     건조   기타  ...              5.0              1.0        11.0     2
33  주간  영통구  젖음/습기    비  ...              4.0              4.0        11.0     8
31  주간  영통구  서리/결빙   맑음  ...              3.0              5.0        11.0     1
29  주간  영통구     건조   흐림  ...              5.0              3.0        11.0     6
13  야간  장안구  젖음/습기   흐림  ...              4.0              3.0        10.0     2
34  주간  영통구  젖음/습기   흐림  ...              4.0              3.0        10.0     3
41  주간  장안구     적설   맑음  ...              1.0              5.0        10.0     1
8   야간  영통구  젖음/습기    비  ...              4.0              4.0        10.0     4
14  야간  팔달구     건조   기타  ...              5.0              1.0        10.0     1
47  주간  팔달구  서리/결빙    눈  ...              3.0              2.0        10.0     2
49  주간  팔달구  젖음/습기   기타  ...              4.0              1.0        10.0     1
30  주간  영통구     기타   맑음  ...              2.0              5.0        10.0     2
9   야간  영통구  젖음/습기   흐림  ...              4.0              3.0         9.0     3
48  주간  팔달구     적설   흐림  ...              1.0              3.0         9.0     1
38  주간  장안구  서리/결빙    눈  ...              3.0              2.0         9.0     1
6   야간  영통구     건조   기타  ...              5.0              1.0         8.0     1
40  주간  장안구     적설    눈  ...              1.0              2.0         7.0     2

[53 rows x 10 columns]
"""

#%%
###############################################################################
# 조건에 따른 rank_score 추출
###############################################################################
# 주야간
# 현재 시간 가져오기
from datetime import datetime
current_time = datetime.now()
""" 주간/야간 구분 함수
> 주간: 오전 7시부터 오후 8시까지 (13시간)
> 야간: 오후 8시부터 다음 날 오전 7시까지 (11시간) """
def timesplit(current_time):
    if current_time.hour>=7 and current_time.hour<20:
        current="주간"
    else:
        current="야간"
    return current
        
time = timesplit(current_time)
print(time)

# 노면상태
road_list = df_rank['노면상태'].unique()
print(road_list)
## ['건조' '서리/결빙' '젖음/습기' '기타' '적설']

# 기상상태
weather_list = df_rank['기상상태'].unique()
print(weather_list)
## ['맑음' '눈' '흐림' '기타' '비']

# 구
gu = df_rank['구'].unique()
print(gu)
## ['권선구' '장안구' '팔달구' '영통구']

#%%
op_time = df_rank['주야간'] == time
op_road = df_rank['노면상태'] == road_list[0]
op_weather = df_rank['기상상태'] == weather_list[0]

fil_op = df_rank.loc[op_time & op_road & op_weather, :]
"""
   주야간    구 노면상태 기상상태  ...  노면상태_rank_score  기상상태_rank_score  rank_score  사고건수
20  주간  권선구   건조   기타  ...              5.0              1.0        12.0     1

[1 rows x 10 columns]
"""
print(fil_op['rank_score'])
## 12.0

#%%
"""
미결사항 
1. 전체 조건이 df_rank로 생성되지 않아 조건이 없는 경우 구별 rank_score을 구할 수 없음
2. rank_score와 사고건수가 일부 타당하지 않게 보이는 행이 있음. 요인별 가중치를 구해야 할 듯함
"""

#%%
df_rank.loc[op_time, '구'].unique()
"""
array(['권선구', '영통구', '장안구', '팔달구'], dtype=object)
"""
df_rank.loc[op_road, '구'].unique()
"""
array(['권선구', '영통구', '장안구', '팔달구'], dtype=object)
"""
df_rank.loc[op_weather, '구'].unique()
"""
array(['권선구', '영통구', '팔달구'], dtype=object)
"""
#   -> '기타' 일 때 '장안구' 값 없음

df_rank.loc[op_time & op_weather, '구'].unique()
"""
array(['권선구', '팔달구'], dtype=object)
"""
#   -> '주간'&'기타'일 때 '영통구' 값 없음
