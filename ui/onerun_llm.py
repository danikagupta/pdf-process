import streamlit as st
import os
from datetime import datetime
from PIL import Image
import io
import base64

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage


def encode_image_path(png_path):
    with Image.open(png_path) as image:
        # Convert image to bytes
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()

def encode_multiple_images(images):
    msg=HumanMessage(content=[
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            } for base64_image in images
            ])
    return msg

def onerun_llm(paper, pages,model):
    dir=os.path.join("pdf_pages",paper)
    images = [os.path.join(dir,page) for page in pages]
    encoded_images = [encode_image_path(image) for image in images]
    for i,image in enumerate(images):
        st.image(image, caption=f'Page {i+1}', use_column_width=True)


    if question:=st.text_input("Ask question"):
        st.write("You asked: ", question)
        chat = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=300)

        messages = [
            SystemMessage(content="You are an AI assistant capable of analyzing images and text."),
            HumanMessage(content=[
                {
                    "type": "text",
                    "text": f"Analyze the following images and respond to the user's prompt: {question}"
                }
            ]),
            encode_multiple_images(encoded_images)
        ]

        response = chat(messages)
        st.subheader("Analysis Result:")
        st.write(response.content)

def ui_one_llm():
    # Get the list of papers - this will be a list of directories under pdf_pages
    papers = os.listdir("pdf_pages")
    paper = st.selectbox("Select paper", papers)
    pages = os.listdir(os.path.join("pdf_pages", paper))
    pages.sort()
    pagecount=len(pages)
    pagechoice=[f"{i+1}" for i in range(pagecount)]
    pagechoices = st.multiselect("Select pages", pagechoice)
    pages=[pages[int(page)-1] for page in pagechoices]
    st.write(f"Selected pages: {pages}")
    onerun_llm(paper, pages,model="gpt-4o-mini")

st.header("One LLM")
ui_one_llm()
st.divider()
#st.header("AIClub LGS Page 1,2")
#onerun_llm("AIClub-LGS",["page_001.png","page_002.png"],"gpt-4o-mini")
