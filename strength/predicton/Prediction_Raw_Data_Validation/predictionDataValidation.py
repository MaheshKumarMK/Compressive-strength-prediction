import sqlite3
from datetime import datetime
import os
import re
import json
import shutil
import pandas as pd
from strength.logger import App_Logger
from strength.constants.prediction_pipeline import *
from strength.constants.log_files import *

class Prediction_Data_validation:
    """
    This class shall be used for handling all the validation done on the Raw Prediction Data!!.

    """

    def __init__(self,path):

        self.Batch_Directory = path

        self.schema_path = SCHEMA_PREDICTION

        self.logger = App_Logger()



    def valuesFromSchema(self):
        """
        Method Name: valuesFromSchema
        Description: This method extracts all the relevant information from the pre-defined "Schema" file.
        Output: LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, Number of Columns
        On Failure: Raise ValueError,KeyError,Exception

        """
        try:

            with open(self.schema_path, 'r') as f:

                dic = json.load(f)

                f.close()

            pattern = dic['SampleFileName']

            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']

            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']

            column_names = dic['ColName']

            NumberofColumns = dic['NumberofColumns']

            file = open(PREDICTION_SCHEMA_VALIDATION_LOG, 'a+')

            message ="LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + "NumberofColumns:: %s" % NumberofColumns + "\n"

            self.logger.log(file,message)

            file.close()

        except ValueError:

            file = open(PREDICTION_SCHEMA_VALIDATION_LOG, 'a+')

            self.logger.log(file,"ValueError:Value not found inside schema_training.json")

            file.close()

            raise ValueError

        except KeyError:

            file = open(PREDICTION_SCHEMA_VALIDATION_LOG, 'a+')

            self.logger.log(file, "KeyError:Key value error incorrect key passed")

            file.close()

            raise KeyError

        except Exception as e:

            file = open(PREDICTION_SCHEMA_VALIDATION_LOG, 'a+')

            self.logger.log(file, str(e))

            file.close()

            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns


    def manualRegexCreation(self):

        """
        Method Name: manualRegexCreation
        Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                    This Regex is used to validate the filename of the prediction data.
        Output: Regex pattern
        On Failure: None

        """
        regex = "['cement_strength']+['\_'']+[\d_]+[\d]+\.csv"

        return regex

    def createDirectoryForGoodBadRawData(self):

        """
        Method Name: createDirectoryForGoodBadRawData
        Description: This method creates directories to store the Good Data and Bad Data
                        after validating the prediction data.

        Output: None
        On Failure: OSError

        """
        try:

            path = PREDICTION_GOOD_RAW_VALIDATED_DIR

            if not os.path.isdir(path):

                os.makedirs(path, exist_ok=True)

            path = PREDICTION_BAD_RAW_VALIDATED_DIR

            if not os.path.isdir(path):

                os.makedirs(path, exist_ok=True)

        except OSError as ex:

            file = open(PREDICTION_GENERAL_LOG, 'a+')

            self.logger.log(file,"Error while creating Directory %s:" % ex)

            file.close()

            raise OSError

    def deleteExistingGoodDataTrainingFolder(self):
        """
        Method Name: deleteExistingGoodDataTrainingFolder
        Description: This method deletes the directory made to store the Good Data
                        after loading the data in the table. Once the good files are
                        loaded in the DB,deleting the directory ensures space optimization.
        Output: None
        On Failure: OSError
        
        """
        try:

            path = PREDICTION_PATH

            if os.path.isdir(PREDICTION_GOOD_RAW_VALIDATED_DIR):

                shutil.rmtree(PREDICTION_GOOD_RAW_VALIDATED_DIR)

                file = open(PREDICTION_GENERAL_LOG, 'a+')

                self.logger.log(file,"GoodRaw directory deleted successfully!!!")

                file.close()

        except OSError as s:

            file = open(PREDICTION_GENERAL_LOG, 'a+')

            self.logger.log(file,"Error while Deleting Directory : %s" %s)

            file.close()

            raise OSError

    def deleteExistingBadDataTrainingFolder(self):

        """
        Method Name: deleteExistingBadDataTrainingFolder
        Description: This method deletes the directory made to store the bad Data.
        Output: None
        On Failure: OSError

        """

        try:

            path = PREDICTION_PATH

            if os.path.isdir(PREDICTION_BAD_RAW_VALIDATED_DIR):

                shutil.rmtree(PREDICTION_BAD_RAW_VALIDATED_DIR)

                file = open(PREDICTION_GENERAL_LOG, 'a+')

                self.logger.log(file,"BadRaw directory deleted before starting validation!!!")

                file.close()

        except OSError as s:

            file = open(PREDICTION_GENERAL_LOG, 'a+')

            self.logger.log(file,"Error while Deleting Directory : %s" %s)

            file.close()

            raise OSError

    def moveBadFilesToArchiveBad(self):


        """
        Method Name: moveBadFilesToArchiveBad
        Description: This method deletes the directory made  to store the Bad Data
                        after moving the data in an archive folder. We archive the bad
                        files to send them back to the client for invalid data issue.
        Output: None
        On Failure: OSError

        """
        now = datetime.now()

        date = now.date()

        time = now.strftime("%H%M%S")

        try:
            pred_path= PREDICTION_ARCHIVE_BAD

            if not os.path.isdir(pred_path):

                os.makedirs(pred_path)

            source = os.path.join(PREDICTION_PATH,"Bad_Raw")

            dest = os.path.join(PREDICTION_ARCHIVE_BAD,'BadData_' + str(date)+"_"+str(time))

            if not os.path.isdir(dest):

                os.makedirs(dest)

            files = os.listdir(source)

            for f in files:

                if f not in os.listdir(dest):

                    shutil.move(source + "\\" + f, dest)

            file = open(PREDICTION_GENERAL_LOG, 'a+')

            self.logger.log(file,"Bad files moved to archive")

            path = 'Prediction_Raw_Files_Validated/'

            if os.path.isdir(path + 'Bad_Raw/'):

                shutil.rmtree(path + 'Bad_Raw/')

            self.logger.log(file,"Bad Raw Data Folder Deleted successfully!!")

            file.close()

        except OSError as e:

            file = open(PREDICTION_GENERAL_LOG ,'a+')

            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)

            file.close()

            raise OSError




    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
            Method Name: validationFileNameRaw
            Description: This function validates the name of the prediction csv file as per given name in the schema!
                         Regex pattern is used to do the validation.If name format do not match the file is moved
                         to Bad Raw Data folder else in Good raw data.
            Output: None
            On Failure: Exception

        """
        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataTrainingFolder()

        self.deleteExistingGoodDataTrainingFolder()


        onlyfiles = [f for f in os.listdir(self.Batch_Directory)]

        try:
            self.createDirectoryForGoodBadRawData()

            f = open(PREDICTION_NAME_VALIDATION_LOG, 'a+')

            for filename in onlyfiles:

                if (re.match(regex, filename)):

                    splitAtDot = re.split('.csv', filename)

                    splitAtDot = (re.split('_', splitAtDot[0]))

                    if len(splitAtDot[2]) == LengthOfDateStampInFile:

                        if len(splitAtDot[3]) == LengthOfTimeStampInFile:

                            shutil.copy(PREDICTION_BATCH_FILES +"\\" + filename, PREDICTION_GOOD_RAW_VALIDATED_DIR)

                            self.logger.log(f,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy(PREDICTION_BATCH_FILES + "\\" + filename, PREDICTION_BAD_RAW_VALIDATED_DIR)

                            self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

                    else:
                        shutil.copy(PREDICTION_BATCH_FILES + "\\" + filename, PREDICTION_BAD_RAW_VALIDATED_DIR)

                        self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(PREDICTION_BATCH_FILES + "\\" + filename, PREDICTION_BAD_RAW_VALIDATED_DIR)

                    self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            f.close()

        except Exception as e:

            f = open(PREDICTION_NAME_VALIDATION_LOG, 'a+')

            self.logger.log(f, "Error occured while validating FileName %s" % e)

            f.close()

            raise e




    def validateColumnLength(self,NumberofColumns):
        """
        Method Name: validateColumnLength
        Description: This function validates the number of columns in the csv files.
                        It is should be same as given in the schema file.
                        If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                        If the column number matches, file is kept in Good Raw Data for processing.
                    The csv file is missing the first column name, this function changes the missing name to "Wafer".
        Output: None
        On Failure: Exception

        """
        try:

            f = open(PREDICTION_COLUMN_VALIDATION_LOG, 'a+')

            self.logger.log(f,"Column Length Validation Started!!")

            for file in os.listdir(PREDICTION_GOOD_RAW_VALIDATED_DIR):

                csv = pd.read_csv(PREDICTION_GOOD_RAW_VALIDATED_DIR + "\\" + file)

                self.logger.log(f, "Read the CSV file succesfully")

                if csv.shape[1] == NumberofColumns:

                    csv.to_csv(PREDICTION_GOOD_RAW_VALIDATED_DIR + "\\"  + file, index=None, header=True)

                    self.logger.log(f, "Saved the CSV file succesfully")

                else:
            
                    shutil.move(PREDICTION_GOOD_RAW_VALIDATED_DIR + "\\" + file, PREDICTION_BAD_RAW_VALIDATED_DIR,)

                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)

            self.logger.log(f, "Column Length Validation Completed!!")

        # except OSError:

        #     f = open(PREDICTION_COLUMN_VALIDATION_LOG, 'a+')

        #     self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)

        #     f.close()

        #     raise OSError

        except Exception as e:

            f = open(PREDICTION_COLUMN_VALIDATION_LOG, 'a+')

            self.logger.log(f, "Error Occured:: %s" % e)

            f.close()

            raise e

        f.close()

    def deletePredictionFile(self):

        if os.path.exists(PREDICTION_OUTPUT_FILE):

            os.remove(PREDICTION_OUTPUT_FILE)

    def validateMissingValuesInWholeColumn(self):
        """
        Method Name: validateMissingValuesInWholeColumn
        Description: This function validates if any column in the csv file has all values missing.
                    If all the values are missing, the file is not suitable for processing.
                    SUch files are moved to bad raw data.
        Output: None
        On Failure: Exception

        """
        try:
            f = open(PREDICTION_MISSING_VALUE, 'a+')

            self.logger.log(f, "Missing Values Validation Started!!")

            for file in os.listdir(PREDICTION_GOOD_RAW_VALIDATED_DIR):

                csv = pd.read_csv(PREDICTION_GOOD_RAW_VALIDATED_DIR + "\\" + file)

                count = 0

                for columns in csv:

                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):

                        count+=1

                        shutil.move(PREDICTION_GOOD_RAW_VALIDATED_DIR + "\\" + file,
                                    PREDICTION_BAD_RAW_VALIDATED_DIR)
                        
                        self.logger.log(f,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)

                        break

                if count==0:

                    # csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(PREDICTION_GOOD_RAW_VALIDATED_DIR + "\\" + file, index=None, header=True)

        except OSError:

            f = open(PREDICTION_MISSING_VALUE, 'a+')

            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)

            f.close()

            raise OSError
        
        except Exception as e:

            f = open(PREDICTION_MISSING_VALUE, 'a+')

            self.logger.log(f, "Error Occured:: %s" % e)

            f.close()

            raise e
        
        f.close()













