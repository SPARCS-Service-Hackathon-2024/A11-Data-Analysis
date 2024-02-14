import streamlit as st
import numpy as np
import pandas as pd

myData = np.random.randn(30,3)
df = pd.DataFrame(data=myData, columns=['a','b','c'])

st.line_chart(df)
st.area_chart(df)
st.bar_chart(df)

myData = {'lat': [37.56668], 'lon': [126.9784]}
for _ in range(100):
    myData['lat'].append(myData['lat'][0] + np.random.randn() / 50.0)
    myData['lon'].append(myData['lon'][0] + np.random.randn() / 50.0)

st.map(data=myData, zoom=10)

