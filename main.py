from src.Imagecaption import logger
from src.Imagecaption.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.Imagecaption.pipeline.image_captioning_pipeline import ImageCaptioningPipeline
from src.Imagecaption.pipeline.story_generation_pipeline import StoryGenerationPipeline
from pathlib import Path

STAGE_NAME_INGESTION = "Data Ingestion stage"
STAGE_NAME_CAPTIONING = "Image Captioning stage"
STAGE_NAME_STORY = "Story Generation stage"

if __name__ == '__main__':
    try:
        # Stage 1: Data Ingestion
        logger.info(f">>>>>> stage {STAGE_NAME_INGESTION} started <<<<<<")
        ingestion_pipeline = DataIngestionPipeline()
        file_path = Path("data/raw/image.png")
        ingested_path = ingestion_pipeline.main(file_path)
        logger.info(f">>>>>> stage {STAGE_NAME_INGESTION} completed <<<<<<\n\nx==========x")

        # Stage 2: Image Captioning
        logger.info(f">>>>>> stage {STAGE_NAME_CAPTIONING} started <<<<<<")
        captioning_pipeline = ImageCaptioningPipeline()
        caption = captioning_pipeline.main(ingested_path)
        logger.info(f"Generated Caption: {caption}")
        logger.info(f">>>>>> stage {STAGE_NAME_CAPTIONING} completed <<<<<<\n\nx==========x")

        # Stage 3: Story Generation
        logger.info(f">>>>>> stage {STAGE_NAME_STORY} started <<<<<<")
        theme = input("Enter desired story theme (e.g., adventure, fantasy, mystery): ")
        word_limit = int(input("Enter story word limit (e.g., 150, 300, 500): "))
        story_pipeline = StoryGenerationPipeline()
        caption_file = Path("data/captions") / f"{ingested_path.stem}_caption.txt"
        story = story_pipeline.main(caption_file, theme, word_limit)
        logger.info(f"Generated Story Preview: {story[:200]}...")
        logger.info(f">>>>>> stage {STAGE_NAME_STORY} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e
