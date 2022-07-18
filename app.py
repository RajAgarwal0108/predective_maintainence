
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            Process_temperature = float(request.form['Process_temperature'])
            Rotational_speed = float(request.form['Rotational_speed'])
            Torque = float(request.form['Torque'])
            Tool_wear = float(request.form['Tool_wear'])
            Machine_failure = request.form['Machine_failure']
            TWF = request.form['TWF']
            HDF = request.form['HDF']
            PWF = request.form['PWF']
            OSF = request.form['OSF']
            RNF = request.form['RNF']
            filename = 'predective_maintainence.pickle'
            loaded_model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            scaler  = pickle.load(open('standard_scaler.pickle','rb'))
            test = scaler.transform([[Process_temperature,Rotational_speed,Torque,Tool_wear,Machine_failure,TWF,HDF,PWF,OSF,RNF]])
            prediction=loaded_model.predict(test)
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')

@app.route('/report',methods=['GET','POST'])
@cross_origin()
def report():
    print('h')
    return render_template('predective_maintainence.html')



if __name__ == "__main__":
	app.run(debug=True) # running the app