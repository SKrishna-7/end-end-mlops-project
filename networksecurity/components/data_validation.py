from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifacts_entity import DataValidationArtifact
from networksecurity.entity.artifacts_entity import DataIngestionArtifact
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file)->pd.DataFrame:
        try:
            return pd.read_csv(file)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            no_columns=len(self._schema_config)
            logging.info(f"Required number of columns : {no_columns}")
            logging.info(f"Dataframe has  {len(dataframe.columns)} columns")

            if len(dataframe.columns)==no_columns:
                return True
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def detect_datadrift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]

                is_sam_dist=ks_2samp(d1,d2)

                if threshold<=is_sam_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({
                    col:{
                        "p_value":float(is_sam_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:

        try:
            train_filepath=self.data_ingestion_artifact.trained_file_path
            test_filepath=self.data_ingestion_artifact.test_file_path

            train_df=DataValidation.read_data(train_filepath)
            test_df=DataValidation.read_data(test_filepath)

            status=self.validate_columns(dataframe=train_df)
            if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
            status = self.validate_columns(dataframe=test_df)
            if not status:
                error_message=f"Test dataframe does not contain all columns.\n"   
            
            #Data drift
            status=self.detect_datadrift(base_df=train_df,current_df=test_df)

            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        