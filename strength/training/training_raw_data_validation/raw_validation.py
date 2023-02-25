from datetime import datetime
import os
import sys
import re
import json
import shutil
import pandas as pd

from strength.exception import StrengthException
from strength.logger import App_Logger
from strength.constants.training_pipeline import *
from strength.constants.log_files import *


class RawDataValidation:
    """
    This class shall be used for handling all the validation done on the Raw Training Data!!.

    """
    def __init__(self,path):

        self.Batch_Directory = path

        self.logger = App_Logger()

        self.schema_path = SCHEMA_FILE_PATH
    

    def manual_regex_creation(self,):
        try:
            """
            Method Name: manualRegexCreation
            Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                        This Regex is used to validate the filename of the training data.
            Output: Regex pattern
            On Failure: None

            """
            regex = REGEX

            return regex

        except Exception as e:
            raise StrengthException(e,sys)

    def GoodBadRawDataDirectory(self):

        """
        Method Name: GoodBadRawDataDirectory
        Description: This method creates directories to store the Good Data and Bad Data
                        after validating the training data.

        Output: None
        On Failure: OSError

        """
        try:
            good_path = TRAINING_GOOD_RAW_FILES_VALIDATED

            if not os.path.isdir(good_path):

                os.makedirs(good_path, exist_ok=True)

            bad_path = TRAINING_BAD_RAW_FILES_VALIDATED

            if not os.path.isdir(bad_path):

                os.makedirs(bad_path, exist_ok=True)

        except OSError as ex:

            file = open(GENERAL_LOG,"a+")

            self.logger(file, f"Error while creating directory {ex}")

            file.close()
            raise OSError

    def deleteExistingGoodDataFolder(self):

        """
        Method Name: deleteExistingGoodDataFolder

        Description: This method deletes the directory made  to store the Good Data
                        after loading the data in the table. Once the good files are
                        loaded in the DB,deleting the directory ensures space optimization.
        Output: None
        On Failure: OSError

        """
        try:

            if os.path.isdir(TRAINING_GOOD_RAW_FILES_VALIDATED):

                shutil.rmtree(TRAINING_GOOD_RAW_FILES_VALIDATED)

                file = open(GENERAL_LOG,"a+")

                self.logger.log(file,"GoodRaw directory deleted successfully!!!")

                file.close()

        except OSError as ex:

            file = open(GENERAL_LOG,"a+")

            self.logger(file, f"Error while creating directory {ex}")

            file.close()

            raise OSError

    def deleteExistingBadDataFolder(self):

        """
        Method Name: deleteExistingBadDataFolder

        Description: This method deletes the directory made  to store the BAD Data
                        after loading the data in the table. Once the good files are
                        loaded in the DB,deleting the directory ensures space optimization.
        Output: None
        On Failure: OSError

        """

        try:
        
            if os.path.isdir(TRAINING_BAD_RAW_FILES_VALIDATED):

                shutil.rmtree(TRAINING_BAD_RAW_FILES_VALIDATED)

                file = open(GENERAL_LOG,"a+")

                self.logger.log(file,"BAD Raw directory deleted successfully!!!")

                file.close()

        except OSError as ex:

            file = open(GENERAL_LOG,"a+")

            self.logger(file, f"Error while creating directory {ex}")

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

        try:    
            source = TRAINING_BAD_RAW_FILES_VALIDATED
        
            if os.path.isdir(source):

                arch_path = ARCHIVED_DIR

                os.makedirs(arch_path, exist_ok=True)

                dest = ARCHIVED_PATH

                os.makedirs(dest, exist_ok=True)

                files = os.listdir(source)

                for f in files:

                    if f not in os.listdir(dest):

                        shutil.move(source +"\\" + f, dest)

                file = open(GENERAL_LOG,"a+")

                self.logger.log(file,"Bad files moved to archive")

                if os.path.isdir(TRAINING_BAD_RAW_FILES_VALIDATED):
                
                    shutil.rmtree(TRAINING_BAD_RAW_FILES_VALIDATED)

                self.logger.log(file,"Bad Raw Data Folder Deleted successfully!!")

                file.close()

        except Exception as e:

            file = open(GENERAL_LOG,"a+")

            self.logger.log(file, "Error while moving bad files to archive:: %s" % e)

            file.close()

            raise StrengthException(e,sys)

    def validationFileNameRaw(self,regex,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
        Method Name: validationFileNameRaw
        Description: This function validates the name of the training csv files as per given name in the schema!
                        Regex pattern is used to do the validation.If name format do not match the file is moved
                        to Bad Raw Data folder else in Good raw data.
        Output: None
        On Failure: Exception

        """

        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.deleteExistingBadDataFolder()

        self.deleteExistingGoodDataFolder()

        onlyfiles = [files for files in os.listdir(self.Batch_Directory)]
        try:
            # create new directories
            self.GoodBadRawDataDirectory()

            f = open(NAME_VALIDATION_LOG,"a+")

            for filename in onlyfiles:

                if (re.match(regex, filename)):

                    splitAtDot = re.split('.csv', filename)

                    splitAtDot = (re.split('_', splitAtDot[0]))

                    if len(splitAtDot[2]) == LengthOfDateStampInFile:

                        if len(splitAtDot[3]) == LengthOfTimeStampInFile:
                            
                            shutil.copy(TRAINING_BATCH_FILES + filename, TRAINING_GOOD_RAW_FILES_VALIDATED)
                            self.logger.log(f,"Valid File name!! File moved to GoodRaw Folder :: %s" % filename)

                        else:
                            shutil.copy(TRAINING_BATCH_FILES + filename, TRAINING_BAD_RAW_FILES_VALIDATED)
                            self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                    else:
                        shutil.copy(TRAINING_BATCH_FILES + filename, TRAINING_BAD_RAW_FILES_VALIDATED)
                        self.logger.log(f,"Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)
                else:
                    shutil.copy(TRAINING_BATCH_FILES + filename, TRAINING_BAD_RAW_FILES_VALIDATED)
                    self.logger.log(f, "Invalid File Name!! File moved to Bad Raw Folder :: %s" % filename)

            f.close()

        except Exception as e:
            
            raise StrengthException(e,sys)


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
            f = open(COLUMN_VALIDATION_LOG,"a+")

            self.logger.log(f,"Column Length Validation Started!!")

            for file in os.listdir(TRAINING_GOOD_RAW_FILES_VALIDATED):

                csv = pd.read_csv(TRAINING_GOOD_RAW_FILES_VALIDATED + "\\" + file)

                self.logger.log(f, "Read the csv file :: %s" % file)

                if csv.shape[1] == NumberofColumns:
                    pass
                
                else:
                    shutil.move(TRAINING_GOOD_RAW_FILES_VALIDATED + "\\" + file, TRAINING_BAD_RAW_FILES_VALIDATED)

                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)

            self.logger.log(f, "Column Length Validation Completed!!")

        except OSError:

            f = open(COLUMN_VALIDATION_LOG,"a+")

            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)

            f.close()

            raise OSError

        except Exception as e:
            raise StrengthException(e,sys)

        f.close()

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
            f = open(MISSING_VALUES_LOG,"a+")

            self.logger.log(f,"Missing Values Validation Started!!")

            for file in os.listdir(TRAINING_GOOD_RAW_FILES_VALIDATED):

                csv = pd.read_csv(TRAINING_GOOD_RAW_FILES_VALIDATED +"\\"+ file)

                count = 0

                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count+=1
                        shutil.move(TRAINING_GOOD_RAW_FILES_VALIDATED + "\\" + file,
                                    TRAINING_BAD_RAW_FILES_VALIDATED)

                        self.logger.log(f,"Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
                        break

                if count==0:

                    csv.to_csv(TRAINING_GOOD_RAW_FILES_VALIDATED + "\\" + file, index=None, header=True)

                    self.logger.log(f, f"There is no missing values in the column")

        except OSError:

            f = open(MISSING_VALUES_LOG,"a+")

            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)

            f.close()

            raise OSError

        except Exception as e:
            raise StrengthException(e,sys)

        f.close()

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

            pattern = dic[SAMPLE_FILE_NAME]

            LengthOfDateStampInFile = dic[LENGTH_OF_DATE_SAMPLE_FILE]

            LengthOfTimeStampInFile = dic[LENGTH_OF_TIME_SAMPLE_FILE]

            column_names = dic[COLUMN_NAME]

            NumberofColumns = dic[NUMBER_OF_COLUMNS]

            file = open(SCHEMA_VALIDATION_LOG,"a+")

            message = "LengthOfDateStampInFile:: %s" %LengthOfDateStampInFile + "\t" + \
                      "LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile +"\t " + \
                      "NumberofColumns:: %s" % NumberofColumns + "\n"

            self.logger.log(file,message)

            file.close()


        except Exception as e:

            file = open(SCHEMA_VALIDATION_LOG,"a+")

            self.logger.log(file, str(e))

            file.close()

            raise StrengthException(e, sys)

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberofColumns