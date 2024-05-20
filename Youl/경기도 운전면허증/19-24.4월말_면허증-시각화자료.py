# -*- coding: utf-8 -*-
"""
Created on Mon May 13 08:49:58 2024

@author: youl
"""
# -*- coding: utf-8 -*-
# 라이브러리 불러오기
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 시각화하기 위해 폰트 설정
plt.rc('font', family='Malgun Gothic')

# 연령대 확인 및 구분
ndf['나이'].unique()
'''array([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
       33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
       50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66,
       67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
       84, 85, 86, 87, 88, 89, 90, 91, 92, 95, 99, 93, 94, 96, 97, 98,  0])'''

# 65세 미만이면 일반운전자, 65세 이상이면 노인운전자로 분류

def calc_age_group(age):
    if age < 65:
        return '일반운전자'    
    else:
        return '노인운전자'

ndf['운전자구분'] = ndf['나이'].apply(calc_age_group)
ndf['운전자구분'].unique() # array(['일반운전자', '노인운전자'], dtype=object)

ndf.info()

#%%
# 전체 인원
group_tot_driver = ndf.groupby('집계월')['종합계'].sum()
print(group_tot_driver)
'''
집계월
201912말    8535625
202012말    8806607
202112말    9071918
202212말    9244904
202312말    9374754
202404말    9416949
Name: 종합계, dtype: int32
'''

ndf.head()
'''
           시군구   도   시   구 성별  나이  1종소계  2종소계  종합계  운전자구분
집계월                                                      
201912말  경기 가평  경기  가평  기타  남  19    95    41  136  일반운전자
201912말  경기 가평  경기  가평  기타  남  20   154    59  213  일반운전자
201912말  경기 가평  경기  가평  기타  여  21   155    63  218  일반운전자
201912말  경기 가평  경기  가평  기타  여  22   200    51  251  일반운전자
201912말  경기 가평  경기  가평  기타  남  23   227    62  289  일반운전자
'''

# 성별에 따른 합계 및 비율
def calc_tot_and_ratio_by_gender(ndf, gender):
    gender_df = ndf[ndf['성별'] == gender] # 성별에 따라 데이터 필터링
    group_tot_sum = gender_df.groupby('집계월')['종합계'].sum() # 인덱스'집계월' groupby
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum() # 집계월별 전체 운전자의 총합
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100 # 비율 계산
    return group_tot_sum, group_ratio_driver

# 남성과 여성 기준으로 합계와 비율 계산
group_tot_sum_male, group_ratio_male_driver = calc_tot_and_ratio_by_gender(ndf, '남')
group_tot_sum_female, group_ratio_female_driver = calc_tot_and_ratio_by_gender(ndf, '여')

print("남성 운전자의 총합:", group_tot_sum_male)
print("남성 운전자의 비율:", group_ratio_male_driver)

print("여성 운전자의 총합:", group_tot_sum_female)
print("여성 운전자의 비율:", group_ratio_female_driver)




#%%
# 운전자 구분에 따른 합계와 비율
def calc_tot_and_ratio_by_driver_type(ndf, driver_type):
    driver_df = ndf[ndf['운전자구분'] == driver_type]
    group_tot_sum = driver_df.groupby('집계월')['종합계'].sum()
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum()
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100
    return group_tot_sum, group_ratio_driver


# 노인운전자와 일반운전자 기준으로 합계와 비율 계산
tot_elderly_driver_sum, ratio_elderly_driver = calc_tot_and_ratio_by_driver_type(ndf, '노인운전자')
tot_regular_driver_sum, ratio_regular_driver = calc_tot_and_ratio_by_driver_type(ndf, '일반운전자')

print("노인운전자의 총합:", tot_elderly_driver_sum)
print("노인운전자의 비율:", ratio_elderly_driver)

print("일반운전자의 총합:", tot_regular_driver_sum)
print("일반운전자의 비율:", ratio_regular_driver)

#%%
# 운전자구분과 성별 매칭
def calc_tot_by_gender_and_driver_type(ndf, gender, driver_type):
    driver_df = ndf[(ndf['운전자구분'] == driver_type) & (ndf['성별'] == gender)]
    group_tot_sum = driver_df.groupby('집계월')['종합계'].sum()
    group_tot_driver = ndf.groupby('집계월')['종합계'].sum()
    group_ratio_driver = (group_tot_sum / group_tot_driver) * 100
    return group_tot_sum, group_ratio_driver

# 노인운전자와 성별 매칭
# 여성 노인운전자의 합계와 남성 노인운전자의 합계 계산
tot_elderly_female_sum, ratio_elderly_female_driver = calc_tot_by_gender_and_driver_type(ndf, '여', '노인운전자')
tot_elderly_male_sum, ratio_elderly_male_driver = calc_tot_by_gender_and_driver_type(ndf, '남', '노인운전자')

print("여성 노인운전자의 합계:", tot_elderly_female_sum) 
print("남성 노인운전자의 합계:", tot_elderly_male_sum)  

print(f"여성 노인운전자의 비율: {ratio_elderly_female_driver.round(1).values}%")
'''여성 노인운전자의 비율: [2.5 2.8 3.2 3.6 4.  4.1]%'''

print(f"남성 노인운전자의 비율: {ratio_elderly_male_driver.round(1).values}%")
'''남성 노인운전자의 비율: [6.2 6.6 6.9 7.3 7.8 8. ]%'''

# 일반운전자와 성별 매칭
# 여성 노인운전자의 합계와 남성 노인운전자의 합계 계산
tot_male_regular_sum, ratio_male_regular_driver = calc_tot_by_gender_and_driver_type(ndf, '여', '일반운전자')
tot_female_regular_sum, ratio_female_regular_driver = calc_tot_by_gender_and_driver_type(ndf, '남', '일반운전자')

print("여성 일반운전자의 합계:", tot_male_regular_sum) 
print("남성 일반운전자의 합계:", tot_female_regular_sum)  

print(f"여성 일반운전자의 비율: {ratio_male_regular_driver.round(1).values}%")
'''여성 일반운전자의 비율: [40.1 40.  40.  39.8 39.6 39.5]%'''

print(f"남성 일반운전자의 비율: {ratio_female_regular_driver.round(1).values}%")
''''남성 일반운전자의 비율: [51.2 50.6 50.  49.3 48.6 48.4]%'''
#%%
# 시각화하기
# 성별에 따른 전체 운전자 비율(선그래프)

# 집계월
months = ndf.index.unique()

# 선 그래프 그리기
plt.figure(figsize=(12, 6))

plt.plot(months, group_ratio_male_driver, marker='o', label='전체 남성운전자')
plt.plot(months, group_ratio_female_driver, marker='o', label='전체 여성운전자')

plt.title('집계월별 운전자 유형별 비율')
plt.xlabel('집계월')
plt.ylabel('운전자 비율 (%)')
plt.xticks(rotation=45)
plt.legend()
#plt.grid(True) # 지저분해보임

plt.tight_layout()
plt.show()

tot_elderly_driver_sum
#%%
# 시각화하기
# 운전자구분에 따른 전체 운전자 비율(선그래프)

# 집계월
months = ndf.index.unique()

# 선 그래프 그리기
plt.figure(figsize=(12, 6))

plt.plot(months, tot_elderly_driver_sum, marker='o', label='노인운전자')
plt.plot(months, tot_regular_driver_sum, marker='o', label='일반운전자')

plt.title('집계월별 운전자 총합(운전자 유형별) ')
plt.xlabel('집계월')
plt.ylabel('운전자 수')
plt.xticks(rotation=45)
plt.legend()
# plt.grid(True) # 지저분해보임

plt.tight_layout()
plt.show()


#%%
# 성별에 따른 운전자 구분 시각화
# 집계월
months = ndf.index.unique()
# 선 그래프 그리기
plt.figure(figsize=(12, 6))

plt.plot(months, ratio_elderly_female_driver, marker='o', label='여성 노인운전자')
plt.plot(months, ratio_male_regular_driver, marker='o', label='여성 일반운전자')
plt.plot(months, ratio_elderly_male_driver, marker='o', label='남성 노인운전자')
plt.plot(months, ratio_female_regular_driver, marker='o', label='남성 일반운전자')

plt.title('집계월별 운전자 유형 및 성별 비율')
plt.xlabel('집계월')
plt.ylabel('운전자 비율 (%)')
plt.xticks(rotation=45)
plt.legend()
# plt.grid(True) # 지저분해보임

plt.tight_layout()
plt.show()

