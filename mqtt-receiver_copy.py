import random
import time
import json
from influxdb import InfluxDBClient
from datetime import datetime
from paho.mqtt import client as mqtt_client


class MqttReceiver:
    def __init__(self, brokerIp = '0.0.0.0', onMessage = None):
        self.broker = brokerIp
        self.port = 1883
        self.topic = "power-hat"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

        self.client = None
        self.__started = False

        self.__onMessage = onMessage
    
    def onReceiveJson(self, onReceiveJsonFunction):
        if not callable(onReceiveJsonFunction):
            print("onReceiveJsonFunction is not callable! Please specify function.")
            return

        def on_message_json(client, userdata, msg):
            jsonDataStr = msg.payload.decode()
            jsonData = json.loads(jsonDataStr)

            onReceiveJsonFunction(jsonData)
        
        self.__onMessage = on_message_json

    def __connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        
        # Set Connecting Client ID
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

    def __subscribe(self):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        if self.client is not None:
            self.client.subscribe(self.topic)

            if self.__onMessage is None:
                self.client.on_message = on_message
            else:
                self.client.on_message = self.__onMessage
            
            return True
        else:
            return False

    def start(self):
        if self.__started:
            return
        
        self.__connect_mqtt()
        self.__subscribe()

        self.__started = True
    
    def loop(self):
        if not self.__started:
            self.start()
        
        self.client.loop_forever()



if __name__ == '__main__':
    def onReceiveJsonFunction(jsonData):
        print(jsonData)
        client = InfluxDBClient('localhost', "8086", 'backend', 'backend', 'mydb')
        list_of_data = []
        for key in jsonData.keys():
            temp = jsonData[key]
            sample = {
                "measurement": "measurement2",
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
        print("poszlo")
        
    
    mqttReceiver = MqttReceiver()
    mqttReceiver.onReceiveJson(onReceiveJsonFunction)
    mqttReceiver.loop()
