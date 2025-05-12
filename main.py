import os
import streamlit as st

from dotenv import load_dotenv

from utils.common import clean_blank, load_config
from utils.get_html import download_pdfs, extract_pdf_links, extract_title_list, fetch_html

# 初始化工作
load_dotenv() ## 加载环境变量
config = load_config() ## 加载配置

data_dir = config['data_dir']
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

with st.sidebar:
    st.title("Arxiv Paper Collector")

with st.chat_message("assistant"):
    st.markdown("请输入关键词")

keypoint_query = st.chat_input("请输入")
if keypoint_query:
    keypoint_query_list = clean_blank(keypoint_query).split(" ")
    with st.chat_message("human"):
        st.markdown("\n".join([f"- {item}" for item in keypoint_query_list]))

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

        pdf_list = pdf_list[:config['max_num']]
        title_list = title_list[:config['max_num']]

        st.markdown("搜索到以下pdf" + '\n' + "\n".join([f"- {pdf_list[idx]}, {title_list[idx]}" for idx in range(len(pdf_list))]))

    with st.chat_message("assistant"):
        with st.status("Downloading...", expanded=True) as status:
            for idx, pdf in enumerate(pdf_list):
                st.markdown(f"- 正在下载：{pdf}")
                download_pdfs([pdf], data_dir + '/save_pdfs')
            
            status.update(label="Downloading Complete!", state="complete", expanded=False)