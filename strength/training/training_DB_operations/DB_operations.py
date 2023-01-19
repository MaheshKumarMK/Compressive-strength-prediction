import shutil
import csv
import os
import sys
from datetime import datetime
import sqlite3

from strength.exception import StrengthException
from strength.logger import App_Logger
from strength.constants.training_pipeline import *
from strength.constants.log_files import *

class dBOperation:
    """
    This class shall be used for handling all the SQL operations.
    """

    def __init__(self) -> None:

        self.logger = App_Logger()

        self.goodFilePath = TRAINING_GOOD_RAW_FILES_VALIDATED

        self.badFilePath = TRAINING_BAD_RAW_FILES_VALIDATED

        self.path = DATABASE_PATH

    def dataBaseConnection(self,DatabaseName):

        """
        Method Name: dataBaseConnection
        Description: This method creates the database with the given name and if Database already exists then opens the connection to the DB.
        Output: Connection to the DB
        On Failure: Raise ConnectionError

        """
        try:
            conn= sqlite3.connect(DATABASE_PATH+DatabaseName+".db" )

            file = DATABASE_CONN_LOG

            self.logger.log(file, "Opened %s database successfully" % DatabaseName)

            file.close()

        except ConnectionError as e:

            file = DATABASE_CONN_LOG

            self.logger.log(file,"Error while connecting to database: %s" %e )

            file.close()

            raise ConnectionError

        except Exception as e:
            raise StrengthException(e,sys)
        
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

            cur = conn.cursor()

            cur.execute("SELECT count(name) FROM sqlite_master WHERE type = 'table'AND name = 'Good_Raw_Data'")

            if cur.fetchone()[0]==1:

                conn.close()

                file = DB_TABLE_LOG

                self.logger.log(file, "Tables created successfully!!")

                file.close()

                file = DB_TABLE_LOG

                self.logger.log(file, "Closed %s database successfully" % DatabaseName)

                file.close()
            
            else:

                for key in column_names.keys():

                    type = column_names[key]

                    #in try block we check if the table exists, if yes then add columns to the table
                    # else in catch block we will create the table

                    try:
                        #cur = cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Good_Raw_Data'".format(dbName=DatabaseName))
                        cur.execute('ALTER TABLE Good_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    except:
                        cur.execute('CREATE TABLE  Good_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))


                    # try:
                    #     #cur.execute("SELECT name FROM {dbName} WHERE type='table' AND name='Bad_Raw_Data'".format(dbName=DatabaseName))
                    #     conn.execute('ALTER TABLE Bad_Raw_Data ADD COLUMN "{column_name}" {dataType}'.format(column_name=key,dataType=type))
                    #
                    # except:
                    #     conn.execute('CREATE TABLE Bad_Raw_Data ({column_name} {dataType})'.format(column_name=key, dataType=type))

                conn.close()

                file = DB_TABLE_LOG

                self.logger.log(file, "Tables created successfully!!")

                file.close()

                file = DATABASE_CONN_LOG

                self.logger.log(file, "Closed %s database successfully" % DatabaseName)

                file.close()

        except Exception as e:

            file = DB_TABLE_LOG

            self.logger.log(file, "Error while creating table: %s " % e)

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

        onlyfiles = [f for f in os.listdir(goodFilePath)]

        log_file = DB_INSERT_LOG

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

        self.fileFromDb = 'Training_FileFromDB/'

        self.fileName = 'InputFile.csv'

        log_file = open("Training_Logs/ExportToCsv.txt", 'a+')

        try:

            conn = self.dataBaseConnection(Database)

            sqlSelect = "SELECT *  FROM Good_Raw_Data"

            cursor = conn.cursor()

            cursor.execute(sqlSelect)

            results = cursor.fetchall()
            
            # Get the headers of the csv file
            headers = [i[0] for i in cursor.description]

            #Make the CSV ouput directory
            if not os.path.isdir(self.fileFromDb):
                os.makedirs(self.fileFromDb)

            # Open CSV file for writing.
            csvFile = csv.writer(open(self.fileFromDb + self.fileName, 'w', newline=''),delimiter=',', lineterminator='\r\n',quoting=csv.QUOTE_ALL, escapechar='\\')

            # Add the headers and data to the CSV file.
            csvFile.writerow(headers)
            csvFile.writerows(results)

            self.logger.log(log_file, "File exported successfully!!!")
            log_file.close()

        except Exception as e:

            self.logger.log(log_file, "File exporting failed. Error : %s" %e)

            log_file.close()




































































































































































































































             
