import os
import json
import random
import hashlib
from flask import Flask, request, jsonify, Response
from influxdb import InfluxDBClient
from datetime import datetime
from flask_cors import CORS

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
                "current": temp["current"],
                "power": temp["power"],
                "timestamp": temp["timestamp"]
            }
        }
        list_of_data.append(sample)
    client.write_points(list_of_data)
    return    


def post_data():
    if request.method == "POST":
        data = request.json
        print(data)
        print(type(data))
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


def send_answer_to_frontend1():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start']
        time_end = json.loads(request.data.decode('utf-8'))['end']
        # body_data = request.json
        # print(type(body_data))
        #print(body_data)
        amount = 20
        # time_start = body_data["start"]
        # time_end = body_data["end"]
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


def send_answer_to_frontend2():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start']
        time_end = json.loads(request.data.decode('utf-8'))['end']
       
        query = f"""
        select voltage, timestamp from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        """
        result = client.query(query)
        result = next(iter(result))
        final_result = {}
        for element in range(len(result)):
            final_result[result[element]['timestamp']] = result[element]['voltage']
        
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result

def send_answer_to_frontend3():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start']
        time_end = json.loads(request.data.decode('utf-8'))['end']
       
        query = f"""
        select current, timestamp from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        """
        result = client.query(query)
        result = next(iter(result))
        final_result = {}
        for element in range(len(result)):
            final_result[result[element]['timestamp']] = result[element]['current']
        
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result

def send_answer_to_frontend4():
    if request.method == "POST":
        time_start = json.loads(request.data.decode('utf-8'))['start']
        time_end = json.loads(request.data.decode('utf-8'))['end']
       
        query = f"""
        select mean(power) AS Power from {measurement_table}
        where time >= '{datetime.utcfromtimestamp(time_start).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        and time < '{datetime.utcfromtimestamp(time_end).strftime('%Y-%m-%d %H:%M:%S.%f')}'
        """
        power_level = next(iter(client.query(query)))[0]["Power"]
        time_span = (time_end - time_start) / 3600
        with open("settings.json", 'r') as setting:
            electricityPrice = json.load(setting)['electricityPrice']
        final_result = {}
        final_result["cost"] = electricityPrice * time_span * power_level
        json_final_result = json.dumps(final_result, indent=2)
        return json_final_result

def send_answer_to_frontend5():
    if request.method == "GET":
        with open("settings.json", 'r') as setting:
            settings_dict = json.load(setting)
            priceAlert = settings_dict['priceAlert']
            usageAlert = settings_dict['usageAlert']
        
        date_end = datetime.now()
        date_start = date_end.replace(minute=0, second=0, hour=0, day=1, microsecond=0)
        date_span = datetime.timestamp(date_end) - datetime.timestamp(date_start) / 3600
        query = f"""
        select mean(power) AS Power from {measurement_table}
        where time >= '{date_start}'
        """
        power_level = next(iter(client.query(query)))[0]["Power"]
        usage = power_level * date_span / 1000 # usage in kWh
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
    if request.method == "POST":
        login = json.loads(request.data.decode('utf-8'))['login']
        password = json.loads(request.data.decode('utf-8'))['password']
        hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        with open("users.json", "r") as file:
            users_dict = json.load(file)
        final_result = {}
        if login in users_dict.key():
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
    if request.method == "POST":
        login = json.loads(request.data.decode('utf-8'))['login']
        password = json.loads(request.data.decode('utf-8'))['password']
        hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        with open("users.json", "r") as file:
            users_dict = json.load(file)
        final_result = {}
        if login in users_dict.key():
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
def index():
    return "Hello, IoT"

@app.route("/ip-discovery")
def hello():
    return Response("Hello", status=418, mimetype='application/json')

@app.route('/api/postdata', methods = ['POST'])
def store_data():
    return post_data()

@app.route('/api/readdata', methods = ['POST'])
def read_data():
    return read_data1

@app.route('/api/frontend_req1', methods = ['POST'])
def get_frontend_request():
    return send_answer_to_frontend1()

@app.route('/api/voltage', methods = ['POST'])
def get_frontend_request2():
    return send_answer_to_frontend2()

@app.route('/api/current', methods = ['POST'])
def get_frontend_request3():
    return send_answer_to_frontend3()

@app.route('/api/cost', methods = ['POST'])
def get_frontend_request4():
    return send_answer_to_frontend4()

@app.route('/notification')
def get_frontend_request5():
    return send_answer_to_frontend5()

@app.route("/login", methods=['POST'])
def checklogin():
    return send_answer_to_frontend6()

@app.route("/register", methods=['POST'])
def checklogin():
    return send_answer_to_frontend7()

@app.route("/set-settings", methods=['POST'])
def setSettings():
    with open("settings.json", 'w') as settings:
        settings.write(request.data.decode('utf-8'))
    return jsonify(True)

@app.route("/get-settings")
def getSettings():
    with open("settings.json", 'r') as settings:
        response = settings.read()
    return response

# @app.route("/get-usage", methods=['POST'])
# def getUsage():
#     start = json.loads(request.data.decode('utf-8'))['start']
#     end = json.loads(request.data.decode('utf-8'))['end']
#     new_dict = {}
#     for i in range(0, 8760):
#         if year_data[str(i)]["timestamp"] >= start and year_data[str(i)]["timestamp"] <= end:
#             new_dict[year_data[str(i)]["timestamp"]] = year_data[str(i)]["power"]
#     return jsonify(new_dict)


if __name__ =="__main__":
    host = os.environ.get('IP', '0.0.0.0')
    port = 8080
    app.run(host=host, port=port, debug=True)
