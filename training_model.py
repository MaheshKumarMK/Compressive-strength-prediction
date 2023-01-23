"""
This is the Entry point for Training the Machine Learning Model.

"""
from sklearn.model_selection import train_test_split
from strength.logger import App_Logger
from strength.constants.log_files import *
from strength.constants.training_pipeline import *
from strength.training.data_ingestion.data_loader import DataGetter
from strength.training.data_preprocessing.preprocessing import Preprocessor
from strength.training.data_preprocessing.clustering import KMeansClustering
from strength.exception import StrengthException

class TrainModel:

    def __init__(self,) -> None:

        self.log_writer = App_Logger()

        self.file_object = MODEL_TRAINING_LOG

    def training_model(self):

    # Logging the start of Training
        self.log_writer.log(self.file_object, 'Start of Training')

        try:
            # Getting the data from the source
            data_getter=DataGetter(self.file_object,self.log_writer)

            data=data_getter.get_data()


            """doing the data preprocessing"""

            preprocessor = Preprocessor(self.file_object, self.log_writer)

            # check if missing values are present in the dataset
            is_null_present,cols_with_missing_values=preprocessor.is_null_present(data)

            # if missing values are there, replace them appropriately.
            if(is_null_present):

                data=preprocessor.impute_missing_values(data) # missing value imputation

            # create separate features and labels
            X, Y = preprocessor.separate_label_feature(data, label_column_name='Concrete_compressive _strength')

            X = preprocessor.logTransformation(X)


            """ Applying the clustering approach"""

            kmeans= KMeansClustering(self.file_object,self.log_writer) # object initialization.

            number_of_clusters=kmeans.elbow_plot(X)  #  using the elbow plot to find the number of optimum clusters

            # Divide the data into clusters
            X=kmeans.create_clusters(X,number_of_clusters)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels']=Y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()

            """ parsing all the clusters and looking for the best ML algorithm to fit on
                individual cluster.

            """

            for i in list_of_clusters:

                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)

                cluster_label= cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=36)

                x_train_scaled, x_test_scaled = preprocessor.standardScalingData(x_train, x_test)

        except Exception as e:

            # logging the unsuccessful Training
            self.log_writer.log(self.file_object, 'Unsuccessful End of Training')

            self.file_object.close()

            raise str



