from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass(frozen=True)
class DataIngestionConfig:
    raw_data_dir: Path
    ingested_data_dir: Path
    allowed_extensions: List[str]
    max_file_size: int
    resize_shape: tuple

@dataclass(frozen=True)
class ImageCaptioningConfig:
    ingested_data_dir: Path
    captions_dir: Path
    florence2_model_name: str
    max_new_tokens: int
    task_prompt: str
    num_beams: int

@dataclass(frozen=True)
class StoryGenerationConfig:
    captions_dir: Path
    stories_dir: Path
    model_name: str
    together_api_key: str
    max_tokens: int
    temperature: float
    top_p: float
    story_prompt_template: str
    default_theme: str = "adventure"
    default_word_limit: int = 400