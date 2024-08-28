import streamlit as st

from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

from unstructured.staging.base import dict_to_elements


def process_file_core(file_contents, file_name):
    s=UnstructuredClient(api_key_auth=st.secrets['UNSTRUCTURED_API_KEY'])

    files=shared.Files(
        content=file_contents,
        file_name=file_name,
    )

    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
        skip_infer_table_types=[],
        pdf_infer_table_structure=True,
    )

    try:
        resp = s.general.partition(req)
        elements = dict_to_elements(resp.elements)
    except SDKError as e:
        print(e)

    tables = [el for el in elements if el.category == "Table"]
    st.write("# START")
    final_text=""
    for t in tables:
        table_html = t.metadata.text_as_html
        final_text += table_html
        st.write(table_html)
    st.write("# COMPLETE")
    alt_text="\n\n".join([str(el) for el in elements])
    return resp, elements, tables, final_text,alt_text

def process_file(file_contents, file_name):
    st.write(f"Processing file: {file_name}")
    resp, elements, tables, final_text,alt_text = process_file_core(file_contents, file_name)
    st.write("Tables: ", len(tables))
    st.write("Elements: ", len(elements))
    st.write("Response: ", resp)
    st.write("Final text: ", final_text)
    st.write("Elements: ", elements)
    st.write("Tables: ", tables)
    st.write("Alt text: ", alt_text)