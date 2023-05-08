import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import requests
import os

server_url = 'http://192.168.2.52:60000'
if_url = 'http://192.168.2.52:6006/#scalars'

if 'obj_default_options' not in st.session_state:
    st.session_state.default_options = ''

if 'obj_aug_options' not in st.session_state:
    st.session_state.aug_options = ''

if 'ins_default_options' not in st.session_state:
    st.session_state.default_options = ''

if 'ins_aug_options' not in st.session_state:
    st.session_state.aug_options = ''

if 'key_default_options' not in st.session_state:
    st.session_state.default_options = ''

if 'key_aug_options' not in st.session_state:
    st.session_state.aug_options = ''

# css 
with open('./css/segtool.css')as file:
    styl = f'<style>{file.read()})</style >'

st.markdown(styl, unsafe_allow_html=True)

class Element:
    def drawChkbox(k, v):
        chked_v = st.checkbox(k, value=v, label_visibility="collapsed")
        return chked_v

    def drawSlider(k,min,max,v):
        sld_v = st.slider(k, min_value = min, max_value = max, value = v, label_visibility="collapsed")
        return sld_v

    def drawCombo(k,o):
        option = st.selectbox(k, options=o, label_visibility="collapsed")
        return option

    def drawTextInput(k, v):
        txt_v = st.text_input(k, v, label_visibility="collapsed")
        return txt_v

ele = Element

def getObjDetc(urlOption, tapOption):
    res = requests.get(server_url+urlOption)
    data = res.json()

    if tapOption == 'obj':
        st.session_state.obj_default_options = data['default_options']
        st.session_state.obj_aug_options = data['aug_options']
        #grouping
        GeometryTransform = []
        ImageTransform = []
        BorderOrientation = []
        for i, aug in enumerate(st.session_state.obj_aug_options):
            if i < 5:
                GeometryTransform.append(aug)
            elif i>=5 and i<10:
                ImageTransform.append(aug)
            else:
                BorderOrientation.append(aug)

        drawInfo(st.session_state.obj_default_options, tapOption)

        for i in st.session_state.obj_aug_options:
            if GeometryTransform[0] == i:
                st.subheader('Geometry Transform')
            elif ImageTransform[0] == i:
                st.subheader('Image Transform')
            elif BorderOrientation[0] == i:
                st.subheader('Border Orientation')
            else:
                st.empty()

            drawAug(st.session_state.obj_aug_options[i], tapOption)

    elif tapOption == 'ins':
        st.session_state.ins_default_options = data['default_options']
        st.session_state.ins_aug_options = data['aug_options']

        drawInfo(st.session_state.ins_default_options, tapOption)

        for i in st.session_state.ins_aug_options:
            drawAug(st.session_state.ins_aug_options[i], tapOption)
    
    else:
        st.session_state.key_default_options = data['default_options']
        st.session_state.key_aug_options = data['aug_options']

        drawInfo(st.session_state.key_default_options, tapOption)

        for i in st.session_state.key_aug_options:
            drawAug(st.session_state.key_aug_options[i], tapOption)


def getPrjNm(json_data, objUrlOption, gubun):
    if gubun == 'obj':
        i_prjnm = st.session_state.obj_default_options['ProjectName']['textinput']['value']
    elif gubun == 'ins':
        i_prjnm = st.session_state.ins_default_options['ProjectName']['textinput']['value']
    else:
        i_prjnm = st.session_state.key_default_options['ProjectName']['textinput']['value']
    res = requests.get(server_url + objUrlOption + i_prjnm)
    data = res.json()
    prjNm = data['project_name']
    saveSetData(prjNm, json_data, objUrlOption)

def saveSetData(prjNm, json_data, objUrlOption):
    res = requests.post(server_url+ objUrlOption + prjNm+'/'+'json', data=json_data)
    print(117, res.json)


def drawInfo(default_options, tapOption):
    for i,k in enumerate(default_options.keys()):
        with st.container():
            s_col1, s_col2 = st.columns([4, 7], gap="small")
            with s_col1:
                st.text(k)
            with s_col2:
                if default_options[k]['menus'][0]=='textinput':
                    default_options[k]['textinput']['value'] = ele.drawTextInput(k+tapOption, default_options[k]['textinput']['value'])
                elif default_options[k]['menus'][0]=='category':
                    default_options[k]['category']['value'] = ele.drawCombo(k+tapOption, default_options[k]['category']['list'])
                else:
                    st.empty()

# def drawGroupTitle(aug_options, tapOption):


def drawAug(aug_options, tapOption):
    menu_cnt = 1
    for i in range(0, len(aug_options['menus'])):
        menu_cnt += 1

    subcol1, subcol2, subcol3, subcol4= st.columns([3, 1, 3.5, 3.5])
    with subcol1:
        if menu_cnt >=1:         
            st.text(aug_options['title'])
        else:
            st.empty()  
    with subcol2:
        if menu_cnt >=2:
            menu = aug_options[aug_options['menus'][0]]
            if menu['menu'] == 'checkbox':
                menu['value'] = ele.drawChkbox(aug_options['title']+tapOption, menu['value'])      
        else:
            st.empty()
    with subcol3:      
        if menu_cnt >=3:
            menu = aug_options[aug_options['menus'][1]]
            if menu['menu'] == 'sliderbar':
                menu['value'] = ele.drawSlider(aug_options['title']+tapOption, menu['min'], menu['max'], menu['value'])
        else:
            st.empty()
    with subcol4:
        if menu_cnt >= 4:
            menu = aug_options[aug_options['menus'][2]]
            if menu['menu'] == 'sliderbar':
                menu['value'] = ele.drawSlider(aug_options['title']+tapOption, menu['min'], menu['max'], menu['value'])
            elif menu['menu'] == 'combobox':
                menu['value'] = ele.drawCombo(aug_options['title']+tapOption, menu['list'])
        else:
            st.empty()

def drawMainPage(urlOption, gubun):
     with st.container():
        col2, col3 = st.columns([8, 4], gap="small")
        with col2:
            components.iframe(if_url, height=860)
        with col3:
            file_sel = '''
                <label className="input-file-button" for="input-file1">
                    이미지 경로를 선택하여주세요.
                    <input type="file" id="input-file1" style="display: none;"/>
                </label>
                <br />
                <label className="input-file-button" for="input-file2">
                    라벨 경로를 선택하여주세요.
                    <input type="file" id="input-file2" style="display: none;"/>
                </label>   
            '''
            st.markdown(f'{file_sel}', unsafe_allow_html=True)

            # file = st.file_uploader("이미지 경로를 선택하여주세요.", key='f_'+gubun)
            # if file is not None:            
            #     print(119, os.path.dirname(os.path.realpath(file.name)))
            
            # file = st.file_uploader("라벨 경로를 선택하여주세요.", key='l_'+gubun)
            # if file is not None:            
            #     print(119, os.path.dirname(os.path.realpath(file.name)))

            if st.button('AUG 실행', use_container_width=True, key='b_'+gubun):
                if gubun == 'obj':
                    json_data = {
                        "default_options" : st.session_state.obj_default_options,
                        "aug_options" : st.session_state.obj_aug_options
                    }
                    print(184, st.session_state.obj_aug_options['RandomPerspectiveTransform'])
                    # save data 
                    getPrjNm(json_data, urlOption, gubun)

                elif gubun == 'ins':
                    json_data = {
                        "default_options" : st.session_state.ins_default_options,
                        "aug_options" : st.session_state.ins_aug_options
                    }
                    print(193, st.session_state.ins_aug_options['RandomPerspectiveTransform'])
                    # save data 
                    getPrjNm(json_data, urlOption, gubun)
                else:
                    json_data = {
                        "default_options" : st.session_state.key_default_options,
                        "aug_options" : st.session_state.key_aug_options
                    }
                    print(201, st.session_state.key_aug_options['RandomPerspectiveTransform'])
                    # save data 
                    getPrjNm(json_data, urlOption, gubun)


            #get server data           
            getObjDetc(urlOption, gubun)

# Draw UI
tab1, tab2, tab3 = st.tabs(["OBJECT DETECTION", "INSTANCE SEGMENTATION", "KEYPOINT DETECTION"])
tabs_font_css = """
    <style>
        button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
            font-size: 17px;
            }
        }
    </style>
"""
st.write(tabs_font_css, unsafe_allow_html=True)
with tab1:
    objUrlOption = '/object-detection/'
    drawMainPage(objUrlOption, 'obj')
with tab2:
    insUrlOption = '/instance-segmentation/'
    drawMainPage(insUrlOption, 'ins')
with tab3:
    keyUrlOption = '/keypoint-detection/'
    drawMainPage(keyUrlOption, 'key')
