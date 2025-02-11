import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifacts_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.logging.logger import logging

from networksecurity.utils.main_utils.utils import save_numpy_array_data , save_obj


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact

            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def data_trans_obj(cls)->Pipeline:
        logging.info("Entered data_transformer_obj method..!")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor:Pipeline=Pipeline([
                (
                    "imputer",imputer
                )
            ])

            logging.info('Preprocessor returned..')
            return processor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered initiate data transformation...")

        try:
            
            logging.info("Starting Data Transformation..")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor=self.data_trans_obj()
            preprocessor_obj=preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_obj.transform(input_feature_test_df)


            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            
            save_obj( self.data_transformation_config.transformed_object_file_path, preprocessor_obj,)
            # save_obj( "final_model/preprocessor.pkl", preprocessor_obj)

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact



        except Exception as e:
            raise NetworkSecurityException(e,sys)