# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:00:38 2024

@author: youl
"""
'''
# 라이브러리 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기((6개 엑셀/df와 파일명 둘다 오름차순으로 처리)

dfs = {} # df 저장공간/딕셔너리

# 파일 이름 패턴과 반복 횟수
file_pattern = '{:d}12월말_경기도운전면허소지현황.xlsx'
years = range(2019, 2024) # 24년도 4월 자료 실패로 2023까지만 불러오기

# 반복문으로 파일을 읽어들여 데이터프레임 생성
for i, year in enumerate(years):
        file_name = file_pattern.format(year)
        dfs[f'df{i+1}'] = pd.read_excel(file_name)

        
# 202404 파일 df 실패/수기처리
df6 = pd.read_excel('202404월말_경기도운전면허소지현황.xlsx') 
'''


# 라이브러리 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# 파일 이름
file_names = ['201912월말_경기도운전면허소지현황.xlsx', 
              '202012월말_경기도운전면허소지현황.xlsx', 
              '202112월말_경기도운전면허소지현황.xlsx',
              '202212월말_경기도운전면허소지현황.xlsx',
              '202312월말_경기도운전면허소지현황.xlsx',
              '202404월말_경기도운전면허소지현황.xlsx']
columns = ['year','경기']
ldf = pd.read_excel('65세 이상 면허 반납자 수(2019~2023).xlsx', usecols=columns)
ldf.rename(columns={'경기': '65세 이상 면허 자진 반납자 수'}, inplace=True)
#ldf = pd.read_excel('65세 이상 면허 반납자 수(2019~2023).xlsx')
ldf

dfs = [] # 데이터프레임 담을 빈 리스트

# 파일 읽고 데이터프레임 생성 후 리스트에 추가
for file_name in file_names:
    df = pd.read_excel(file_name)
    df.rename(columns={'운전면허소지자 현황(시군구, 연령, 대장별)': '집계월', 
                       'Unnamed: 1': '도', 'Unnamed: 2': '시군구', 'Unnamed: 3': '지역별', 
                       'Unnamed: 4': '성별','Unnamed: 5': '나이',
                       'Unnamed: 6': '종합계', 'Unnamed: 7': '1종소계', 'Unnamed: 8': '2종소계'}, inplace=True)
    dfs.append(df)


# 불필요한 열 삭제
for i in range(len(dfs)):
    dfs[i] = dfs[i].iloc[3:-1] 
    
    
# 결과 확인
for d in dfs:
    print(d.shape)
    
'''
(7053, 9)
(7104, 9)
(7127, 9)
(7125, 9)
(7158, 9)
(7323, 9)
'''

# 잘 처리 되었나 확인하기
for d in dfs:
    print(d.head)

for d in dfs:
    print(d.tail)

for d in dfs:
    print(d.info)


# 이제 nan 값이 있나 확인부터 하기(True면 nan값이 존재)
for d in dfs:
    print(d.isnull().values.any())

'''
False
False
False
False
False
False
''' 

# nan이 몇개나 있나?
for d in dfs:
    print(d.isnull().sum().sum())

'''
0
0
0
0
0
0
'''

# 잘 처리되었으니 리스트에 있는 모든 데이터프레임을 합치자
merged_df = pd.concat(dfs, ignore_index=True)

merged_df['집계월'] = merged_df['집계월'].replace(['201912말','202012말','202112말','202212말','202312말','202404말'],
                                                  ['2019','2020','2021','2022','2023','2024'])

# 집계월은 동일하니 인덱스로 설정
merged_df = merged_df.set_index('집계월')

# 결과 확인 밒 출력
print(merged_df.shape)  # (42866, 8)
merged_df.info()

#%%
# 다른 데이터 타입을 가진 컬럼 확인 : include='all'
# object 타입의 컬럼을 top으로 최빈값 확인
merged_df.describe(include='all')
'''
            도       시군구       지역별     성별     나이    종합계   1종소계   2종소계
count   42866     42866     42866  42866  42866  42866  42866  42866
unique      1        52        52      2     85   5433   4284   3101
top        경기  경기 성남 분당  경기 성남 분당      남     60      1      0      1
freq    42866       987       987  22641    585   1985   4148   1983
''' 

object_columns = merged_df.columns[merged_df.dtypes == 'object']
object_columns 
'''Index(['도', '시군구', '지역별', '성별', '나이', '종합계', '1종소계', '2종소계'], dtype='object')'''


# for문 활용하여 다른 컬럼의 값들 확인
for col in object_columns:
    print(col)
    print(merged_df[col].unique(), '\n')
    

# for 문 결과보니 '나이, 합계, 1종소계, 2종소계'는 데이터가 숫자니 int로 변경
merged_df = merged_df.astype({'나이': 'int', '종합계': 'int', '1종소계': 'int', '2종소계': 'int'})

merged_df.info()

#%%
# 지역 내용 처리하기(도, 시군구, 지역별)
# 원본 자료에 '도, 시군구, 지역별' 값이 비슷함에 확인하기
print(merged_df['도'].equals(merged_df['시군구'])) # False
print(merged_df['시군구'].equals(merged_df['지역별'])) # True

# 값이 같으니 정제하기
# 시군구 값을 'split(' ')'로 쪼개기
merged_df['지역리스트'] = merged_df['시군구'].str.split(' ')

## 시군구 값을 두번째 리스트인 시까지만 남기고 새로운 컬럼 만들기
def region_second_value(merged_df):
    return merged_df[1]

# 상위값 데이터 할당하기
merged_df['시'] = merged_df['지역리스트'].apply(region_second_value) 


# 3번째 리스트 값 처리 하기
def process_region(merged_df):
    gu = []  # 빈 리스트 생성
    for i in range(len(merged_df['지역리스트'])):
        if len(merged_df['지역리스트'][i]) == 3:
            gu.append(merged_df['지역리스트'][i][2])
        else:
            gu.append('기타') # 빈 값은 기타로 처리
    merged_df['구'] = gu  # 새로운 열 '구' 추가 및 할당
    return merged_df

# 함수 호출
ndf = process_region(merged_df)

# 중복되는 '지역별'과 필요없는 '지역리스트' 지우기
ndf = ndf.drop(columns=['지역별'])
ndf = ndf.drop(columns=['지역리스트'])
print(ndf)

# 마지막으로 가독성있게 컬럼 재배치
ndf = ndf[['시군구', '도', '시', '구', '성별', '나이', '1종소계', '2종소계', '종합계']]
print(ndf)

# '나이' 65세 이상 노인 데이터 필터
df_filtered = ndf[ndf['나이'] >= 65]
print(df_filtered)

# 종합계로 오타난 거 총합계로 변경
df_filtered.rename(columns={'종합계': '경기도 65세 이상 면허 소지자 수(명)'}, inplace=True)
df_filtered

# 
license_65 = df_filtered.groupby('집계월')['경기도 65세 이상 면허 소지자 수(명)'].sum()
print(license_65)

ldf = ldf.set_index('year')