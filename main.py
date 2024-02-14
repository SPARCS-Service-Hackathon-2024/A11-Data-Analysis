import streamlit as st
import pandas as pd

# CSV 파일 경로
file_path = '/Users/bin/Desktop/a11-analysis/data/school.csv'

# CSV 파일 읽기 (한국어 인코딩 사용)
school_df = pd.read_csv(file_path, encoding='utf-8')

# 데이터 표시
st.write("학교 데이터:")
st.write(school_df)

# 지도 표시 (위도와 경도로 설정)
st.map(data=school_df, zoom=10)
