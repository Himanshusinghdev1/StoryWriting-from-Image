from pathlib import Path
import shutil
from src.Imagecaption.entity.config_entity import DataIngestionConfig
from src.Imagecaption.utils.common import (
    create_directories,
    is_allowed_file,
    validate_image,
    resize_image
)
import os

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        create_directories([config.raw_data_dir, config.ingested_data_dir])

    def ingest(self, file_path: Path) -> Path:
        # Check extension
        if not is_allowed_file(file_path.name, self.config.allowed_extensions):
            raise ValueError(f"File type not supported: {file_path.suffix}")

        # File size check
        if file_path.stat().st_size > self.config.max_file_size:
            raise ValueError(f"File size exceeds limit: {file_path.stat().st_size}")

        # Validate image
        if not validate_image(file_path):
            raise ValueError("Uploaded file is not a valid image.")

        # Resize and save to ingested_data_dir
        resized_path = resize_image(file_path, self.config.resize_shape)
        final_path = self.config.ingested_data_dir / resized_path.name
        resized_path.rename(final_path)
        return final_path
