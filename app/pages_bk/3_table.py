import streamlit as st
import pandas as pd
import numpy as np

data = pd.DataFrame(
    np.random.randn(10, 6),
    columns=('컬럼 %d' % i for i in range(6)))

if 'df' not in st.session_state:
    st.session_state.df = data

# LINK TO THE CSS FILE
with open('./css/style.css')as file:
    styl = f'<style>{file.read()})</style >'

st.markdown(styl, unsafe_allow_html=True)

st.subheader("샘플 테이블")

with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 6], gap="small")
    with col1:
        if st.button('생성', type='primary'):
            st.session_state.df = st.session_state.df.append(pd.Series([1, 1, 1, 1, 1, 1],
                                                                       index=data.columns), ignore_index=True)
    with col2:
        if st.button('삭제', type='primary'):
            st.session_state.df = st.session_state.df.drop(
                st.session_state.df.index[-1])
    with col3:
        if st.button('수정', type='primary'):
            print('modify')

    st.table(st.session_state.df)


st.sidebar.success("sample table")
