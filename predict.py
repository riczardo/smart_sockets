import pandas as pd
from pmdarima import auto_arima
import numpy as np
import joblib

# path to historical data and saved model
path = 'year.json'
model_file = 'arima_model.joblib'

# loading historical data
def readData(path):
    df = pd.read_json(path).T
    df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')
    df['consumption'] = df['power'] * 1 * 0.001
    df = df.drop(['current', 'power', 'voltage', 'timestamp'], axis=1)
    return df

def trainModel(df):
    train = np.array(df['consumption'][5996:6884].values)
    test = np.array(df['consumption'][6884:7400].values)

    arima_model = auto_arima(train, trace=True,start_p=1, start_q=1, max_p=1, max_d=1, max_q=1,D=1, start_Q=3, max_P=1, max_D=1, max_Q=3, max_order=6,n_fits=100,method='lbfgs',m=24,seasonal=True)
    return arima_model

# loading trained model
def loadModel(model_file):
    arima_model = joblib.load(model_file)
    return arima_model

# energy consumption forecast for specified number of days [kWh]
def predictConsumption(arima_model, days):
    prediction = arima_model.predict(n_periods=days*24)
    consumption = np.sum(prediction)
    return consumption

# one day forecast hourly [kWh]
def predictDay(arima_model):
    prediction = arima_model.predict(n_periods=24)
    prediction = pd.DataFrame({ 'consumption': prediction })
    prediction['timestamp'] = pd.date_range(start='00:00:00', end='23:00:00', freq='1H')
    prediction['timestamp']=prediction['timestamp'].dt.strftime('%H:%M')
    return prediction.to_json(orient='index')


# example
'''arima_model=loadModel(model_file)
consumption = predictConsumption(arima_model, 30)
print(consumption)
data = predictDay(arima_model)
print(data)'''
