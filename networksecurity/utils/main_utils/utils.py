import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import dill
import pickle

from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import pandas as pd

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    

def save_numpy_array_data(file_path: str,array: np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as obj:
            np.save(obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
        
    

def save_obj(file_path: str,obj: object)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e
        

def load_obj(file_path: str,)->object:
    try:
        logging.info(f"Attempting to load file from: {os.path.abspath(file_path)}")

        if not os.path.exists(file_path):
            raise Exception(f"The file {file_path} is not exists..!")
        
        with open(file_path,'rb') as file_obj:
            loaded_obj=pickle.load(file_obj)
            logging.info(f"Loaded object type: {type(loaded_obj)}")            
            return loaded_obj
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e



def load_numpy_arr(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException(e,sys) from e




def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model
            logging.info("The Params : ",gs.best_params_)
            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)
            results=[]
            results.append({
        'Model': model,
        'Best Parameters': gs.best_params_,
        'Best Score': gs.best_score_,
        'Best Estimator': gs.best_estimator_
    })
            results_df = pd.DataFrame(results)
            results_df.to_csv('best_model_result/best_model_results.csv', index=False)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
