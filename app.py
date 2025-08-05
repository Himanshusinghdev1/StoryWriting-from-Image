import streamlit as st
from pathlib import Path
from src.Imagecaption.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.Imagecaption.pipeline.image_captioning_pipeline import ImageCaptioningPipeline
from src.Imagecaption.pipeline.story_generation_pipeline import StoryGenerationPipeline

# Ensure upload and output folders exist
for folder in ["data/raw", "data/ingested", "data/captions", "data/stories"]:
    Path(folder).mkdir(parents=True, exist_ok=True)

st.title("🖼️➡️📝 Image to Story Generator Web App")

uploaded_file = st.file_uploader(
    "Upload an image (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])

theme = st.text_input("Story Theme", value="adventure")
word_limit = st.number_input("Word Limit", min_value=100, max_value=1000, value=400, step=50)

if st.button("Generate Story"):
    if uploaded_file is None:
        st.error("Please upload an image file.")
    else:
        # Save file to disk
        upload_path = Path("data/raw") / uploaded_file.name
        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.info(f"Image saved at {upload_path}")

        # 1. Data Ingestion
        with st.spinner("Processing image..."):
            data_pipeline = DataIngestionPipeline()
            ingested_path = data_pipeline.main(upload_path)
        st.image(str(ingested_path), caption="Preprocessed Image", use_column_width=True)

        # 2. Image Captioning
        with st.spinner("Generating caption..."):
            caption_pipeline = ImageCaptioningPipeline()
            caption = caption_pipeline.main(ingested_path)
        st.success("Caption generated!")
        st.markdown(f"**Caption:** {caption}")

        # 3. Story Generation
        caption_file = Path("data/captions") / f"{ingested_path.stem}_caption.txt"
        with st.spinner("Generating story..."):
            story_pipeline = StoryGenerationPipeline()
            story = story_pipeline.main(caption_file, theme, word_limit)
        st.success("Story generated!")

        # Show story in a nice box
        st.markdown(f"**Theme:** {theme}  |  **Word limit:** {word_limit}")
        st.markdown("### Your Story:")
        st.markdown(
            f"<div style='width: 650px; min-height: 100px; max-height: 600px; background: #f7f7f7; border-radius: 8px; border: 1px solid #ebebeb; margin: 1em 0; padding: 1.5em; overflow-y: auto; overflow-x: hidden; font-family: Georgia,serif; font-color: black; font-size: 1.1em; white-space: pre-wrap; word-wrap: break-word; box-sizing: border-box;'>{story}</div>",
            unsafe_allow_html=True
        )

st.markdown("---\nDeveloped with ❤️ using Streamlit")
