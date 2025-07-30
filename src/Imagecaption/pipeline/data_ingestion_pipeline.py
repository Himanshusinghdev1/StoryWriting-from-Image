import logging
from pathlib import Path

from src.Imagecaption.config.configuration import ConfigurationManager
from src.Imagecaption.components.data_ingestion import DataIngestion

logger = logging.getLogger(__name__)
STAGE_NAME = "Data Ingestion stage"


class DataIngestionPipeline:
    def __init__(self):
        pass

    def main(self, file_path: Path):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        ingested_path = data_ingestion.ingest(file_path)
        logger.info(f"Ingested and preprocessed image saved at: {ingested_path}")
        return ingested_path


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python data_ingestion_pipeline.py <image_file_path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        pipeline = DataIngestionPipeline()
        pipeline.main(file_path)
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e
