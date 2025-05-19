import streamlit as st
import pandas as pd

from streamlit_pdf_viewer import pdf_viewer

if 'pdf_list' not in st.session_state:
    st.write("请先进行搜索")
else:
    pdf_list = st.session_state.pdf_list

    pdf_df = pd.DataFrame(
        pdf_list, 
        columns=['URL', 'Title', 'FilePath'],
    )
    st.dataframe(
        pdf_df,
        key="pdf_df",
        on_select="rerun",
        selection_mode=["single-row"],
        hide_index=True
    )
    
    if len(st.session_state.pdf_df.selection['rows']) != 0:
        row = int(st.session_state.pdf_df.selection['rows'][0])
        file_path = pdf_df.loc[row,'FilePath']
        with st.status("Loading...", expanded=True) as status:
            pdf_viewer(file_path)
            status.update(label="Loading Complete!", state="complete")
    else:
        pass