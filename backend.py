import os
import json
import random
import hashlib
from flask import Flask, request, jsonify, Response
from influxdb import InfluxDBClient
from datetime import datetime, timedelta, date
from flask_cors import CORS, cross_origin

import predictv2

#   steup for all
app = Flask(__name__)
CORS(app)
client = InfluxDBClient('localhost', "8086", 'backend', 'backend', 'mydb')
measurement_table = "measurement10"

###########################################
#   Sekcja funckji                        #
###########################################
def transform_json_for_db_insert(data: dict):
    list_of_data = []
    for key in data.keys():
        temp = data[key]
        sample = {
            "measurement": measurement_table,
            "time": datetime.utcfromtimestamp(temp["timestamp"]).strftime('%Y-%m-%d %H:%M:%S.%f'),
            "fields":{
                "voltage": temp["voltage"],
                "current": temp["current"]*(-1),
                "power": temp["power"],
                "timestamp": temp["timestamp"],
                "id": random.randrange(2)
            }
        }
        list_of_data.append(sample)
    client.write_points(list_of_data)
    return    


def post_data():
    if request.method == "POST":
        data = request.json
        transform_json_for_db_insert(data)
        list = client.get_list_database()
        return list


def read_data1():
    result = client.query(f'select * from {measurement_table};')
    print(result)
    print(type(result))
    list_of_records = list(result.get_points(measurement=f"{measurement_table}"))
    print(list_of_records)
    return list_of_records


def get_time_batch(timestamp_start, timestamp_end):
    time_difference = (timestamp_end - timestamp_start) / 20
    if time_difference < 1:
        x = str(int(time_difference * 1000000)) + "u"
        return x
    elif time_difference < 60:
        x = str(int(time_difference)) + "s"
        return x
    elif time_difference < 3600:
        x = str(int(time_difference / 60)) + "m"
        return x
    elif time_difference < 86400:
        x = str(int(time_difference / (60*60))) + "h"
        return x
    else:
        x = str(int(time_difference / (60*60*24))) + "d"
        return x 


def send_answer_to_frontend1():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start'] / 1000
        time_end = json.loads(request.data.decode('utf-8'))['end'] / 1000
        amount = 20
        time_diffference_step = (time_end - time_start) / amount
        time_from = time_start
        time_to = time_start
        final_result = {}

        for step in range(1,amount+1):
            time_to += time_diffference_step
            query = f"""
            select mean(power) AS "MeanPower" from {measurement_table}
            where time >= '{datetime.utcfromtimestamp(time_from).strftime('%Y-%m-%d %H:%M:%S.%f')}'
            and time < '{datetime.utcfromtimestamp(time_to).strftime('%Y-%m-%d %H:%M:%S.%f')}'
            """
            result = client.query(query)
            final_result[time_from] = next(iter(result))[0]['MeanPower']
            time_from = time_to
            
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result

def send_answer_to_frontend1_v2():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start'] / 1000
        time_end = json.loads(request.data.decode('utf-8'))['end'] / 1000
        time_range_unit = get_time_batch(time_start, time_end)
        time_diff = (time_end - time_start) / 20
        print(time_range_unit)
        final_result = {}
        query = f"""
        select mean(power) AS "MeanPower" from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        group by time({time_range_unit})
        """
        print(query)
        final_result = {}
        try:
            list_time_and_price = next(iter(client.query(query)))
            print(list_time_and_price)
            time_act = time_start
            print(time_start)
            for element in(list_time_and_price):
                if element['MeanPower'] is not None:
                    final_result[f"{time_act}"] = element['MeanPower']
                time_act += time_diff
        except:
            return json.dumps({})
        
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


def send_answer_to_frontend1_v3():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start'] / 1000
        time_end = json.loads(request.data.decode('utf-8'))['end'] / 1000
        devices = []
        devices = json.loads(request.data.decode('utf-8'))['devices']
        time_range_unit = get_time_batch(time_start, time_end)
        time_diff = (time_end - time_start) / 20
        print(time_range_unit)
        final_result = {}
        if not bool(devices):
            return json.dump({0:0,1:1}, indent=2)
        for device in devices:
            query = f"""
            select mean(power) AS "MeanPower" from {measurement_table}
            where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
            and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
            and id = {device}
            group by time({time_range_unit})
            """
            print(query)
            try:
                list_time_and_price = next(iter(client.query(query)))
                print(list_time_and_price)
                time_act = time_start
                final_result[f"{device}"] = {}
                for element in(list_time_and_price):
                    if element['MeanPower'] is not None:
                        final_result[f"{device}"][f"{time_act*1000}"] = element['MeanPower']
                    time_act += time_diff
            except:
                return json.dumps({})
        
        print(final_result)
        json_final_result = json.dumps(final_result, indent=2)
        with open("test12345", "w") as file:
            file.write(json_final_result)
        return json_final_result

def send_answer_to_frontend2():
    """
    voltage for given time
    """
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start'] / 1000
        time_end = json.loads(request.data.decode('utf-8'))['end'] / 1000
       
        query = f"""
        select voltage, timestamp from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        """        
        result = client.query(query)
        try:
            result = next(iter(result))
        except:
            return json.dumps({"0":{},"1":{}})
        final_result = {}
        for element in range(len(result)):
            final_result[result[element]['timestamp']*1000] = result[element]['voltage']

        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


def send_answer_to_frontend3():
    """
    current for given time range
    """
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start'] / 1000
        time_end = json.loads(request.data.decode('utf-8'))['end'] / 1000
        print(time_start)
        print(time_end)
        query = f"""
        select current, timestamp from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        """
        result = client.query(query)
        try:
            result = next(iter(result))
        except:
            return json.dumps({})

        final_result = {}
        for element in range(len(result)):
            final_result[result[element]['timestamp']*1000] = result[element]['current']
        
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


def send_answer_to_frontend4():
    """
    price for given time range
    """
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start'] / 1000
        time_end = json.loads(request.data.decode('utf-8'))['end'] / 1000
       
        query = f"""
        select mean(power) AS Power from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        """
        try:
            power_level = next(iter(client.query(query)))[0]["Power"] / 1000
        except:
            return json.dumps({})
        time_span = (time_end - time_start) / 3600
        with open("settings.json", 'r') as setting:
            electricityPrice = json.load(setting)['electricityPrice']
        final_result = {}
        final_result["cost"] = electricityPrice * time_span * power_level
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


def send_answer_to_frontend4v2():
    """
    usage & cost & prediction 
    """
    if request.method == "POST":
        span = json.loads(request.data.decode('utf-8'))['span']
        time_now = datetime.now()
        time = time_now.replace(minute=0, second=0, hour=0, microsecond=0)
        if span == "week":
            time = time - timedelta(days=time.weekday())
        elif span == "month":
            time = time.replace(day=1)
        elif span == "year":
            time = time.replace(day=1, month=1)
        query = f"""
        select mean(power) AS Power from {measurement_table}
        where time >= '{time}'
        """
        try:
            power_level = next(iter(client.query(query)))[0]["Power"] / 1000
        except:
            return json.dumps({})
        
        with open("settings.json", 'r') as setting:
            settings_dict = json.load(setting)
            priceAlert = settings_dict['priceAlert']
            electricity = settings_dict['electricityPrice']

        final_result = {}
        time_span = (datetime.timestamp(time_now)-datetime.timestamp(time)) / 3600
        usage = power_level * time_span 
        cost = usage * electricity
        final_result["usage"] = usage
        final_result["price"] = cost
        model = predictv2.loadModel("arima_model.joblib")
        final_result["prediction"] = predictv2.predictUsage(model,30)
        return json.dumps(final_result, indent=2)


def send_answer_to_frontend5():
    """
    alert / notification
    """
    if request.method == "GET":
        with open("settings.json", 'r') as setting:
            settings_dict = json.load(setting)
            priceAlert = settings_dict['priceAlert']
            usageAlert = settings_dict['usageAlert']
        
        date_end = datetime.now()
        date_start = date_end.replace(minute=0, second=0, hour=0, day=1, microsecond=0)
        date_span = (datetime.timestamp(date_end) - datetime.timestamp(date_start) ) / 3600
        query = f"""
        select mean(power) AS Power from {measurement_table}
        where time >= '{date_start}'
        """
        try:
            power_level = next(iter(client.query(query)))[0]["Power"] / 1000
        except:
            final_result = {}
            final_result["usage"] = False
            final_result["price"] = False
            json_final_result = json.dumps(final_result, indent=2)
            return json_final_result
        usage = power_level * date_span 
        cost = usage * priceAlert["value"]

        final_result = {}
        if usage > int(usageAlert["value"]) and usageAlert["on"] == True:
            final_result["usage"] = True
        else:
            final_result["usage"] = False
        
        if cost > int(priceAlert["value"]) and priceAlert["on"] == True:
            final_result["price"] = True
        else:
            final_result["price"] = False
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


def send_answer_to_frontend6():
    """
    login user
    """
    if request.method == "POST":
        login = json.loads(request.data.decode('utf-8'))['username']
        password = json.loads(request.data.decode('utf-8'))['password']
        hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        with open("users.json", "r") as file:
            users_dict = json.load(file)
        final_result = {}
        if login in users_dict.keys():
            if hash == users_dict[login]:
                final_result["status"] = True
                final_result["message"] = "OK"
            else:
                final_result["status"] = False
                final_result["message"] = "Wrong password"
        else:
            final_result["status"] = False
            final_result["message"] = "Wrong user"

        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


def send_answer_to_frontend7():
    """
    register user
    """
    if request.method == "POST":
        login = json.loads(request.data.decode('utf-8'))['username']
        password = json.loads(request.data.decode('utf-8'))['password']
        hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        with open("users.json", "r") as file:
            users_dict = json.load(file)
        final_result = {}
        if login in users_dict.keys():
            final_result["status"] = False
            final_result["message"] = "User already exist"
        else:
            users_dict[login] = hash
            json_object = json.dumps(users_dict, indent=2)
            with open("users.json",'w') as file:
                file.write(json_object)
            final_result["status"] = True
            final_result["message"] = "User added"
        
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result


###########################################
#   sekcja API                            #
###########################################
@app.route('/')
@cross_origin()
def index():
    return "Hello, IoT"

@app.route("/ip-discovery")
@cross_origin()
def hello():
    return Response("Hello", status=418, mimetype='application/json')

@app.route('/api/postdata', methods = ['POST'])
@cross_origin()
def store_data():
    return post_data()

@app.route('/api/readdata', methods = ['POST'])
@cross_origin()
def read_data():
    return read_data1()

@app.route('/api/frontend_req1', methods = ['POST'])
@cross_origin()
def get_frontend_request():
    return send_answer_to_frontend1_v3()

@app.route('/api/voltage', methods = ['POST'])
@cross_origin()
def get_frontend_request2():
    return send_answer_to_frontend2()

@app.route('/api/current', methods = ['POST'])
@cross_origin()
def get_frontend_request3():
    return send_answer_to_frontend3()

@app.route('/api/cost', methods = ['POST'])
@cross_origin()
def get_frontend_request4():
    response = send_answer_to_frontend4v2()
    return response

@app.route('/notification')
@cross_origin()
def get_frontend_request5():
    return send_answer_to_frontend5()

@app.route("/login", methods=['POST'])
@cross_origin()
def checklogin():
    response = send_answer_to_frontend6()
    return response

@app.route("/register", methods=['POST'])
@cross_origin()
def register():
    return send_answer_to_frontend7()

@app.route("/set-settings", methods=['POST'])
@cross_origin()
def setSettings():
    with open("settings.json", 'w') as settings:
        settings.write(request.data.decode('utf-8'))
    return jsonify(True)

@app.route("/get-settings")
@cross_origin()
def getSettings():
    with open("settings.json", 'r') as settings:
        response = settings.read()
    return response

if __name__ =="__main__":
    host = os.environ.get('IP', '0.0.0.0')
    port = 8080
    app.run(host=host, port=port, debug=True)




