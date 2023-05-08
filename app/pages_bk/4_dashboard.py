import streamlit as st
import pandas as pd
import numpy as np

# LINK TO THE CSS FILE
with open('./css/style.css')as file:
    styl = f'<style>{file.read()})</style >'


# IMPORT DATA
data = pd.read_csv("../data/sampledata.csv", encoding='cp949')
df = pd.DataFrame(data)

with st.container():
    col1, col2 = st.columns([8, 8])

    with col1:
        st.write("here is ...")

    with col2:
        st.write("here is 2....")

st.dataframe(df)
