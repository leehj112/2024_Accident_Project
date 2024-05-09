# -*- coding: utf-8 -*-
"""
Created on Wed May  8 14:12:00 2024

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
#   날짜(object)                   
df['날짜'] = df['사고일시'].dt.date                                            ## 2023-01-01
#   연(int)
df['연'] = df['사고일시'].dt.year                                              ## 2023
#   월(int)
df['월'] = df['사고일시'].dt.month                                             ## 1
#   일(int)
df['일'] = df['사고일시'].dt.day                                               ## 1
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

# [사고유형] '차대사람 - 기타' -> '차대사람', '기타'
dep1 = []
dep2 = []
for i in range(len(df)) :
    dep1.append(df['사고유형'].str.split(' - ')[i][0])
    dep2.append(df['사고유형'].str.split(' - ')[i][1])
df['사고유형1'] = dep1
df['사고유형2'] = dep2

# [도로형태] '단일로 - 기타' -> '단일로', '기타'
dep1 = []
dep2 = []
for i in range(len(df)) :
    dep1.append(df['도로형태'].str.split(' - ')[i][0])
    dep2.append(df['도로형태'].str.split(' - ')[i][1])
df['도로형태1'] = dep1
df['도로형태2'] = dep2

# [피해운전자] nan -> 0
""" df.iloc[:, 18:22].columns 
Index(['피해운전자 차종', '피해운전자 성별', '피해운전자 연령', '피해운전자 상해정도'], dtype='object')
"""
df.iloc[:, 18:22] = df.iloc[:, 18:22].fillna(0)

# [연령] 00세(object) -> 00(int)
# '가해운전자'
df['가해운전자 연령'] = df['가해운전자 연령'].str[:-1]
# int 변환
df['가해운전자 연령'] = df['가해운전자 연령'].astype('int64')
#
# '피해운전자'
df['피해운전자 연령'] = df['피해운전자 연령'].str[:-1]
## -> nan(0->nan), '미분'('미분류') 존재
#       -> '미분류' : 0
df['피해운전자 연령'] = df['피해운전자 연령'].replace('미분', 0)
#       -> nan : 0
df['피해운전자 연령'] = df['피해운전자 연령'].fillna(0)
# int 변환
df['피해운전자 연령'] = df['피해운전자 연령'].astype('int64')

#%%
df.columns
"""
Index(['사고번호', '사고일시', '요일', '시군구', '사고내용', '사망자수', '중상자수', '경상자수', '부상신고자수',
       '사고유형', '법규위반', '노면상태', '기상상태', '도로형태', '가해운전자 차종', '가해운전자 성별',
       '가해운전자 연령', '가해운전자 상해정도', '피해운전자 차종', '피해운전자 성별', '피해운전자 연령',
       '피해운전자 상해정도', '날짜', '연', '월', '일', '시간', '구', '동', '사고유형1', '사고유형2',
       '도로형태1', '도로형태2'],
      dtype='object')
"""

df_table = df.loc[:, ['날짜', '연', '월', '일', '요일', '시간', 
                      '구', '동', '노면상태', '기상상태', '도로형태1', '도로형태2', 
                      '법규위반', '사고유형1', '사고유형2', '사고내용',
                      '가해운전자 차종', '가해운전자 성별', '가해운전자 연령', '가해운전자 상해정도', 
                      '피해운전자 차종', '피해운전자 성별', '피해운전자 연령', '피해운전자 상해정도',
                      '사망자수', '중상자수', '경상자수', '부상신고자수'
                      ]]

df_table['사고건수'] = 1
df_table.info()

#%%
""" 각 요인별 과거 3개년 사고건수 기준 순위의 합계
-> 공통 요인 : 월, 요일, 시간대, 동, 노면, 기상, 도로
-> 사용자 요인	: 성별, 연령, 차종
"""
df_rank = df_table.groupby(['월', '일', '요일', '시간', '구', '동', '노면상태', '기상상태', '도로형태1', '도로형태2',
                            '가해운전자 차종', '가해운전자 성별', '가해운전자 연령'])['사고건수'].sum()
df_rank.head()
"""
월  일  요일   시간  구    동      노면상태  기상상태  도로형태1  도로형태2  가해운전자 차종  가해운전자 성별  가해운전자 연령
1  1  금요일  21  권선구  오목천동   건조    맑음    단일로    기타     승용        남         68          1
      일요일  15  팔달구  인계동    건조    맑음    단일로    기타     승용        남         65          1
           18  장안구  조원동    건조    맑음    교차로    교차로부근  승용        남         69          1
   2  월요일  8   팔달구  매산로1가  건조    맑음    교차로    교차로안   승용        여         73          1
           17  장안구  영화동    건조    맑음    교차로    교차로안   화물        남         72          1
Name: 사고건수, dtype: int64
"""

df_rank = df_rank.reset_index()

#%%
df_rank['사고건수'].unique()
## array([1], dtype=int64)
# -> 요인별 사고건수 = 1

#%%
# 월별 랭크
rank = df_rank['월'].value_counts().rank(ascending=False).astype('int64')
"""
월
10     1
5      2
12     3
6      4
11     5
8      6
9      7
2      8
4      9
3     10
1     11
7     11
Name: count, dtype: int64
"""

rank.index
## Index([10, 5, 12, 6, 11, 8, 9, 2, 4, 3, 1, 7], dtype='int32', name='월')

rank[10] 
## 1

#%%
df_rank['rank_score'] = 0

for x in rank.index :
    score = rank[x]
    df_rank.loc[df_rank['월'] == x, 'rank_score'] += score
    
df_rank
"""
       월   일   요일  시간    구  ... 가해운전자 차종 가해운전자 성별 가해운전자 연령 사고건수 rank_score
0      1   1  금요일  21  권선구  ...       승용        남       68    1         11
1      1   1  일요일  15  팔달구  ...       승용        남       65    1         11
2      1   1  일요일  18  장안구  ...       승용        남       69    1         11
3      1   2  월요일   8  팔달구  ...       승용        여       73    1         11
4      1   2  월요일  17  장안구  ...       화물        남       72    1         11
  ..  ..  ...  ..  ...  ...      ...      ...      ...  ...        ...
1875  12  30  금요일  16  권선구  ...       화물        남       67    1          3
1876  12  30  금요일  20  권선구  ...       승용        남       72    1          3
1877  12  30  금요일  23  팔달구  ...       승용        남       66    1          3
1878  12  31  금요일   4  권선구  ...       승용        남       69    1          3
1879  12  31  일요일   6  팔달구  ...       승용        남       80    1          3

[1880 rows x 15 columns]
"""
    
# 일별 랭크    
rank_day = df_rank['일'].value_counts().rank(ascending=False).astype('int64')
"""
일
26     1
8      2
10     2
20     4
14     5
21     6
24     6
12     8
4      8
5     10
3     11
2     11
22    13
28    14
16    14
29    16
11    17
17    18
7     18
13    20
30    20
25    22
1     22
18    24
15    24
23    26
6     27
19    28
9     28
27    30
31    31
Name: count, dtype: int64
"""

for x in rank_day.index :
    score = rank_day[x]
    df_rank.loc[df_rank['일'] == x, 'rank_score'] += score

df_rank
"""
       월   일   요일  시간    구  ... 가해운전자 차종 가해운전자 성별 가해운전자 연령 사고건수 rank_score
0      1   1  금요일  21  권선구  ...       승용        남       68    1         33
1      1   1  일요일  15  팔달구  ...       승용        남       65    1         33
2      1   1  일요일  18  장안구  ...       승용        남       69    1         33
3      1   2  월요일   8  팔달구  ...       승용        여       73    1         22
4      1   2  월요일  17  장안구  ...       화물        남       72    1         22
  ..  ..  ...  ..  ...  ...      ...      ...      ...  ...        ...
1875  12  30  금요일  16  권선구  ...       화물        남       67    1         23
1876  12  30  금요일  20  권선구  ...       승용        남       72    1         23
1877  12  30  금요일  23  팔달구  ...       승용        남       66    1         23
1878  12  31  금요일   4  권선구  ...       승용        남       69    1         34
1879  12  31  일요일   6  팔달구  ...       승용        남       80    1         34

[1880 rows x 15 columns]
"""

#%%
# 랭크 함수
def rank_score(df, element) :
    rank_df = df[element].value_counts().rank(ascending=False).astype('int64')
    for x in rank_df.index :
        score = rank_df[x]
        df.loc[df[element] == x, 'rank_score'] += score
    return df

#%% 
# 요인
element = ['월', '일', '요일', '시간', '구', '동', '노면상태', '기상상태', '도로형태1', '도로형태2',
           '가해운전자 차종', '가해운전자 성별', '가해운전자 연령']    

# 각 요인의 순위 합계
df_rank['rank_score'] = 0

for i in element :
    rank_score(df_rank, i)
    
df_rank.sort_values(by='rank_score')
"""
       월   일   요일  시간    구  ... 가해운전자 차종 가해운전자 성별 가해운전자 연령 사고건수 rank_score
619    5   8  월요일  10  팔달구  ...       승용        남       66    1         26
1477  10  20  금요일  16  장안구  ...       승용        여       68    1         27
552    4  26  월요일  16  권선구  ...       승용        남       67    1         27
733    5  26  금요일  15  팔달구  ...       승용        남       69    1         27
1695  11  26  금요일  10  장안구  ...       승용        여       66    1         27
  ..  ..  ...  ..  ...  ...      ...      ...      ...  ...        ...
1141   8  19  토요일  11  장안구  ...      원동기        남       85    1        113
953    7   6  목요일   9  팔달구  ...       승용        남       65    1        114
207    2  15  화요일  20  팔달구  ...       승용        남       71    1        115
792    6   6  화요일   5  영통구  ...       이륜        남       71    1        117
482    4  11  일요일   1  장안구  ...       승용        남       70    1        120

[1880 rows x 15 columns]
"""
