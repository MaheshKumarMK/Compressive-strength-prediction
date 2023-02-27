# Compressive-strength-prediction

# Business use case:

Compressive strength is the ability of material (concrete) or structure to carry the loads on its surface without any crack or deflection.

Concrete strength (compressive strength) is by far the most important property of concrete. It represents the mechanical characteristics of concrete; The 28 days’ compressive strength of concrete cylinders or cube samples has widely been accepted as the minimum specified concrete strength in most design codes (ACI 318-14, CSA A23.3-14). Concrete Strength is also considered a key factor in obtaining desired Durability Performance.
During Concreting work, random concrete sample test specimens are collected and are tested on compression testing machine after 7 days curing or 28 days curing.

Main purpose of the test:
1.	The compressive strength of cubes gives us the information of the potential strength of the concrete mix from which it is sampled.

2.	It helps in determining whether correct mix proportions of various mix proportions of various materials were used to get the desired strength.

3.	The variations in the results obtained at the site, from time to time for a particular grade of concrete can help in determining the quality control exercised and uniformity of concrete produced.

Strength of Concrete at various ages:

![alt text](https://github.com/MaheshKumarMK/Compressive-strength-prediction/blob/54345fdd6d3d9e73850a821c8f3d6c56af17e501/images/Capture.PNG)

The failure of compressive strength tests can result in significant costs and workforce requirements as the built structure may need to be discarded and rebuilt. This is why it is important to ensure the proper mixing and curing of concrete and to regularly test concrete samples to confirm that they meet the required strength specifications. The results of the compressive strength tests help to ensure the structural integrity and safety of the concrete structures, preventing costly failures in the future.


# Problem objective:
Reduce the risk and cost involved in discarding the concrete structures when the concrete cube test fails.

# Solution proposed:
To build a regression model to predict the concrete compressive strength based before hand on the different features in the training data.


# Architecture:
 
![alt text](https://github.com/MaheshKumarMK/Compressive-strength-prediction/blob/c46717b41c055333798224270dbb9d03a4f32d5f/images/Picture1.jpg)

Data Description
Given is the variable name, variable type, the measurement unit and a brief description. 
The concrete compressive strength is the regression problem. The order of this listing 
corresponds to the order of numerals along the rows of the database. 

Apart from training files, we also require a "schema" file from the client, which contains all the relevant information about the training files such as:
Name of the files, Length of Date value in Filename, Length of Time value in Filename, Number of Columns, Name of the Columns, and their datatype.
 

# Data Validation 
In this step, we perform different sets of validation on the given set of training files.  

1.	We have created a class “TrainValidation” which initializes logger file and classes “RawValidation” and “DBoperation” which defines a method “train_validation”.
2.	Under this method “RawValidation “ class is called and following validations are done, 
a)	A “manual regex” method is defined which checks the exact pattern of the file name.
b)	“goodbadrawdatadirectory” method is defined which creates directories to save good and bad raw valid datas.
c)	Method “delete_existing_good_datafolder” and “delete_existing_bad_datafolder” are created which uses “shutill.rmtree” library to remove the directories.
d)	Method”move_files_to_archieve_bad” is defined which creates a directory to move all the bad raw data to the archive folder and deletes the bad data directory. These archived file is sent back to clients to recheck the invalid data and send the valid file. “shutil.move” is used to move the files to the archive directory.
e)	Method “validationfilenameraw” ,
-	Deletes the good and bad data valid folder (if existing) first and creates a new good data valid raw data directory.
-	Validates the name of the csv files from batch files based on the given name in the schema file. We have created a regex pattern as per the name given in the schema file to use for validation.  
-	If the data is valid, it copies the data to good data folder , else to bad data folder using “shutill.copy” library.

f)	Method “validate_col_length”,
-	Reads the good data file from the directory and this function validates the number of columns in the csv files.
-	It is should be same as given in the schema file.
-	If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
-	 If the column number matches, file is kept in Good Raw Data for processing.

g)	Method “validateMissingValuesInWholeColumn” is defined which,
-	
h)	 
i)	The datatype of columns - The datatype of columns is given in the schema file. This is validated when we insert the files into Database. If the datatype is wrong, then the file is moved to "Bad_Data_Folder".

j)	Null values in columns - If any of the columns in a file have all the values as NULL or missing, we discard such a file and move it to "Bad_Data_Folder".



# Data Insertion in Database
1) Database Creation and connection - Create a database with the given name passed. If the database is already created, open the connection to the database. 
2) Table creation in the database - Table with name - "Good_Data", is created in the database for inserting the files in the "Good_Data_Folder" based on given column names and datatype in the schema file. If the table is already present, then the new table is not created and new files are inserted in the already present table as we want training to be done on new as well as old training files.     
3) Insertion of files in the table - All the files in the "Good_Data_Folder" are inserted in the above-created table. If any file has invalid data type in any of the columns, the file is not loaded in the table and is moved to "Bad_Data_Folder".
 
# Model Training 
1) Data Export from Db - The data in a stored database is exported as a CSV file to be used for model training.
2) Data Preprocessing  
   a) Check for null values in the columns. If present, impute the null values using the KNN imputer
   b) transform the features using log transformation
   c) Scale the training and test data separately 
3) Clustering - KMeans algorithm is used to create clusters in the preprocessed data. The optimum number of clusters is selected by plotting the elbow plot, and for the dynamic selection of the number of clusters, we are using "KneeLocator" function. The idea behind clustering is to implement different algorithms
   To train data in different clusters. The Kmeans model is trained over preprocessed data and the model is saved for further use in prediction.
4) Model Selection - After clusters are created, we find the best model for each cluster. We are using two algorithms, "Random forest Regressor" and “Linear Regression”. For each cluster, both the algorithms are passed with the best parameters derived from GridSearch. We calculate the Rsquared scores for both models and select the model with the best score. Similarly, the model is selected for each cluster. All the models for every cluster are saved for use in prediction. 
 
# Prediction Data Description
 
Client will send the data in multiple set of files in batches at a given location. Data will contain climate indicators in 8 columns.
Apart from prediction files, we also require a "schema" file from client which contains all the relevant information about the training files such as:
Name of the files, Length of Date value in FileName, Length of Time value in FileName, Number of Columns, Name of the Columns and their datatype.
 Data Validation  
In this step, we perform different sets of validation on the given set of training files.  
1) Name Validation- We validate the name of the files on the basis of given Name in the schema file. We have created a regex pattern as per the name given in schema file, to use for validation. After validating the pattern in the name, we check for length of date in the file name as well as length of time in the file name. If all the values are as per requirement, we move such files to "Good_Data_Folder" else we move such files to "Bad_Data_Folder". 
2) Number of Columns - We validate the number of columns present in the files, if it doesn't match with the value given in the schema file then the file is moved to "Bad_Data_Folder". 
3) Name of Columns - The name of the columns is validated and should be same as given in the schema file. If not, then the file is moved to "Bad_Data_Folder". 
4) Datatype of columns - The datatype of columns is given in the schema file. This is validated when we insert the files into Database. If dataype is wrong then the file is moved to "Bad_Data_Folder". 
5) Null values in columns - If any of the columns in a file has all the values as NULL or missing, we discard such file and move it to "Bad_Data_Folder".  
Data Insertion in Database 
1) Database Creation and connection - Create database with the given name passed. If the database is already created, open the connection to the database. 
2) Table creation in the database - Table with name - "Good_Data", is created in the database for inserting the files in the "Good_Data_Folder" on the basis of given column names and datatype in the schema file. If table is already present then new table is not created, and new files are inserted the already present table as we want training to be done on new as well old training files.     
3) Insertion of files in the table - All the files in the "Good_Data_Folder" are inserted in the above-created table. If any file has invalid data type in any of the columns, the file is not loaded in the table and is moved to "Bad_Data_Folder".


# Prediction 
1) Data Export from Db - The data in the stored database is exported as a CSV file to be used for prediction.
2) Data Preprocessing   
   a) Check for null values in the columns. If present, impute the null values using the KNN imputer
   b) transform the features using log transformation
   c) Scale the training and test data separately 
3) Clustering - KMeans model created during training is loaded, and clusters for the preprocessed prediction data is predicted.
4) Prediction - Based on the cluster number, the respective model is loaded and is used to predict the data for that cluster.
5) Once the prediction is made for all the clusters, the predictions along with the original names before label encoder are saved in a CSV file at a given location and the location is returned to the client.
 

