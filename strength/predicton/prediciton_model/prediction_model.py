import pandas
import os
from strength.training.file_operations import file_methods
from strength.training.data_preprocessing import preprocessing
from strength.predicton.data_ingestion import data_loader_prediction
from strength.logger import App_Logger
from strength.predicton.Prediction_Raw_Data_Validation.predictionDataValidation import Prediction_Data_validation
from strength.constants.log_files import *


class prediction:

    def __init__(self,path):

        self.file_object = open(PREDICTION_LOG, 'a+')

        self.log_writer = App_Logger()

        self.pred_data_val = Prediction_Data_validation(path)

    def predictionFromModel(self):

        try:
            self.pred_data_val.deletePredictionFile() #deletes the existing prediction file from last run!

            self.log_writer.log(self.file_object,'Start of Prediction')

            data_getter=data_loader_prediction.Data_Getter_Pred(self.file_object,self.log_writer)

            data=data_getter.get_data()


            preprocessor=preprocessing.Preprocessor(self.file_object,self.log_writer)

            is_null_present,cols_with_missing_values=preprocessor.is_null_present(data)
            
            if(is_null_present):

                data=preprocessor.impute_missing_values(data)

            data  = preprocessor.logTransformation(data)

            #scale the prediction data
            data_scaled = pandas.DataFrame(preprocessor.pred_standardScalingData(data),columns=data.columns)

            #data=data.to_numpy()
            file_loader=file_methods.File_Operation(self.file_object,self.log_writer)

            kmeans=file_loader.load_model('KMeans')

            ##Code changed
            #pred_data = data.drop(['Wafer'],axis=1)
            clusters=kmeans.predict(data_scaled)#drops the first column for cluster prediction

            data_scaled['clusters']=clusters

            clusters=data_scaled['clusters'].unique()

            result=[] # initialize blank list for storing predicitons
            # with open('EncoderPickle/enc.pickle', 'rb') as file: #let's load the encoder pickle file to decode the values
            #     encoder = pickle.load(file)

            for i in clusters:

                cluster_data= data_scaled[data_scaled['clusters']==i]

                cluster_data = cluster_data.drop(['clusters'],axis=1)

                model_name = file_loader.find_correct_model_file(i)
                
                model = file_loader.load_model(model_name)

                for val in (model.predict(cluster_data.values)):

                    result.append(val)

            result = pandas.DataFrame(result,columns=['Predictions'])

            pred_path="Prediction_Output_File"

            if not os.path.isdir(pred_path):
                os.makedirs(pred_path, exist_ok=True)


            result.to_csv(os.path.join(pred_path,"Predictions.csv"),header=True) #appends result to prediction file

            self.log_writer.log(self.file_object,'End of Prediction')

        except Exception as ex:

            self.log_writer.log(self.file_object, 'Error occured while running the prediction!! Error:: %s' % ex)

            raise ex
        
        return pred_path

            # old code
            # i=0
            # for row in data:
            #     cluster_number=kmeans.predict([row])
            #     model_name=file_loader.find_correct_model_file(cluster_number[0])
            #
            #     model=file_loader.load_model(model_name)
            #     #row= sparse.csr_matrix(row)
            #     result=model.predict([row])
            #     if (result[0]==-1):
            #         category='Bad'
            #     else:
            #         category='Good'
            #     self.predictions.write("Wafer-"+ str(wafer_names[i])+','+category+'\n')
            #     i=i+1
            #     self.log_writer.log(self.file_object,'The Prediction is :' +str(result))
            # self.log_writer.log(self.file_object,'End of Prediction')
            #print(result)




