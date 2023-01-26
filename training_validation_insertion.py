from datetime import datetime
import sys
import os

from strength.logger import App_Logger
from strength.exception import StrengthException
from strength.training.training_raw_data_validation.raw_validation import RawDataValidation
from strength.constants.log_files import *
from strength.training.training_DB_operations.DB_operations import dBOperation

class TrainValidation:

    def __init__(self, path) -> None:

        self.log_writer = App_Logger()

        self.file_object = open(MAIN_TRAINING_LOG, "a+")

        self.raw_data = RawDataValidation(path)

        self.db_operations = dBOperation()

    def train_validation(self):

        try:
            self.log_writer.log(self.file_object, 'Start validation of training files and data')

            # extracting values from prediction schema
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, noofcolumns = self.raw_data.valuesFromSchema()

            # getting the regex defined to validate filename
            regex = self.raw_data.manual_regex_creation()

            # validating filename of prediction files
            self.raw_data.validationFileNameRaw(regex, LengthOfDateStampInFile, LengthOfTimeStampInFile)

            # validating column length in the file
            self.raw_data.validateColumnLength(noofcolumns)

            # validating if any column has all values missing
            self.raw_data.validateMissingValuesInWholeColumn()

            self.log_writer.log(self.file_object, "Raw Data Validation Complete!!")

            self.log_writer.log(self.file_object,
                                "Creating Training_Database and tables on the basis of given schema!!!")
            
            # create database with given name, if present open the connection! Create table with columns given in schema
            self.db_operations.createTableDb ('Training', column_names)

            self.log_writer.log(self.file_object, "Table creation Completed!!")

            self.log_writer.log(self.file_object, "Insertion of Data into Table started!!!!")

            # insert csv files in the table
            self.db_operations.insertIntoTableGoodData('Training')

            self.log_writer.log(self.file_object, "Insertion in Table completed!!!")

            self.log_writer.log(self.file_object, "Deleting Good Data Folder!!!")
            
            # Delete the good data folder after loading files in table
            self.raw_data.deleteExistingGoodDataFolder()

            self.log_writer.log(self.file_object, "Good_Data folder deleted!!!")

            self.log_writer.log(self.file_object, "Moving bad files to Archive and deleting Bad_Data folder!!!")

            # Move the bad files to archive folder
            self.raw_data.moveBadFilesToArchiveBad()

            self.log_writer.log(self.file_object, "Bad files moved to archive!! Bad folder Deleted!!")

            self.log_writer.log(self.file_object, "Validation Operation completed!!")

            self.log_writer.log(self.file_object, "Extracting csv file from table")

            # export data in table to csvfile
            self.db_operations.selectingDatafromtableintocsv('Training')

            self.file_object.close()
            
        except Exception as e:
            raise StrengthException(e,sys)
    
    
    