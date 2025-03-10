import os
import sys

from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging

from networksecurity.entity.artifacts_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig



from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_obj,load_obj
from networksecurity.utils.main_utils.utils import load_numpy_arr,evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metrics import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
import mlflow
from urllib.parse import urlparse

import dagshub
dagshub.init(repo_owner='SKrishna-7', repo_name='NetworkSecurity', mlflow=True)


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,model,metrics):
        with mlflow.start_run():
            f1_score=metrics.f1_score
            precision_score=metrics.precision_score
            recall_score=metrics.recall_score

            mlflow.log_metric("f1 score",f1_score)
            mlflow.log_metric("precision score",precision_score)
            mlflow.log_metric("recall score",recall_score)


            mlflow.sklearn.log_model(model,"model")

    def train_model(self,xtrain,ytrain,xtest,ytest):
        models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
        params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                'criterion':['gini', 'entropy', 'log_loss'],
                'criterion':['gini', 'entropy'],
                
                'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                'criterion':['squared_error', 'friedman_mse'],
                'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

        model_report:dict=evaluate_models(X_train=xtrain,y_train=ytrain,X_test=xtest,y_test=ytest,models=models,param=params)
        
        logging.info(model_report)

        best_model_score=max(sorted(model_report.values()))
        best_model=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        model=models[best_model]
        ytrain_pred=model.predict(xtrain)
        classification_train_metric=get_classification_score(y_true=ytrain,y_pred=ytrain_pred)
        self.track_mlflow(model,classification_train_metric)

        ##To track the Mlflow
        ytest_pred=model.predict(xtest)
        classification_test_metric=get_classification_score(y_true=ytest,y_pred=ytest_pred)
        self.track_mlflow(model,classification_test_metric)
        
        # preprocessor = load_obj(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        # Network_Model=NetworkModel(preprocessor=preprocessor,model=model)
        save_obj(self.model_trainer_config.trained_model_file_path,obj=NetworkModel)
        #model pusher
        save_obj("final_model/model.pkl",model)
        
        
        ## Model Trainer Artifact
        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_arr(train_file_path)
            test_arr = load_numpy_arr(test_file_path)

            xtrain, ytrain, xtest, ytest = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(xtrain,ytrain,xtest,ytest)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)