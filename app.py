# Import from standard library
import os
import logging

# Import from 3rd party libraries
import streamlit as st

# Import modules from the local package
import stable_diffusion, chroma_cohere


def generate_prompt():

    st.session_state.text_error = ""

    if st.session_state.cohere_api_key == "":
        st.session_state.text_error = "Missed API key."
        return


    st.session_state.text_error = ""

    if st.session_state.file_path == "" or st.session_state.query == "":
        st.session_state.text_error = "Missed a file or query."
        return


    st.session_state.prompt_generate = ""
    st.session_state.text_error = ""

    with text_spinner_placeholder:
        with st.spinner("Please wait while we process your query..."):
            prompt = chroma_cohere.generate_prompt(query=st.session_state.query, file_path=st.session_state.file_path, cohere_api_key=st.session_state.cohere_api_key)

            if prompt == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return
            
            st.session_state.prompt_generate = (prompt)



def imagine():

    st.session_state.text_error = ""

    if st.session_state.stable_diffusion_api_key == "":
        st.session_state.text_error = "Missed API key."
        return


    st.session_state.text_error = ""

    if st.session_state.im_query == "":
        st.session_state.text_error = "Missed a query."
        return

    st.session_state.imagine = ""
    st.session_state.img_path = ""
    st.session_state.text_error = ""

    with text_spinner_placeholder:
        with st.spinner("Please wait while we generate your image..."):
            im_path = stable_diffusion.imagine(prompt=st.session_state.im_query, stable_diffusion_api_key=st.session_state.stable_diffusion_api_key)

            if im_path == "":
                st.session_state.text_error = "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                logging.info(f"Text Error: {st.session_state.text_error}")
                return
            
            st.session_state.img_path = (im_path)




# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)



# Configure Streamlit page and state
st.set_page_config(page_title="Imagine", page_icon="🍩")


# Store the initial value of widgets in session state
if "imagine" not in st.session_state:
    st.session_state.imagine = ""

if "img_path" not in st.session_state:
    st.session_state.img_path = ""

if "query" not in st.session_state:
    st.session_state.query = ""

if "im_query" not in st.session_state:
    st.session_state.im_query = ""

if "prompt_generate" not in st.session_state:
    st.session_state.prompt_generate = ""

if "file_path" not in st.session_state:
    st.session_state.file_path = ""

if "text_error" not in st.session_state:
    st.session_state.text_error = ""

if "cohere_api_key" not in st.session_state:
    st.session_state.cohere_api_key = ""

if "stable_diffusion_api_key" not in st.session_state:
    st.session_state.stable_diffusion_api_key = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"



# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# Render Streamlit page
with st.sidebar:
    st.session_state.cohere_api_key = st.text_input('Cohere API Key', )
    st.session_state.stable_diffusion_api_key = st.text_input('Stable Diffusion API Key', )


# title of the app
st.title("Chroma + Cohere + Stable Diffusion Tutorial")


st.markdown(
    "This is a demo of the Chroma + Cohere + Stable Diffusion model."
)


# file upload
file = st.file_uploader(label="Upload file", type=["pdf",])
if file is not None:
    filename = "book.pdf"
    with open(filename, "wb") as f:
        f.write(file.getbuffer())
    st.session_state.file_path = "book.pdf"


# textarea
st.session_state.query = st.text_area(
    label="Query the document",
    placeholder="Harry Potter as Balenciaga runway model", height=100)


# button
st.button(
    label="Generate Prompt",
    help="Click to genearate prompt",
    key="generate_prompt",
    type="primary",
    on_click=generate_prompt,
    )


# textarea
st.session_state.im_query = st.text_area(label="Image description", placeholder="Harry Potter as Balenciaga runway model", height=100)


# button
st.button(
    label="Generate image",
    help="Click to genearate image",
    key="generate_image",
    type="primary",
    on_click=imagine,
    )


text_spinner_placeholder = st.empty()
if st.session_state.text_error:
    st.error(st.session_state.text_error)


if st.session_state.prompt_generate:
    st.markdown("""---""")
    st.text_area(label="Generated Prompt", value=st.session_state.prompt_generate,)


if st.session_state.img_path:
    st.markdown("""---""")
    st.subheader("Image generated by Stable Diffusion")
    st.image(st.session_state.img_path, use_column_width=True, caption="Image generated by Stable Diffusion", output_format="PNG")