import shutil
import sqlite3
from os import listdir
import os
import csv
from strength.logger import App_Logger
from strength.constants.prediction_pipeline import *
from strength.constants.log_files import *


class dBOperation:
    """
    This class shall be used for handling all the SQL operations.

    """

    def __init__(self):
        self.path = DATABASE
        self.badFilePath = PREDICTION_BAD_RAW_VALIDATED_DIR
        self.goodFilePath = PREDICTION_GOOD_RAW_VALIDATED_DIR
        self.logger = App_Logger()


    def dataBaseConnection(self,DatabaseName):

        """
        Method Name: dataBaseConnection
        Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
        Output: Connection to the DB

        """
        try:
            conn = sqlite3.connect(self.path+DatabaseName+'.db')

            file = open(PREDICTION_DATABASE_CONN_LOG, 'a+')
            self.logger.log(file, "Opened %s database successfully" % DatabaseName)
            file.close()
        except ConnectionError:
            file = open(PREDICTION_DATABASE_CONN_LOG, 'a+')
            self.logger.log(file, "Error while connecting to database: %s" %ConnectionError)
            file.close()
            raise ConnectionError
        return conn

    def createTableDb(self,DatabaseName,column_names):

        """
        Method Name: createTableDb
        Description: This method creates a table in the given database which will be used to insert the Good data after raw data validation.
        Output: None
        On Failure: Raise Exception

        """
        try:
            conn = self.dataBaseConnection(DatabaseName)
            conn.execute('DROP TABLE IF EXISTS Good_Raw_Data;')

            for key in column_names.keys():
                type = column_names[key]

                # we will remove the column of string datatype before loading as it is not needed for training
                #in try block we check if the table exists, if yes then add columns to the table
                # else in catch block we create the table
                try:
                    #cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                    conn.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                except:
                    conn.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

            conn.close()

            file = open(PREDICTION_DB_TABLE_CREATION_LOG, 'a+')
            self.logger.log(file, "Tables created successfully!!")
            file.close()

            file = open(PREDICTION_DATABASE_CONN_LOG, 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()

        except Exception as e:
            file = open(PREDICTION_DB_TABLE_CREATION_LOG, 'a+')
            self.logger.log(file, "Error while creating table: %s " % e)
            file.close()
            conn.close()
            file = open(PREDICTION_DATABASE_CONN_LOG, 'a+')
            self.logger.log(file, "Closed %s database successfully" % DatabaseName)
            file.close()
            raise e


    def insertIntoTableGoodData(self,Database):

        """
        Method Name: insertIntoTableGoodData
        Description: This method inserts the Good data files from the Good_Raw folder into the
                    above created table.
        Output: None
        On Failure: Raise Exception

        """

        conn = self.dataBaseConnection(Database)
        goodFilePath= self.goodFilePath
        badFilePath = self.badFilePath
        onlyfiles = [f for f in listdir(goodFilePath)]
        log_file = open(PREDICTION_DB_INSERT_LOG, 'a+')

        for file in onlyfiles:
            try:

                with open(goodFilePath+'/'+file, "r") as f:
                    next(f)
                    reader = csv.reader(f, delimiter="\n")
                    for line in enumerate(reader):
                        for list_ in (line[1]):
                            try:
                                conn.execute('INSERT INTO Good_Raw_Data values ({values})'.format(values=(list_)))
                                self.logger.log(log_file," %s: File loaded successfully!!" % file)
                                conn.commit()
                            except Exception as e:
                                raise e

            except Exception as e:

                conn.rollback()
                self.logger.log(log_file,"Error while creating table: %s " % e)
                shutil.move(goodFilePath+'/' + file, badFilePath)
                self.logger.log(log_file, "File Moved Successfully %s" % file)
                log_file.close()
                conn.close()
                raise e

        conn.close()
        log_file.close()


    def selectingDatafromtableintocsv(self,Database):

        """
        Method Name: selectingDatafromtableintocsv
        Description: This method exports the data in GoodData table as a CSV file. in a given location.
                    above created .
        Output: None
        On Failure: Raise Exception

        """

        self.fileFromDb = PREDICTION_FILE_DB
        self.fileName = 'InputFile.csv'
        log_file = open(PREDICTION_LOGS_EXPORT_CSV, 'a+')
        try:
            conn = self.dataBaseConnection(Database)
            sqlSelect = "SELECT *  FROM Good_Raw_Data"
            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()

            #Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(PRED_INPUT_FILE, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")

        except Exception as e:
            self.logger.log(log_file, "File exporting failed. Error : %s" %e)
            raise e





