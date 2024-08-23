import streamlit as st
from pdf2image import convert_from_bytes
import os

import io
import base64

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from PIL import Image

(col1,col2,col3)=st.tabs(["File upload","Ask question","Future use"])
if 'total_pages' not in st.session_state:
    st.session_state['total_pages'] = 0

os.environ["OPENAI_API_KEY"]=st.secrets["OPENAI_API_KEY"]

def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def encode_image_path(png_path):
    with Image.open(png_path) as image:
        # Convert image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

def col1code():
    uploaded_file=st.file_uploader("Upload PDF file",type="pdf")
    if uploaded_file is not None:
        images = convert_from_bytes(uploaded_file.read())
        output_dir = "pdf_pages"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        st.write(f"Total Pages: {len(images)}")
        st.session_state['total_pages'] = len(images)
        for i, image in enumerate(images):
            output_path = os.path.join(output_dir, f'page_{i + 1}.png')
            image.save(output_path, 'PNG')
            st.image(image, caption=f'Page {i + 1}', use_column_width=True)
            st.write(f"Saved: {output_path}")        


def col2code():
    st.write("Pages: ", st.session_state['total_pages'])
    if st.session_state['total_pages']>0:
        page_number = st.number_input("Enter page number", min_value=1, max_value=st.session_state['total_pages'])
        st.write("You entered: ", page_number)
        image_path = os.path.join("pdf_pages", f'page_{page_number}.png')
        st.image(image_path, caption=f'Page {page_number}', use_column_width=True)
        if question:=st.text_input("Ask question"):
            st.write("You asked: ", question)
            st.write("Answer: ", "This is a dummy answer")
            base64_image = encode_image_path(image_path)

            # Set up ChatOpenAI model
            chat = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=300)

            # Prepare messages
            messages = [
                SystemMessage(content="You are an AI assistant capable of analyzing images and text."),
                HumanMessage(content=[
                    {
                        "type": "text",
                        "text": f"Analyze the following image and respond to the user's prompt: {question}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                    }
                ])
            ]

            # Get the response
            response = chat(messages)

            # Display the result
            st.subheader("Analysis Result:")
            st.write(response.content)

def col3code():
    st.write("This is column 3 ZZZ")

with col1:
    st.write("File Upload")
    col1code()

with col2:
    st.write("Ask question")
    col2code()

with col3:
    st.write("Future use")
    col3code()

