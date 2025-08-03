from pathlib import Path
import logging
from together import Together
from src.Imagecaption.entity.config_entity import StoryGenerationConfig
from src.Imagecaption.utils.common import create_directories

logger = logging.getLogger(__name__)

class StoryGeneration:
    def __init__(self, config: StoryGenerationConfig):
        self.config = config
        create_directories([self.config.stories_dir])
        self.client = Together(api_key=self.config.together_api_key)

    def generate_story(self, caption_file_path: Path, theme: str = None, word_limit: int = None) -> str:
        with open(caption_file_path, 'r', encoding='utf-8') as f:
            caption = f.read().strip()

        # Use user input or default
        theme = theme or self.config.default_theme
        word_limit = word_limit or self.config.default_word_limit

        prompt = self.config.story_prompt_template.format(caption=caption, theme=theme, word_limit=word_limit)
        logger.info(f"Calling Together.ai with Llama-3.3-70B-Instruct-Turbo-Free...")

        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
        )
        story = response.choices[0].message.content.strip()

        story_path = self.config.stories_dir / f"{caption_file_path.stem.replace('_caption', '')}_story.txt"
        with open(story_path, "w", encoding="utf-8") as f:
            f.write(story)
        logger.info(f"Story saved at: {story_path}")
        return story
