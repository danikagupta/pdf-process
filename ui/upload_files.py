import streamlit as st
import os
from pdf2image import convert_from_bytes
import io
from PIL import Image
import base64

def process_one_file(pdfbytes,name="Unknown"):
    output_dir1 = "pdf_full"
    if not os.path.exists(output_dir1):
        os.makedirs(output_dir1)
    output_path1 = os.path.join(output_dir1, f'{name}.pdf')
    with open(output_path1, 'wb') as f:
        f.write(pdfbytes)
    images = convert_from_bytes(pdfbytes)
    output_dir2 = "pdf_pages/"+name
    if not os.path.exists(output_dir2):
        os.makedirs(output_dir2)
    st.write(f"Total Pages: {len(images)}")
    st.session_state['total_pages'] = len(images)
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir2, f'page_{i + 1:03}.png')
        image.save(output_path, 'PNG')
        st.image(image, caption=f'Page {i + 1}', use_column_width=True)
        st.write(f"Saved: {output_path}") 



st.header("Upload PDF files")
uploaded_file=st.file_uploader("Upload PDF file",type="pdf")
fname=st.text_input("Enter file name")
if st.button("Upload") and uploaded_file is not None and fname is not None:
    process_one_file(uploaded_file.read(),name=fname)
st.divider()
