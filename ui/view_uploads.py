import streamlit as st
import os


def show_past_uploads():
    # Walk through all files in pdf_pages and show number of pages by counting number of files
    upload_list=[]
    if os.path.exists("pdf_pages"):
        for file in os.listdir("pdf_pages"):
            #st.write(f"File: {file} has {len(os.listdir(os.path.join('pdf_pages',file)))} pages")
            upload_list.append({"file":file,"pages":len(os.listdir(os.path.join('pdf_pages',file)))})
    st.dataframe(upload_list,hide_index=True)


st.header("Past uploads")
show_past_uploads()
st.divider()