from src.Imagecaption import logger
from src.Imagecaption.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.Imagecaption.pipeline.image_captioning_pipeline import ImageCaptioningPipeline
from pathlib import Path

STAGE_NAME_INGESTION = "Data Ingestion stage"
STAGE_NAME_CAPTIONING = "Image Captioning stage"

if __name__ == '__main__':
    try:
        # Ingestion
        logger.info(f">>>>>> stage {STAGE_NAME_INGESTION} started <<<<<<")
        pipeline = DataIngestionPipeline()
        file_path = Path("data/raw/image.png")
        ingested_path = pipeline.main(file_path)
        logger.info(f">>>>>> stage {STAGE_NAME_INGESTION} completed <<<<<<\n\nx==========x")
        # Captioning
        logger.info(f">>>>>> stage {STAGE_NAME_CAPTIONING} started <<<<<<")
        caption_pipeline = ImageCaptioningPipeline()
        caption = caption_pipeline.main(ingested_path)
        logger.info(f"Caption: {caption}")
        logger.info(f">>>>>> stage {STAGE_NAME_CAPTIONING} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
