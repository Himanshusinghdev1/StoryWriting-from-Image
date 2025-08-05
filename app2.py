import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO

# CONFIGURATION (set your Hugging Face API key in HF_TOKEN env variable)
FLORENCE2_MODEL = "microsoft/Florence-2-large-ft"
STORY_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
MAX_CAPTION_TOKENS = 64
MAX_STORY_TOKENS = 700

# Utility: Call Hugging Face image captioning API (Florence-2)
def generate_caption(image_bytes, hf_token):
    api_url = f"https://api-inference.huggingface.co/models/{FLORENCE2_MODEL}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    files = {"image": image_bytes}
    payload = {
        "parameters": {"max_new_tokens": MAX_CAPTION_TOKENS},
        "options": {"wait_for_model": True}
    }
    response = requests.post(api_url, headers=headers, files=files, data={"inputs": ""})
    result = response.json()
    # Florence-2 output: [{"generated_text": "caption ..."}]
    caption = result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else str(result)
    return caption.strip()

# Utility: Call TogetherAI/HF Llama model API for story generation
def generate_story(caption, theme, word_limit, hf_token):
    prompt = (
        f"Expand the following image description into a {theme} story of around {word_limit} words. "
        "Be creative, engaging, and vivid.\n\n"
        f"Image Description: {caption}\n\nStory:"
    )
    api_url = f"https://api-inference.huggingface.co/models/{STORY_MODEL}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    data = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": MAX_STORY_TOKENS,
            "temperature": 0.75,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
            "do_sample": True
        },
        "options": {"wait_for_model": True}
    }
    response = requests.post(api_url, headers=headers, json=data)
    result = response.json()
    # Llama output: [{"generated_text": "..."}]
    story = result[0]["generated_text"] if isinstance(result, list) and "generated_text" in result[0] else str(result)
    # Remove the prompt if included
    if "Story:" in story:
        story = story.split("Story:", 1)[-1].strip()
    return story.strip()

# Streamlit UI
st.set_page_config(page_title="Image-to-Story Generator", layout="wide")
st.title("📝 Image to Story Generator with AI")

st.markdown(
    "Turn your images into captivating stories! Upload an image, select a theme and word limit, and let AI do the magic."
)
hf_token = st.secrets["HF_API_KEY"] if "HF_API_KEY" in st.secrets else st.text_input("Enter your Hugging Face API token:", type="password")

with st.form(key="image_story_form"):
    uploaded_img = st.file_uploader("Upload an image (jpg/png)", type=['jpg', 'jpeg', 'png'])

    theme = st.text_input("Story Theme", value="adventure")
    word_limit = st.number_input("Word Limit (100–1000)", value=400, min_value=100, max_value=1000, step=50)
    submit = st.form_submit_button("Generate Story")

if submit and uploaded_img and hf_token:
    st.image(uploaded_img, caption="Your uploaded image", use_column_width="always")

    # Image to caption
    with st.spinner("Generating image caption..."):
        img_bytes = uploaded_img.read()
        caption = generate_caption(img_bytes, hf_token)
        st.success("Caption generated!")
        st.markdown(f"**AI-generated Caption:** {caption}")

    # Caption to story
    with st.spinner("Generating story..."):
        story = generate_story(caption, theme, word_limit, hf_token)
        st.success("Story generated!")

    # Display the story in a fixed-width, scrollable box
    st.markdown(
        f"""
        <div style='width: 650px; min-height: 100px; max-height: 600px; background: #f7f7f7; border-radius: 8px; border: 1px solid #ebebeb; margin: 1em 0; padding: 1.5em; overflow-y: auto; overflow-x: hidden; font-family: Georgia,serif; font-size: 1.1em; white-space: pre-wrap; word-wrap: break-word; box-sizing: border-box;'>
        {story}
        </div>
        """,
        unsafe_allow_html=True
    )

elif submit and not uploaded_img:
    st.error("Please upload an image!")
elif submit and not hf_token:
    st.error("Please enter your Hugging Face API token!")

st.markdown("---\nDeveloped with ❤️ using Streamlit and Hugging Face Spaces.")

