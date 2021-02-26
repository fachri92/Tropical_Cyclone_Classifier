from flask import Flask, render_template, request, session, redirect
import numpy as np
import pandas as pd
import seaborn as sb
import plotly
import plotly.graph_objs as go
import mysql.connector
# Data dari flask di kirim ke browser dalam bentuk json
import json
import joblib
import pickle

# Sumber Data
pacific = pd.read_csv('Pacific_Deployment.csv').set_index('Unnamed: 0')



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# Render Picture
@app.route('/static/<path:x>')
def gal(x):
    return send_from_directory("static",x)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    return render_template('predict.html')
'''
'Maximum Wind', 'Minimum Pressure', 'Year', 'Latitude', 'Longitude'
'''
@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method=='POST':
        input = request.form

        df_to_predict = pd.DataFrame({
            'Maximum Wind': [input['Maximum Wind']],
            'Minimum Pressure': [input['Minimum Pressure']],
            'Year': [input['Year']],
            'Latitude': [input['Latitude']],
            'Longitude': [input['Longitude']]
        })

        prediksi = model.predict(df_to_predict)

        return render_template('result.html', data=input, pred=prediksi[0])
@app.route('/index')
def index():
    return render_template('index.html')



# Data Visualization

@app.route('/piechart')
def piechart():
    return render_template('piechart.html')

@app.route('/yearlyfrequency')
def yearlyfrequency():
    return render_template('yearlyfrequency.html')

@app.route('/monthlyfrequency')
def monthlyfrequency():
    return render_template('monthlyfrequency.html')   

@app.route('/scatplot')
def scatplot():
    return render_template('scatplot.html')  

@app.route('/categoryfrequency')
def categoryfrequency():
    return render_template('categoryfrequency.html')  
    
@app.route('/maxwind')
def maxwind():
    return render_template('maxwind.html') 

@app.route('/correlation')
def correlation():
    return render_template('correlation.html') 

#  Input and Delete
@app.route('/input', methods=("POST", "GET"))
def data():
    n = [a for a in range(len(pacific))]
    list_name = pacific['Name']
    list_month = pacific['Month']
    list_year = pacific['Year']
    list_status = pacific['Status']
    list_max = pacific['Maximum Wind']
    list_min = pacific['Minimum Pressure']
    return render_template('input.html', n=n, list_name = list_name, list_month=list_month, list_year=list_year, list_status=list_status, 
     list_max=list_max, list_min = list_min, tables=[pacific.to_html(classes='data')], titles=pacific.columns.values)

@app.route('/inputdata', methods=["POST"])
def inputdata():
    input = request.form
    name = str(input['Name'])
    month = float(input['Month'])
    year = float(input['Year'])
    maximum = float(input['Maximum Wind'])
    minimum = float(input['Minimum Pressure'])
    status = input['Status']
    if status == '0':
        status_cat = 'HU'
    elif status == '1':
        status_cat = 'TS'
    elif status == '2':
        status_cat = 'LO'
    elif status == '3':
        status_cat = 'TD'
    pacific = pd.read_csv('Pacific_Deployment.csv').set_index('Unnamed: 0')
    listappend = [name,month,year,status_cat,maximum,minimum]
    pacific.loc[len(pacific)] = listappend
    pacific.to_csv('Pacific_Deployment.csv')
    n = [a for a in range(len(pacific))]
    list_name = pacific['Name']
    list_month = pacific['Month']
    list_year = pacific['Year']
    list_status = pacific['Status']
    list_max = pacific['Maximum Wind']
    list_min = pacific['Minimum Pressure']
    return render_template('input.html', n=n, list_name = list_name, list_month=list_month, list_year=list_year, list_status=list_status, 
     list_max=list_max, list_min = list_min, tables=[pacific.to_html(classes='data')], titles=pacific.columns.values)
    
@app.route('/delete', methods=["POST"])
def delete():
    input = request.form
    row = int(input['Row'])
    pacific = pd.read_csv('Pacific_Deployment.csv').set_index('Unnamed: 0')
    if 0 < row <= len(pacific) :
        pacific = pacific[:len(pacific)-row]
        pacific.to_csv('Pacific_Deployment.csv')
    else:
        pass
    n = [a for a in range(len(pacific))]
    list_name = pacific['Name']
    list_month = pacific['Month']
    list_year = pacific['Year']
    list_status = pacific['Status']
    list_max = pacific['Maximum Wind']
    list_min = pacific['Minimum Pressure']
    return render_template('input.html', n=n, list_name = list_name, list_month=list_month, list_year=list_year, list_status=list_status, 
     list_max=list_max, list_min = list_min, tables=[pacific.to_html(classes='data')], titles=pacific.columns.values)
if __name__ == '__main__':
    filename = 'rfc4.sav'
    model = pickle.load(open(filename,'rb'))
    app.run(debug=True, port=4000)

