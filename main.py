from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import ModelTrainerConfig

import sys

if __name__ =='__main__':
    try:
        
        trainingpipelineconfig=TrainingPipelineConfig()
        
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)

        data_trans_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("Initiate the data transformation..")
        data_transformation=DataTransformation(data_validation_artifact,data_trans_config)
        logging.info("data Transformation Completed")
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        # logging.info(data_transformation_artifact)
        print(data_transformation_artifact)

        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        logging.info("Initiate the Model Training..")
        model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifact)
        logging.info("Model Training Completed")
        model_artifacts=model_trainer.initiate_model_trainer()
        print(model_artifacts)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
