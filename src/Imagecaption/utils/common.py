import os
import sys
import yaml
import json
import joblib
import base64
from pathlib import Path
from typing import Any, Optional, Union
from PIL import Image
import logging
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError

logger = logging.getLogger(__name__)

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        logger.error(f"Error reading yaml file {path_to_yaml}: {str(e)}")
        raise e

@ensure_annotations
def create_directories(path_to_directories: list):
    for path in path_to_directories:
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"json file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving json file {path}: {str(e)}")
        raise e

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    try:
        with open(path) as f:
            content = json.load(f)
        logger.info(f"json file loaded successfully from: {path}")
        return ConfigBox(content)
    except Exception as e:
        logger.error(f"Error loading json file {path}: {str(e)}")
        raise e

@ensure_annotations
def save_bin(data: Any, path: Path):
    try:
        joblib.dump(value=data, filename=path)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.error(f"Error saving binary file {path}: {str(e)}")
        raise e

@ensure_annotations
def load_bin(path: Path) -> Any:
    try:
        data = joblib.load(path)
        logger.info(f"Binary file loaded from: {path}")
        return data
    except Exception as e:
        logger.error(f"Error loading binary file {path}: {str(e)}")
        raise e

@ensure_annotations
def get_size(path: Path) -> str:
    try:
        size_in_kb = round(os.path.getsize(path) / 1024)
        return f"~ {size_in_kb} KB"
    except Exception as e:
        logger.error(f"Error getting file size for {path}: {str(e)}")
        return "Size unknown"

@ensure_annotations
def validate_image(image_path: Path) -> bool:
    try:
        with Image.open(image_path) as img:
            img.verify()
        logger.info(f"Image validation successful for: {image_path}")
        return True
    except Exception as e:
        logger.error(f"Image validation failed for {image_path}: {str(e)}")
        return False

@ensure_annotations
def resize_image(image_path: Path, max_size: tuple = (512, 512)) -> Path:
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            resized_path = image_path.parent / f"resized_{image_path.name}"
            img.save(resized_path, "JPEG", quality=85)
        logger.info(f"Image resized and saved at: {resized_path}")
        return resized_path
    except Exception as e:
        logger.error(f"Error resizing image {image_path}: {str(e)}")
        raise e

@ensure_annotations
def encode_image_to_base64(image_path: Path) -> str:
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        logger.info(f"Image encoded to base64: {image_path}")
        return encoded_string
    except Exception as e:
        logger.error(f"Error encoding image to base64 {image_path}: {str(e)}")
        raise e

@ensure_annotations
def clean_filename(filename: str) -> str:
    import re
    cleaned = re.sub(r'[^\w\-_\.]', '_', filename)
    logger.info(f"Filename cleaned: {filename} -> {cleaned}")
    return cleaned

@ensure_annotations
def ensure_dir_exists(directory: Path):
    try:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ensured: {directory}")
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {str(e)}")
        raise e

@ensure_annotations
def delete_file(file_path: Path) -> bool:
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"File deleted: {file_path}")
            return True
        else:
            logger.warning(f"File does not exist: {file_path}")
            return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False

@ensure_annotations
def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()

@ensure_annotations
def is_allowed_file(filename: str, allowed_extensions: list) -> bool:
    extension = get_file_extension(filename)
    allowed = extension.lstrip('.') in [ext.lower().lstrip('.') for ext in allowed_extensions]
    logger.info(f"File extension check for {filename}: {allowed}")
    return allowed

@ensure_annotations
def create_unique_filename(original_filename: str, upload_dir: Path) -> str:
    import time
    import uuid
    cleaned_filename = clean_filename(original_filename)
    name, ext = os.path.splitext(cleaned_filename)
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:8]
    unique_filename = f"{name}_{timestamp}_{unique_id}{ext}"
    counter = 1
    while (upload_dir / unique_filename).exists():
        unique_filename = f"{name}_{timestamp}_{unique_id}_{counter}{ext}"
        counter += 1
    logger.info(f"Unique filename created: {unique_filename}")
    return unique_filename
