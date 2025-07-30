from src.Imagecaption import logger
from src.Imagecaption.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from pathlib import Path

STAGE_NAME = "Data Ingestion stage"

if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DataIngestionPipeline()
        file_path = Path("data/raw/image.png")
        pipeline.main(file_path)   # If your main() requires arguments, adapt as needed
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
