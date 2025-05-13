import os
import base64
import streamlit as st
import pandas as pd

from dotenv import load_dotenv

from streamlit_pdf_viewer import pdf_viewer
from utils.common import clean_blank, load_config
from utils.get_html import download_pdfs, extract_pdf_links, extract_title_list, fetch_html

# 初始化工作
load_dotenv() ## 加载环境变量
config = load_config() ## 加载配置

## 设置数据保存路径
data_dir = config['data_dir']
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

## 设置session变量
if 'pdf_list' not in st.session_state:
    st.session_state.pdf_list = []

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": {
            "type": "text",
            "text": "请输入关键词"
        }
    })

# 加载页面
## 加载侧边栏
with st.sidebar:
    st.title("Arxiv Paper Collector")

## 加载主页面
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["content"]["type"] == "text":
            st.markdown(message["content"]["text"])
        elif message["content"]["type"] == "status":
            with st.status(label=message["content"]['status']['label'], state=message["content"]['status']['state'], expanded=message["content"]['status']['expanded']):
                for text in message["content"]['status']['texts']:
                    st.markdown(text)

# with st.chat_message("assistant"):
#     st.markdown("请输入关键词")

keypoint_query = st.chat_input("请输入关键词，以空格分隔")
if keypoint_query:
    keypoint_query_list = clean_blank(keypoint_query).split(" ")
    with st.chat_message("human"):
        st.markdown("  \n".join([f"{item}" for item in keypoint_query_list]))
        st.session_state.messages.append({
            "role": "human",
            "content": {
                "type": "text",
                "text": "  \n".join([f"{item}" for item in keypoint_query_list])
            }
        })

    keypoint = "+".join(keypoint_query_list)
    base_url = config['url'] # https://arxiv.org/search
    # https://arxiv.org/search/?query=LLM+RL&searchtype=all&abstracts=show&order=-announced_date_first&size=50
    search_url = base_url + f'/?query={keypoint}' + '&searchtype=all&abstracts=show&order=-announced_date_first&size=25'

    with st.chat_message("assistant"):
        with st.status("Searching...", expanded=True) as status:
            st.markdown("- 正在搜索：" + search_url)
            html = fetch_html(search_url)

            st.markdown("- 正在保存中间结果")
            with open(os.path.join(data_dir, 'paper.html'), "w", encoding='utf-8') as f:
                f.write(html)

            st.markdown("- 正在获取PDF链接")
            pdf_list = extract_pdf_links(html)
            title_list = extract_title_list(html)
            assert len(pdf_list) == len(title_list)

            status.update(label="Searching Complete!", state="complete", expanded=False)

        st.session_state.messages.append({
            "role": "assistant",
            "content": {
                "type": "status",
                "status": {
                    "label": "Searching Complete!",
                    "state": "complete",
                    "expanded": False,
                    "texts": [
                        "- 正在搜索：" + search_url,
                        "- 正在保存中间结果",
                        "- 正在获取PDF链接"
                    ]
                }
            }
        })
        pdf_list = pdf_list[:config['max_num']]
        title_list = title_list[:config['max_num']]

        st.markdown("搜索到以下pdf" + '\n' + "\n".join([f"- {pdf_list[idx]}, {title_list[idx]}" for idx in range(len(pdf_list))]))
        st.session_state.messages.append({
            "role": "assistant",
            "content": {
                "type": "text",
                "text": "搜索到以下pdf" + '\n' + "\n".join([f"- {pdf_list[idx]}, {title_list[idx]}" for idx in range(len(pdf_list))])
            }
        })

    with st.chat_message("assistant"):
        with st.status("Downloading...", expanded=True) as status:
            for idx, pdf in enumerate(pdf_list):
                st.markdown(f"- 正在下载：{pdf}")
                saved_paths = download_pdfs([pdf], data_dir + '/save_pdfs')
                st.session_state.pdf_list.append((pdf, title_list[idx], saved_paths[0]))
            
            status.update(label="Downloading Complete!", state="complete", expanded=False)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": {
                "type": "status",
                "status": {
                    "label": "Downloading Complete!",
                    "state": "complete",
                    "expanded": False,
                    "texts": [
                        "- 正在下载：" + pdf for pdf in pdf_list
                    ]
                }
            }
        })