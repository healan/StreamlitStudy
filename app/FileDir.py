import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
import os, os.path, time, sys
from pathlib import Path
import datetime
import shutil
from distutils.dir_util import copy_tree
from streamlit.components.v1 import html
import tqdm
import threading
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, as_completed
from streamlit.runtime.scriptrunner import add_script_run_ctx
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
# from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
import uuid
from streamlit_javascript import st_javascript
import execute
import selenium
from selenium import webdriver
from streamlit_ws_localstorage import injectWebsocketCode, getOrCreateUID
from streamlit_server_state import server_state, server_state_lock
from stqdm import stqdm


with open('./css/filedir.css')as file:
    styl = f'<style>{file.read()})</style >'

st.markdown(styl, unsafe_allow_html=True)

if 'from_path' not in st.session_state:
    st.session_state.from_path = ''

if 'dst_path' not in st.session_state:
    st.session_state.dst_path = ''

if 'cur_sel' not in st.session_state:
    st.session_state.cur_sel = ''

with server_state_lock["th"]: 
    if "th" not in server_state:
        server_state.th = []

my_js = """
    window.onload = function(){
        console.log(50);
    };

    window.addEventListener("scroll", function () {
        console.log(53);
    });

    window.addEventListener('beforeunload', function(event) {
        console.log('I am the 1st one.');
    });

    window.addEventListener('unload', function(event) {
        console.log('I am the 3rd one.');
    });
"""

# Wrapt the javascript as html code
my_html = f"<script>{my_js}</script>"

# Execute your app
html(my_html,height=0)

class Mycopier(threading.Thread):   
    def __init__(self, number, cnt ,pbar, progress_rate):
        threading.Thread.__init__(self)
        self._return = None
        self.number = number
        self.cnt = cnt
        self.my_thread_bar = pbar
        self.progress_rate = progress_rate

    def add_num(self):
        for i in range(self.progress_rate, self.number):
            time.sleep(0.3) #1초 후
            self.progress_rate += 1
            self.my_thread_bar.progress(self.progress_rate, text='my thread progress: '+str(self.cnt))
            print('thread', self.cnt, 'start!', 'total:', i + 1, 'progressrate : ', self.progress_rate) 
        
    def run(self):
        print(81)
        threading.Thread(target=self.add_num())
        return 0 

    

class FolderMng:
        
    def scan_folder(path, option):
        if(path != ''):
            try:
                for e in os.scandir(path):
                    if e.is_dir():
                        if st.button(f":file_folder: {e.name}", key=option+e.name, use_container_width=True):
                            st.session_state.cur_sel = option+e.name
                            if option =='from':
                                st.session_state.from_path = e.path
                            else:
                                st.session_state.dst_path = e.path

                    if e.is_file():
                        statinfo = os.lstat(e.path)
                        modify_date = datetime.datetime.fromtimestamp(statinfo.st_mtime)
                        extension = os.path.splitext(e.path)[1]
                        file_size = statinfo.st_size
                        if option =='from':
                            if st.button(f":page_with_curl: {e.name} {modify_date} {extension} {file_size}", key=option+e.name, use_container_width=True):
                                st.session_state.from_path = e.path
                        else:
                            if st.button(f":page_with_curl: {e.name} {modify_date} {extension} {file_size}", key=option+e.name, use_container_width=True):
                                st.session_state.dst_path = e.path
            except OSError as error:
                if error.errno == 20:
                    st.session_state.cur_sel = error.filename
                else:
                    print(error)


    def parent_folder(option):
        if option == 's':
            st.session_state.from_path = Path(st.session_state.from_path).parent
        if option == 'd':
            st.session_state.dst_path = Path(st.session_state.dst_path).parent

    
    def copy_file_with_progress(src_path,dest_path,block_size=1024*1024):
        total_size = os.path.getsize(src_path)
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        copyedbuf=0       

        # Progress <-- MyCopyer. 
        with open(src_path, 'rb') as src_file:
            with open(dest_path, 'wb') as dest_file:
                for p in range(0, 100):
                    buf = src_file.read(block_size)
                    if not buf:
                        break
                    copyedbuf += len(buf)
                    print(105, p, copyedbuf)
                    # dest_file.write(buf)
                    print(int((copyedbuf/total_size)*100))
                    my_bar.progress(int((copyedbuf/total_size)*100), text=progress_text)

                    # bar = f'<div class ="progress">{}</div>'
                    # st.markdown(bar, unsafe_allow_html=True)           
        #         with tqdm.tqdm(total=total_size, unit='B', unit_scale=True, desc='Copying', leave=True) as progress_bar:
        #             while True:
        #                 buf = src_file.read(block_size)
        #                 if not buf:
        #                     break
        #                 dest_file.write(buf)
        #                 progress_bar.update(len(buf))
                        
        #                 print(progress_bar.desc)               
        # bar = f'<div class="progress">{progress_bar}</div>'
        # st.markdown(bar, unsafe_allow_html=True)

folderMng = FolderMng
copier = Mycopier

st.title('파일 관리 프로그램')


# for i in range(1,3):
#     globals()['my_thread_bar_{}'.format(i)] = st.progress(0)
my_thread_bar1 = st.progress(0)
my_thread_bar2 = st.progress(0)

runtime = get_instance()
session_id = get_script_run_ctx().session_id
print(152, session_id)
session_info = runtime._session_mgr.get_session_info(session_id)
print(154, session_info)

if len(server_state.th) > 0 :
   
    print(163, server_state.progress_rate)

    if server_state.progress_rate != 0:
        print(166)

# print(156, server_state.th)
# if server_state.th != 0:
#     print(226, server_state.progress_rate)
#     my_thread_bar1_a = st.progress(server_state.progress_rate)
#     for i in range(server_state.progress_rate, 100):
#         time.sleep(0.5) #1초 후
#         my_thread_bar1_a.progress( i + 1, text='my thread progress')

with st.container():
    col1, col2, col3, col4 = st.columns([1,1,1,9], gap="small")
    with col2:
        btn_copy = st.button('복사', key='Copy', type='primary')
        control = st.empty()
        message = st.empty()
        work1 = ''
        work2 = ''
        
        if btn_copy:
            # THREAD    
            with ThreadPoolExecutor(2) as excutor:
                try:
                    print('Thread start')
                    # ctx = get_script_run_ctx()
                    with server_state_lock["progress_rate"]:  
                        print(181)
                        if "progress_rate" not in server_state:
                            server_state.progress_rate = 0
                        work1 = excutor.submit(Mycopier(100, 0, my_thread_bar1, server_state.progress_rate).run)

                    with server_state_lock["progress_rate2"]: 
                        print(192)
                        if "progress_rate2" not in server_state:
                            server_state.progress_rate2 = 0                  
                        work2 = excutor.submit(Mycopier(100, 1, my_thread_bar2, server_state.progress_rate2).run)

                except RuntimeError as e:
                    print('200RuntimeError : ', e)
                except Exception as e:
                    print('202Exception : ', e)

                with server_state_lock.th:
                    for t in excutor._threads:
                        add_script_run_ctx(t)
                        server_state.th.append(t)
                        print(193, len(server_state.th))

                with server_state_lock.th:
                    for future in as_completed([work1, work2]):
                        server_state.th.pop(future.result())
                        print('212Thread end', future.result())           
           
            # if os.path.isfile(st.session_state.from_path):
            #     st.session_state.copy_status='Y'
            #     filename = os.path.basename(st.session_state.from_path)
            #     print(69, st.session_state.from_path, os.path.join(st.session_state.dst_path,filename))
            #     # shutil.copy2(st.session_state.from_path, os.path.join(st.session_state.dst_path,filename))
            #     folderMng.copy_file_with_progress(st.session_state.from_path, os.path.join(st.session_state.dst_path,filename))
            # elif os.path.isdir(st.session_state.from_path):
            #     print(71, st.session_state.from_path, st.session_state.dst_path)
            #     copy_tree(st.session_state.from_path, st.session_state.dst_path)
            # else:
            #     print('unknown format')
    with col3:
        st.button('이미지편집', key='modifyImg', type='primary')


st.markdown(f'</br>', unsafe_allow_html=True)
with st.container():
    col1, col2, col3, col4 = st.columns([0.5, 5.5, 5.5, 0.5], gap="small")
    with col2:
        st.subheader('SRC FOLDER')
        st.session_state.from_path = st.text_input('from_path', st.session_state.from_path, label_visibility='collapsed')
    with col3:
        st.subheader('DST FOLDER')
        st.session_state.dst_path = st.text_input('dst_path', st.session_state.dst_path, label_visibility='collapsed')

with st.container():
    col1, col2, col3, col4 = st.columns([1, 5 ,5, 1], gap="small")
    with col2:
        subcol1, subcol2= st.columns([11,1], gap="small")
        with subcol1:
            if st.session_state.from_path != '': 
                st.button("..", key='srcBack', on_click=folderMng.parent_folder, args=('s'), use_container_width=True)
                folderMng.scan_folder(st.session_state.from_path, 'from')

    with col3:
        subcol1, subcol2,subcol3 = st.columns([1,10,1], gap="small")
        with subcol2:
            if st.session_state.dst_path != '': 
                st.button("..", key='dstBack', on_click=folderMng.parent_folder, args=('d'), use_container_width=True)
                folderMng.scan_folder(st.session_state.dst_path, 'dst')


