import streamlit as st

with open('./css/dstyle.css')as cssfile:
    styl = f'<style>{cssfile.read()}</style >'

st.markdown(styl, unsafe_allow_html=True)


with open('download_design.html') as file:
    ele = f'<div>{file.read()}</div>'


st.markdown(ele, unsafe_allow_html=True)
