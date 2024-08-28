import streamlit as st
import os

from unstructued_io import process_file

def main():
    st.title("Unstructured Data Processing")
    papers = os.listdir("pdf_full")
    paper = st.selectbox("Select paper", papers,key="test-component")
    if st.button("Run Analysis"):
        fqfn=os.path.join("pdf_full", paper)
        with open(fqfn, "rb") as f:
            file_contents = f.read()
        process_file(file_contents, paper)


main()