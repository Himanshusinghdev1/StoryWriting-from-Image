import logging
from pathlib import Path
from src.Imagecaption.config.configuration import ConfigurationManager
from src.Imagecaption.components.story_generation import StoryGeneration

logger = logging.getLogger(__name__)
STAGE_NAME = "Story Generation Stage"

class StoryGenerationPipeline:
    def __init__(self): pass

    def main(self, caption_file_path: Path):
        config = ConfigurationManager().get_story_generation_config()
        story_generator = StoryGeneration(config)
        story = story_generator.generate_story(caption_file_path)
        logger.info(f"Story generated (length: {len(story)} characters)")
        return story

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = StoryGenerationPipeline()
        cap_path = Path("data/captions/resized_image_caption.txt")
        pipeline.main(cap_path)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
