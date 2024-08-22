import streamlit as st
from pdf2image import convert_from_bytes
import os

(col1,col2,col3)=st.tabs(["File upload","Col2","Col3"])

def pdf_to_images(uploaded_file):
    pdfReader = PyPDF2.PdfReader(uploaded_file)
    count = len(pdfReader.pages)
    images=[]
    for i in range(count):
        page = pdfReader.pages[i]
        images.append(page.to_image())
    return images

def col1code():
    st.write("This is column 1 XXX")
    st.markdown("# Upload file: PDF")
    uploaded_file=st.file_uploader("Upload PDF file",type="pdf")
    if uploaded_file is not None:
        images = convert_from_bytes(uploaded_file.read())
        output_dir = "pdf_pages"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        st.write(f"Total Pages: {len(images)}")
        for i, image in enumerate(images):
            output_path = os.path.join(output_dir, f'page_{i + 1}.png')
            image.save(output_path, 'PNG')
            st.image(image, caption=f'Page {i + 1}', use_column_width=True)
            st.write(f"Saved: {output_path}")        


def col2code():
    st.write("This is column 2 YYY")

def col3code():
    st.write("This is column 3 ZZZ")

with col1:
    st.write("File Upload")
    col1code()

with col2:
    st.write("This is column 2")
    col2code()

with col3:
    st.write("This is column 3")
    col3code()

