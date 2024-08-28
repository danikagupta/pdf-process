import streamlit as st
import os
from datetime import datetime
from PIL import Image
import io
import base64


from langchain_community.llms import OpenAI
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


def onerun_llm_pages(paper, pages,model):
    dir=os.path.join("pdf_pages",paper)
    images = [os.path.join(dir,page) for page in pages]
    encoded_images = [encode_image_path(image) for image in images]
    st.image(images[0], caption=f'Front Page', use_column_width=True)

    default_question="""
    (1) read this paper and tell me if it ran any mycoremediation experiments
    (2) Create a table with 
      (a) One row for every experiment 
      (b) the columns having - dye, fungi type, length of experiment, concentration, pH, agitation, result and a final field for any other comments.
    
    Ensure that the concentration is of the dye. Add a separate column for concentration of fungi.
    """
    question=st.text_area("Ask question",value=default_question)
    if st.button("Run Analysis"):
        #st.write("You asked: ", question)
        chat = ChatOpenAI(model_name="gpt-4o-mini", max_tokens=3000)

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
        #print("Response: ", response)
        #st.write(response)
        st.subheader("Analysis Result:")
        st.write(response.content)
        # Extracting token usage information
        #st.subheader("Response metadata")
        response_metadata = response.response_metadata
        #st.write(response_metadata)
        #st.subheader("Token Usage")
        token_usage = response_metadata["token_usage"]
        #st.write(token_usage)
        st.subheader("Token Counts")
        completion_tokens = token_usage['completion_tokens']
        prompt_tokens = token_usage['prompt_tokens']
        total_tokens = token_usage['total_tokens']
        st.write(f"Completion Tokens: {completion_tokens}, Prompt Tokens: {prompt_tokens}, Total Tokens: {total_tokens}")

        # Printing the token counts
        st.write(f"Completion Tokens: {completion_tokens}")
        st.write(f"Prompt Tokens: {prompt_tokens}")
        st.write(f"Total Tokens: {total_tokens}")

def ui_one_llm_full_pdf():
    # Get the list of papers - this will be a list of directories under pdf_pages
    papers = os.listdir("pdf_pages")
    paper = st.selectbox("Select paper", papers,key="query-json")
    pages = os.listdir(os.path.join("pdf_pages", paper))
    pages.sort()
    onerun_llm_pages(paper, pages, model="gpt-4o-mini")

st.header("Query JSON")
ui_one_llm_full_pdf()
