import os

GENERAL_LOG=open(os.path.join("training_artifact", "Training_Logs/GeneralLog.txt","a+"))

COLUMN_VALIDATION_LOG = open(os.path.join("training_artifact","Training_Logs/columnValidationLog.txt", 'a+'))

MISSING_VALUES_LOG = open(os.path.join("training_artifact","Training_Logs/missingValuesInColumn.txt", 'a+'))

SCHEMA_VALIDATION_LOG = open(os.path.join("training_artifact","Training_Logs/valuesfromSchemaValidationLog.txt", 'a+'))

MAIN_TRAINING_LOG = open(os.path.join("training_artifact", "Training_Logs/Training_Main_Log.txt"),"a+")

NAME_VALIDATION_LOG = open(os.path.join("training_artifact","Training_Logs/nameValidationLog.txt", 'a+'))

DATABASE_CONN_LOG = open(os.path.join("training_artifact", "Training_Logs/DataBaseConnectionLog.txt", 'a+'))

DB_TABLE_LOG = open(os.path.join("training_artifact","Training_Logs/DbTableCreateLog.txt", 'a+'))

DB_INSERT_LOG = open(os.path.join("training_artifact","Training_Logs/DbInsertLog.txt", 'a+'))

MODEL_TRAINING_LOG = open(os.path.join("training_artifact","Training_Logs/ModelTrainingLog.txt", 'a+'))


