import streamlit as st
import pandas as pd
import altair as alt
import re

file_path = './data/seogu_data.csv'

st.title("대전 - 통계와 추이")

# ----CHART 1----
st.header("대전 서구 혼인, 이혼 현황")

# Dropdown
option = st.selectbox('데이터 유형을 선택하세요:', ('출생', '출생-여자', '출생-남자', '이혼', '혼인'))

# 공공데이터 출처: https://www.data.go.kr/data/15075218/fileData.do#/layer%20data%20infomation
# 공공데이터 출처: https://www.data.go.kr/data/15061151/fileData.do


# 선택 데이터: 총출생, 이혼, 혼인까지 가능
if option == '출생':
    data_column = '총출생'
elif option == '출생-여자':
    data_column = '출생_여자'
elif option == '출생-남자':
    data_column = '출생_남자'
elif option == '이혼':
    data_column = '이혼'
else:
    data_column = '혼인'


seogu_df = pd.read_csv(file_path, encoding='utf-8')

chart = alt.Chart(seogu_df).mark_line().encode(
    x='월',
    y=data_column,
    color='기준연도:N',
    tooltip=['월', data_column, '기준연도']
).interactive()

st.altair_chart(chart, use_container_width=True)


# ----CHART 2----
st.header("대전 지역별 다자녀가정 우대 업체")

food_path = './data/대전광역시_다자녀가정우대 참여업체현황(음식점)_20210927.csv'
bakery_path = './data/대전광역시_다자녀가정우대 참여업체현황(제과점)_20210927.csv'
institute_path = './data/대전광역시_다자녀가정우대 참여업체현황(학원, 독서실)_20210927.csv'
books_path = './data/대전광역시_다자녀가정우대 참여업체현황(서적, 문구)_20210927.csv'
health_path = './data/대전광역시_다자녀가정우대 참여업체현황(건강, 레저)_20210927.csv'

food_df = pd.read_csv(food_path)
bakery_df = pd.read_csv(bakery_path)
institute_df = pd.read_csv(institute_path)
books_df = pd.read_csv(books_path)
health_df = pd.read_csv(health_path)

dfs = [food_df, bakery_df, institute_df, books_df, health_df]

combined_df = pd.concat(dfs)

#XX동 뽑아오기
def extract_text_up_to_dong(text):
    match = re.search(r'\((.*?동)', text)
    if match:
        return match.group(1)
    else:
        return ""
combined_df['동'] = combined_df['소재지'].apply(extract_text_up_to_dong)

# 셀렉션
selected_dong = st.selectbox('지역 선택:', combined_df['동'].unique())

# 동별 필터링 
filtered_df = combined_df[combined_df['동'] == selected_dong]


colors = ['blue', 'green', 'red', 'orange', 'purple']
names = ['음식점', '제과점', '학원/독서실', '서적/문구', '건강/레저']


for i, df in enumerate(dfs):
    filtered_df.loc[filtered_df.index.isin(df.index), 'Dataframe'] = f'{names[i]}'

color_mapping = {name: color for name, color in zip(names, colors)}

if selected_dong:
    for i, df in enumerate(dfs):
        company_names = filtered_df[filtered_df.isin(df)['기관ㆍ업체명']]
        if not company_names.empty:
            st.markdown(f"<span style='color:orange'><b>{names[i]}:</b>", unsafe_allow_html=True)
            for company in company_names['기관ㆍ업체명'].unique():
                st.write(f"- {company}")
else:
    st.write("Please select a 동.")