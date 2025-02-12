
# End to End MLOPS Project with ETL Pipeline - Building Network Security Project using Phishing Dataset


This project demonstrates an End-to-End MLOps pipeline using a phishing dataset.The pipeline encompasses data ingestion, validation, transformation, model training, evaluation, and deployment, The goal of the project is to build a robust machine learning model to detect phishing websites using a complete MLOps setup, ensuring that it can be maintained, versioned, and deployed in production with ease.

The pipeline integrates tools and frameworks like MLflow, DagsHub, MongoDB, FastAPI, Docker, and GitHub Actions to automate processes like model training, deployment, and continuous integration/continuous deployment (CI/CD). automating everything from data ingestion to model deployment. This project focused on the MLOps lifecycle, leveraging powerful tools of machine learning workflows

# Project Overview

## Folder Structure
![Folder Structure](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/floder.png)

* `constants/`: Holds configuration files used throughout the pipeline.
* `entity/`: Contains definitions for core entities like models and data schemas.
* `logging/`: Custom logging setup for tracking pipeline and model training activities.
* `exception/`: Custom exceptions for handling errors in the pipeline.
* `pipeline/`: Orchestrates the flow of the ML pipeline, from ETL to model training and inference.
* `utils/`: General utility functions used across the project.






# Project Architecture

![Project Flow](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/Projectflow.png)

1. **Data Ingestion** → 2. **Validation** → 3. **Transformation** → 4. **Model Training** → 5. **Deployment with FastAPI** → 6. **Monitoring with MLflow**


* `Data Ingestion`: Load raw phishing data from CSV files and store it in MongoDB for easy access and scalability.
* `Data Validation`: Ensure the data's integrity by checking for missing values, duplicates, or outliers.
* `Data Transformation`: Clean the data and apply feature engineering techniques (e.g., scaling, encoding, or feature extraction).
* `Model Training`: Train machine learning models using different algorithms and tune hyperparameters.
* `Model Evaluation`: Evaluate the trained models based on performance metrics like accuracy, precision, recall, and F1 score.
* `Deployment`: Expose the trained model through a FastAPI application to make predictions on new phishing data.
* `MLOps Automation`: Track experiments and models using MLflow and manage the entire pipeline with DagsHub. Dockerize the application for portability.

## Data Ingestion Architecture

![Data ingestion](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/DataIngestion.png)

## Data Validation Architecture

![Data Validation](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/DataValidation.png)


## Data Transformation Architecture

![Data Transformation](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/Datatransformation.png)


## Model Trainer Architecture

![Model Trainer](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/Modeltrainer.png)

# Hyperparameter Tuning for Model Selection

 During the model development process, I performed hyperparameter tuning to optimize the model's performance. Various hyperparameters were tested across different configurations to find the best performing model.
 
## Models and Hyperparameters
![Model](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/models.png)

## Model Performance Comparison:
Here are the results for different models tested:

* AdaBoost: 92.51%
* Random Forest: 89.08%
* Decision Tree: 86.35%
* Gradient Boosting: 82.43%
* Logistic Regression: 79.43%

## Best Model and Hyperparameter
![Model](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/bestmodel.png)

# Running the Project 

## Flask output
 After successfully setting up and running the project, the Flask API should be up and running. Below is an example of the output you would see when accessing the API.

![FlaskOutput](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/flask.png)

## Mlflow Ui

![FlaskOutput](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/mlflow.png)

## DagsHub

DagsHub is used for tracking experiments and managing model versioning. 

![Dasghub](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/Dagshub.png)


## Metrics over multiple runs

![Metrics](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/combine.png)

## Scores
![Metrics](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/metrics.png)

![Metrics](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/charts.png)

# Prediction Report on Test Data
After training and fine-tuning the model, I evaluated its performance on a separate test dataset. Below is the Prediction Report in the form of an HTML table.

![pred](https://github.com/SKrishna-7/end-end-mlops-project/blob/main/ProjectStructure/pred.png)


# Conclusion
This project has been an exciting journey through the entire Machine Learning lifecycle. From data ingestion and cleaning to model training, evaluation, and deployment, I’ve built a robust end-to-end MLOps pipeline. The key goal of this project was to demonstrate how to structure and automate a complete machine learning workflow, making it ready for production.

By experimenting with multiple models and fine-tuning hyperparameters, I was able to identify the AdaBoost model as the most efficient for this particular task, achieving an accuracy of 92.51%. I then containerized the entire workflow using Docker, integrated continuous integration/continuous deployment (CI/CD) through GitHub Actions, and tracked model experiments using MLflow.

This pipeline not only automates the machine learning lifecycle but also makes it easier to deploy, monitor, and update the models as new data becomes available.


## Authors
[@SureshKrishnan](https://github.com/SKrishna-7)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-green)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)


  
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/suresh-krishnan-s/)



