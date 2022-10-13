from flask import Flask,render_template,request
import pickle,numpy as np
from flask_mysqldb import MySQL
model = pickle.load(open('model.pkl','rb'))
scaler = pickle.load(open('scaler_model.pkl','rb'))

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'company'
 
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict_placement():
    
    company_name = request.form.get('company_name')
    rd_spend = float(request.form.get('rd spend'))
    administration = float(request.form.get('administration'))
    marketing_spend = float(request.form.get('marketing spend'))

    input = np.array([rd_spend,administration,marketing_spend]).reshape(1,3)

    #scaling input data
    input_scaled = scaler.transform(input)

    # prediction
    result = model.predict(input_scaled)
    profit = round((result[0][0]),2)
    cursor = mysql.connection.cursor()
    cursor.execute(' INSERT INTO Company VALUES(%s,%s,%s,%s,%s)',(company_name,rd_spend,administration,marketing_spend,profit))
    mysql.connection.commit()
    cursor.close()
    return render_template('index.html',result="Predicted Profit of {} is {}$".format(company_name,profit))

if __name__ == '__main__':
    app.run(debug=True)