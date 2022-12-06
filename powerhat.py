import time
import math
import board
import random
import json
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from paho.mqtt import client as mqtt_client
import requests
import netifaces
import sys

# Set SENDER to mqtt in order to use MQTT protocol
# or set it to http to use HTTP protocol

SENDER = 'mqtt'
# SENDER = 'http'

# MASTER_RB_IP='192.168.30.12'
MASTER_RB_IP=None
CHECK_ENDPOINT = ':8080/ip-discovery'

def ip2int(ip):
    parts = ip.split('.')

    ret = 0

    for p in parts:
        ret <<= 8
        ret |= int(p)

    return ret

def int2ip(i):
    parts = []
    while i > 0:
        parts += [str(
            i & 0xff
        )]

        i >>= 8
    return '.'.join(reversed(parts))

def checkIp(ipStr, timeout):
    # print("checkIp", ipStr)

    try:
        r = requests.get(
            'http://' + ipStr + CHECK_ENDPOINT,
            stream=True,
            timeout=timeout
        )
        ipOfResponse = r.raw._original_response.fp.raw._sock.getpeername()[0]

        return r.status_code == 418
    except Exception:
        return False

def findMasterRBIp():
    timeouts = [
        0.1,
        1,
        3,
        10
    ]

    for timeout in timeouts:
        for iface in netifaces.interfaces()[::-1]:
            iface_details = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in iface_details:
                for data in iface_details[netifaces.AF_INET]:
                    ip = data['addr']
                    mask = data['netmask']

                    if ip == '127.0.0.1':
                        continue
                    ip = ip2int(ip)
                    mask = ip2int(mask)

                    networkIp = ip & mask
                    ipsInNetwork = ip2int('255.255.255.255') - mask
                    startIp = networkIp + 1
                    endIp = networkIp + ipsInNetwork

                    print("Trying IPs from", int2ip(startIp), 'to', int2ip(endIp))

                    for tryIp in range(startIp, endIp + 1):
                        if checkIp(int2ip(tryIp), timeout):
                            return int2ip(tryIp)
    return None


class MqttSender:
    def __init__(self, brokerIp = MASTER_RB_IP):
        self.broker = brokerIp
        self.port = 1883
        self.topic = "power-hat"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

        self.client = None
        self.__started = False

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

    def publish(self, msg):
        if self.client is None:
            self.__connect_mqtt()

        if self.client is None:
            print("Warning: client is None. Not publishing!")
            return

        result = self.client.publish(self.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")

    def send(self, msg):
        self.publish(msg)

    def sendJson(self, jsonData):
        self.publish(json.dumps(jsonData))

    def connect(self):
        self.__connect_mqtt()
        self.client.loop_start()

class HttpSender:
    def __init__(self, ip = MASTER_RB_IP, port = '8080'):
        self.url = "http://" + ip + ":" + port + "/api/postdata"

    def connect(self):
        pass

    def sendJson(self, jsonData):
        #self.publish(json.dumps(jsonData))
        #self.client.loop_start()
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(self.url, data=json.dumps(jsonData), headers=headers)

if __name__ == '__main__':
    if MASTER_RB_IP is None:
        MASTER_RB_IP = findMasterRBIp()
        print("Found Master RaspberryPi IP:", MASTER_RB_IP)
    


    if SENDER == 'http':
        httpSender = HttpSender()
    else:
        mqttSender = MqttSender()
        mqttSender.connect()

    i2c_bus = board.I2C()
    ina4 = INA219(i2c_bus,addr=0x43)
    ina4.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina4.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina4.bus_voltage_range = BusVoltageRange.RANGE_16V

    while True:
        dump = {}
        t_end = time.time() + (10)
        counter = 0
	
        while time.time() < t_end:
   	 
            voltage4 = ina4.bus_voltage + (ina4.shunt_voltage /1000)  
            current4 = ina4.current
            power4 = ina4.power
            timestamp = time.time()

            print("Voltage:{:6.3f}V    Current:{:9.6f}A    Power:{:9.6f}W".format((voltage4),(current4/100000),(power4)))
            print("")
   	 
            dump[str(counter)] = {'timestamp': timestamp, 'voltage': voltage4, 'current': current4, 'power': power4}

            counter += 1
            p1 = time.time()
            p2 = (p1 - (p1 % 0.1)) +0.1 
            time.sleep(p2 - p1)
	
        if SENDER == 'http':
            httpSender.sendJson(dump)
        else:
            mqttSender.sendJson(dump)
