import logging
from pathlib import Path
from src.Imagecaption.config.configuration import ConfigurationManager
from src.Imagecaption.components.image_captioning import ImageCaptioning

logger = logging.getLogger(__name__)
STAGE_NAME = "Image Captioning Stage"

class ImageCaptioningPipeline:
    def __init__(self):
        pass

    def main(self, image_path: Path):
        config = ConfigurationManager().get_image_captioning_config()
        image_captioner = ImageCaptioning(config)
        caption = image_captioner.caption_image(image_path)
        logger.info(f"Image caption generated: {caption}")
        return caption

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = ImageCaptioningPipeline()
        path = Path("data/ingested/resized_image.png")  # Input from previous stage
        pipeline.main(path)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
