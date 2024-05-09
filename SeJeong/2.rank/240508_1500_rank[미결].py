# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:35:45 2024

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

df_rank = df.loc[:, ['주야간', '구', '노면상태', '기상상태', '사고건수',
                     '사망자수', '중상자수', '경상자수', '부상신고자수']]


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
element = ['주야간', '구', '노면상태', '기상상태']    

# 각 요인의 순위 합계
df_rank['rank_score'] = 0

for i in element :
    rank_score(df_rank, i)
    
df_rank.sort_values(by='rank_score', ascending=False)
"""
     주야간    구   노면상태 기상상태  사고건수  사망자수  중상자수  경상자수  부상신고자수  rank_score
1094  주간  장안구     적설    눈     1     0     1     0       0          13
1097  주간  장안구     적설    눈     1     0     0     2       0          13
19    야간  영통구     건조   기타     1     0     0     1       0          12
7     주간  장안구  서리/결빙    눈     1     0     0     1       0          11
1124  야간  영통구  젖음/습기   흐림     1     0     0     1       0          11
  ..  ...    ...  ...   ...   ...   ...   ...     ...         ...
786   주간  권선구     건조   맑음     1     0     0     1       0           4
788   주간  권선구     건조   맑음     1     0     0     1       0           4
1452  주간  권선구     건조   맑음     1     0     5     1       0           4
794   주간  권선구     건조   맑음     1     0     0     1       0           4
162   주간  권선구     건조   맑음     1     0     1     0       0           4

[1880 rows x 10 columns]
"""

