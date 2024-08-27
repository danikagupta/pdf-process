import streamlit as st
import os
from pdf2image import convert_from_bytes
import io
from PIL import Image
import base64

def process_one_file(pdfbytes,name="Unknown"):
    images = convert_from_bytes(pdfbytes)
    output_dir = "pdf_pages/"+name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    st.write(f"Total Pages: {len(images)}")
    st.session_state['total_pages'] = len(images)
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir, f'page_{i + 1}.png')
        image.save(output_path, 'PNG')
        st.image(image, caption=f'Page {i + 1}', use_column_width=True)
        st.write(f"Saved: {output_path}") 


uploaded_file=st.file_uploader("Upload PDF file",type="pdf")
fname=st.text_input("Enter file name")
if st.button("Upload") and uploaded_file is not None and fname is not None:
    process_one_file(uploaded_file.read(),name=fname)


st.divider()