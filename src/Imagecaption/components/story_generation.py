import logging
from pathlib import Path
import os
import streamlit as st
from together import Together

logger = logging.getLogger(__name__)

class StoryGeneration:
    def __init__(self, config):
        self.config = config
        
        # Robust API key retrieval (Streamlit secrets + local env fallback)
        try:
            api_key = st.secrets["TOGETHER_API_KEY"]
        except Exception:
            api_key = os.getenv("TOGETHER_API_KEY", getattr(config, "together_api_key", ""))
            
        self.client = Together(api_key=api_key)

    def generate_story(self, caption_file_path, theme=None, word_limit=None) -> str:
        # Check if the first argument is a path or a caption string
        if isinstance(caption_file_path, (str, Path)) and os.path.exists(caption_file_path):
            with open(caption_file_path, 'r', encoding='utf-8') as f:
                caption = f.read().strip()
            save_to_disk = True
        else:
            caption = str(caption_file_path).strip()
            save_to_disk = False

        logger.info("Generating story from caption")

        prompt = f"""You are a creative storyteller. Based on the following image description, write an engaging short story.

Image Description: {caption}

Instructions:
- Write a complete short story of 3-4 paragraphs
- Include a clear beginning, middle, and end
- Use vivid, descriptive language
- Give the main character a name and personality
- End with a meaningful or surprising conclusion

Story:"""

        response = self.client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=1024,
            temperature=0.8,
        )

        story = response.choices[0].message.content.strip()
        
        if save_to_disk and hasattr(self.config, "stories_dir"):
            # Ensure folder exists
            self.config.stories_dir.mkdir(parents=True, exist_ok=True)
            story_path = self.config.stories_dir / f"{Path(caption_file_path).stem.replace('_caption', '')}_story.txt"
            with open(story_path, "w", encoding="utf-8") as f:
                f.write(story)
            logger.info(f"Story saved at: {story_path}")

        logger.info("Story generated successfully")
        return story
