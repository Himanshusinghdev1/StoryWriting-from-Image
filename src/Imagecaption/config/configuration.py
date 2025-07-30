import os
from pathlib import Path
from src.Imagecaption.utils.common import read_yaml
from src.Imagecaption.entity.config_entity import DataIngestionConfig

class ConfigurationManager:
    def __init__(self, config_path: str = "config/config.yaml", params_path: str = "params.yaml"):
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
