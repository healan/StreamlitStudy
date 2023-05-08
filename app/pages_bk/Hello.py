import streamlit as st
import pandas as pd
import numpy as np
import requests
import json


url = 'http://192.168.2.51:8009'

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

# session state
if 'ex_ip' not in st.session_state:
    st.session_state.ex_ip = [0,0,0,0]

if 'subnet' not in st.session_state:
    st.session_state.subnet = [0,0,0,0]

# css 
with open('./css/hello.css')as file:
    styl = f'<style>{file.read()})</style >'

st.markdown(styl, unsafe_allow_html=True)

# FAST API 연동
def saveInfo():
    data = {
        'a' : 1,
        'b' : 2
    }
    j_data = json.dumps(data)
    res = requests.post(url+'/web/internet/', j_data)
    print(27, res.text)

def getInfo():
    res = requests.get(url+'/web/internet/info/')
    info = res.json()

    if info['code'] == 200:
        info_ex_ip = info['data']['ex_ip'].split('.')
        info_subnet = info['data']['subnet'].split('.')
        print(info_ex_ip)
        print(info_subnet)
        st.session_state.ex_ip[0] = info_ex_ip[0]
        st.session_state.ex_ip[1] = info_ex_ip[1]
        st.session_state.ex_ip[2] = info_ex_ip[2]
        st.session_state.ex_ip[3] = info_ex_ip[3]
        
        st.session_state.subnet[0] = info_subnet[0]
        st.session_state.subnet[1] = info_subnet[1]
        st.session_state.subnet[2] = info_subnet[2]
        st.session_state.subnet[3] = info_subnet[3]
    else:
        print('server error')



# get data
df1 = pd.DataFrame(
    {
        "인터넷 정보": ['인터넷 연결 상태', '인터넷 연결 방식', '인터넷 연결 시간'],
        "" : ['인터넷에 연결됨', '동적 ip 연결         외부 ip 주소 : 111.111.111.1', '60일 19시간']
    }
)

# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """
# Draw UI
st.write("# Web Controller")

with st.container():
    col1, col2, col3 = st.columns([1,1,10])
    with col1:  
        if st.button('Save', use_container_width=True):
            print(49)
            saveInfo()
    
    with col2:
        if st.button('Refresh', use_container_width=True):
            getInfo()
            
st.markdown(f'<br/>', unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([5.5, 1, 5.5], gap="small")

    with col1:
        st.subheader(':blue[시스템 요약 정보]')
        # styler = df1.style.hide_index()
        # st.write(styler.to_html(), unsafe_allow_html=True)
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        st.dataframe(df1, use_container_width=True)

    with col3:
        st.subheader(':blue[인터넷 설정]')
        with st.container():
            genre = st.radio(
                "인터넷 설정 정보",
                ('동적 ip 방식', 'PPPoE', '고정 ip 방식'))

            if genre == '동적 ip 방식':
                st.write('')
            else:
                st.write("")

        with st.container():
            col1, col2, col3 = st.columns([3, 5, 4], gap="small")
            with col1:
                st.write('외부 IP주소')
                st.write('서브넷 마스크')
            with col2 :
                st.text_input('1', 'Life of Brian',label_visibility="collapsed")
                st.text_input('2', 'Life of Brian',label_visibility="collapsed")
            with col3 :
                agree = st.checkbox('사설 IP 할당 허용')

st.divider()
with st.container():
    col1, col2, col3= st.columns([5.5, 1, 5.5], gap="small")
    with col1:
        st.subheader(':blue[커넥션 제어]')
        with st.container():
            subcol1, subcol2, subcol3 = st.columns([2,7,3], gap="small")
            with subcol1:
                st.write('최대 커넥션 수')
                st.write('최소 커넥션 수')
            with subcol2:
                html3 = f"""
                    <div class="total-dc3">
                        <input type="text" style="height:30px; width:100%;">
                    </div>
                 
                     <div class="total-dc3">
                        <input type="text" style="height:30px; width:100%; margin-top:7px">
                    </div>
                    """
                st.markdown(html3, unsafe_allow_html=True)
            with subcol3:
                st.write('개 ( 0: 제한없음, 512 ~)')
                st.write('개 ( 0: 제한없음, 512 ~)')


    with col3:
        st.subheader(':blue[커넥션 정보]')
        st.write('전체 커넥션 정보')
        my_bar = st.progress(10)
        st.divider()
        st.write('IP별 커넥션 정보')
        my_bar2 = st.progress(0.05,'192.168.2.51')
        my_bar3 = st.progress(0.09,'192.168.2.68')

