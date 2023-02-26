from wsgiref import simple_server
# from markupsafe import escape
# from flask import Flask, request, render_template
# from flask import Response
import os
# from flask_cors import CORS, cross_origin
from strength.training.training_model.training_model import TrainModel
from training_validation_insertion import TrainValidation
# import flask_monitoringdashboard as dashboard
from strength.predicton.prediciton_model.prediction_model import prediction
from prediction_validation_insertion import PredValidation

# os.putenv('LANG', 'en_US.UTF-8')
# os.putenv('LC_ALL', 'en_US.UTF-8')

# app = Flask(__name__)
# dashboard.bind(app)
# CORS(app)

# @app.route("/", methods=['GET'])
# @cross_origin()
# def home():
#     return render_template('index.html')

# @app.route("/train", methods=['POST'])
# @cross_origin()


if __name__ == "__main__":

    # def trainRouteClient():
    # try:
        # if request.json['folderPath'] is not None:
            # path = request.json['folderPath']
        # path = os.path.join("strength","training","Training_Batch_Files")    #['folderPath']
        # train_valObj = TrainValidation(path) #object initialization

        # train_valObj.train_validation()#calling the training_validation function


    #     trainModelObj = TrainModel() #object initialization
    #     trainModelObj.training_model() #training the model for the files in the table


    # except ValueError as e:
    #     raise e

    #     return Response("Error Occurred! %s" % ValueError)

    # except KeyError:

    #     return Response("Error Occurred! %s" % KeyError)

    # except Exception as e:

    #     return Response("Error Occurred! %s" % e)
    # return Response("Training successfull!!")

# @app.route("/predict", methods=['POST'])
# @cross_origin()
# def predictRouteClient():
    try:
        # if request.json is not None:
        #     path = request.json['filepath']

        #     pred_val = PredValidation(path) #object initialization

        #     pred_val.prediction_validation() #calling the prediction_validation function

        #     pred = prediction(path) #object initialization

        #     # predicting for dataset present in database
        #     path = pred.predictionFromModel()
        #     # return Response("Prediction File created at %s!!!" % path)
        # elif request.form is not None:
            path = "strength\predicton\Prediction_Batch_files"

            pred_val = PredValidation(path) #object initialization

            pred_val.prediction_validation() #calling the prediction_validation function

            pred = prediction(path) #object initialization

            # predicting for dataset present in database
            path = pred.predictionFromModel()

    except ValueError as e:
        raise e
#             return Response("Prediction File created at %s!!!" % path)

#     except ValueError:
#         return Response("Error Occurred! %s" %ValueError)
#     except KeyError:
#         return Response("Error Occurred! %s" %KeyError)
#     except Exception as e:
#         return Response("Error Occurred! %s" %e)


# port = int(os.getenv("PORT",5001))
# if __name__ == "__main__":
#     host='0.0.0.0'
#     httpd = simple_server.make_server( host,port, app)
#     print("Serving on %s %d" % ( host,port))
#     httpd.serve_forever()