import os
from pathlib import Path
from dotenv import load_dotenv
from src.Imagecaption.utils.common import read_yaml
from src.Imagecaption.entity.config_entity import (DataIngestionConfig,ImageCaptioningConfig,StoryGenerationConfig)

class ConfigurationManager:
    def __init__(self, config_path: str = "config/config.yaml", params_path: str = "params.yaml"):
        load_dotenv()
        self.config = read_yaml(Path(config_path))
        self.params = read_yaml(Path(params_path))

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        params = self.params.data_ingestion
        return DataIngestionConfig(
            raw_data_dir=Path(config.raw_data_dir),
            ingested_data_dir=Path(config.ingested_data_dir),
            allowed_extensions=config.allowed_extensions,
            max_file_size=config.max_file_size,
            resize_shape=tuple(params.resize_shape)
        )

    def get_image_captioning_config(self) -> ImageCaptioningConfig:
        config = self.config.image_captioning
        params = self.params.image_captioning
        return ImageCaptioningConfig(
            ingested_data_dir=Path(config.ingested_data_dir),
            captions_dir=Path(config.captions_dir),
            florence2_model_name=config.florence2_model_name,
            max_new_tokens=params.max_new_tokens,
            task_prompt=params.task_prompt,
            num_beams=params.num_beams
        )

    def get_story_generation_config(self) -> StoryGenerationConfig:
        config = self.config.story_generation
        params = self.params.story_generation
        api_key = os.getenv("TOGETHER_API_KEY", config.together_api_key)
        if api_key.startswith("${") and api_key.endswith("}"):
            api_key = os.getenv(api_key[2:-1], "")
        return StoryGenerationConfig(
            captions_dir=Path(config.captions_dir),
            stories_dir=Path(config.stories_dir),
            model_name=config.model_name,
            together_api_key=api_key,
            max_tokens=params.max_tokens,
            temperature=params.temperature,
            top_p=params.top_p,
            story_prompt_template=params.story_prompt_template
        )