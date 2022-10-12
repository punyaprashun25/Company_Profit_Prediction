from flask import Flask,render_template,request
import pickle,numpy as np
import pandas as pd
model = pickle.load(open('model.pkl','rb'))
scaler = pickle.load(open('scaler_model.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict_placement():

    rd_spend = float(request.form.get('rd spend'))
    administration = float(request.form.get('administration'))
    marketing_spend = float(request.form.get('marketing spend'))

    input = np.array([rd_spend,administration,marketing_spend]).reshape(1,3)

    #scaling input data
    input_scaled = scaler.transform(input)

    # prediction
    result = model.predict(input_scaled)
    profit = round((result[0][0]),2)
    return render_template('index.html',result="Predicted Profit of your company is {}$".format(profit))

if __name__ == '__main__':
    app.run(debug=True)