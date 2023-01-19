import os
from datetime import datetime

SCHEMA_FILE_PATH = os.path.join("schema_training.json")

REGEX="['cement_strength']+['\_'']+[\d_]+[\d]+\.csv"

PATH = "Training_Raw_files_validated/"

TRAINING_GOOD_RAW_FILES_VALIDATED=os.path.join(PATH, "Good_Raw/")

TRAINING_BAD_RAW_FILES_VALIDATED=os.path.join(PATH, "Bad_Raw/")

TIMESTAMP = datetime.strftime("%m_%d_%Y_%H_%M_%S")

ARCHIVED_DIR = "TrainingArchiveBadData"

ARCHIVED_PATH = os.path.join(ARCHIVED_DIR,"BadData_",TIMESTAMP)


SAMPLE_FILE_NAME='SampleFileName'

LENGTH_OF_DATE_SAMPLE_FILE = 'LengthOfDateStampInFile'

LENGTH_OF_TIME_SAMPLE_FILE='LengthOfTimeStampInFile'

COLUMN_NAME = 'ColName'

NUMBER_OF_COLUMNS = 'NumberofColumns'

TRAINING_BATCH_FILES = "Training_Batch_Files/"

DATABASE_PATH='Training_Database/'






