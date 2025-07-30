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
