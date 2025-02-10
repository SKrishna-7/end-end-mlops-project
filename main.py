from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ =='__main__':
    try:
        
        dataingestion=DataIngestion(DataIngestionConfig(TrainingPipelineConfig()))

        print(dataingestion.initiate_data_ingestion())


    except Exception as e:
        raise NetworkSecurityException(e,sys)
