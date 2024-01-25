from distutils.cmd import Command
from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import schedule
import time
import threading
from flask_cors import CORS 
from flask_socketio import SocketIO, emit  

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# InfluxDB Configuration
#token = "94qWOH0wxeFMQxAUp3DfcQXeGURIIl5KudjZZdWC5bQcWTEniZyUib2vm8isbktznjpyF_PhK_7-McGoG0dW2A=="
token = "DyyA4waY92fqqL4sVcps8EI1_Mb4tKR_6WqfSOYuCy_7cZUUhZW0H_7YubRUYNXbhfs_i7gpOjhiZJs9lcQ0JA=="
org = "iot"
url = "http://localhost:8086"
bucket = "measurements"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)
clock = False
mqtt_client = mqtt.Client()

def on_connect(client: mqtt.Client, userdata: any, flags, result_code):
    print("Connected with result code " + str(result_code))
    client.subscribe("topic/db/buzz")
    client.subscribe("topic/dht/temperature")
    client.subscribe("topic/dht/humidity")
    client.subscribe("topic/dl/light")
    client.subscribe("topic/ds/button")
    client.subscribe("topic/uds/distance")
    client.subscribe("topic/ms/keypressed")
    client.subscribe("topic/pir/movement")
    client.subscribe("topic/b4sd/segment")
    client.subscribe("topic/alarm")
    client.subscribe("topic/gyro/acceleration")    #ubrzanje
    client.subscribe("topic/gyro/rotation")    # rotacija
    client.subscribe("topic/rgb/light")
    client.subscribe("topic/ir/hue")
    client.subscribe("topic/db/clock")

def save_to_db(message, verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if(message.topic == "topic/alarm"):
        point = (Point("alarm").field("measurement", message.payload.decode("utf-8")))
        write_api.write(bucket=bucket, org=org, record=point)
        if message.payload.decode("utf-8") == "on":
            socketio.emit('alarm', "on")
        else :
            socketio.emit('alarm', "off")
    elif(message.topic == "topic/db/clock"):
        if message.payload.decode("utf-8") == "clockOn":
            socketio.emit("alarmClock", "clockOn")
        else:
            socketio.emit("alarmClock", "clockOff")

    elif(message.topic == "topic/gyro/rotation"):
        data = json.loads(message.payload.decode('utf-8'))
        try:
            point = (
                Point(data["measurement"])
                .tag("simulated", data["simulated"])
                .tag("runs_on", data["runs_on"])
                .tag("name", data["name"])
                .field("x", data["rotation_x"])
                .field("y", data["rotation_x"])
                .field("z", data["rotation_x"])
            )
            print(point)
            write_api.write(bucket, org=org, record=point)
            if verbose:
                print("Got message: " + json.dumps(data))
        except Exception as e:
            exception_message = str(e)
            print(exception_message)

    elif(message.topic == "topic/gyro/acceleration"):
        data = json.loads(message.payload.decode('utf-8'))
        try:
            point = (
                Point(data["measurement"])
                .tag("simulated", data["simulated"])
                .tag("runs_on", data["runs_on"])
                .tag("name", data["name"])
                .field("x", data["acceleration_x"])
                .field("y", data["acceleration_x"])
                .field("z", data["acceleration_x"])
            )
            print(point)
            write_api.write(bucket, org=org, record=point)
            if verbose:
                print("Got message: " + json.dumps(data))
        except Exception as e:
            exception_message = str(e)
            print(exception_message)
    else:
        data = json.loads(message.payload.decode('utf-8'))
        try:
            point = (
                Point(data["measurement"])
                .tag("simulated", data["simulated"])
                .tag("runs_on", data["runs_on"])
                .tag("name", data["name"])
                .field("measurement", data["value"])
            )
            print(point)
            write_api.write(bucket, org=org, record=point)
            if verbose:
                print("Got message: " + json.dumps(data))
        except Exception as e:
            exception_message = str(e)
            print(exception_message)  

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(msg)
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/alarm', methods=['GET'])
def alarm_off():
    try:
        mqtt_client.publish("topic/alarm", "off")
        socketio.emit('alarm', "off")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/rgb', methods=['POST'])
def set_rgb_mode():
    try:
        data = request.get_json()
        mode = data.get('mode')
        mqtt_client.publish("topic/rgb", mode)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1) 
        global clock
        if clock:
	        break  
        

def alarm_clock_scheduled(command):
    mqtt_client.publish("topic/db/clock", command)
    global clock
    clock = True

@app.route('/addAlarmClock', methods=['POST'])
def set_alarm_clock():
    try:
        data = request.get_json()
        time = data.get('req')
        alarm_time = datetime.strptime(time, '%H:%M')
        command = "clockOn"
        global clock
        clock = False
        schedule.every().day.at(alarm_time.strftime('%H:%M')).do(alarm_clock_scheduled, command)
        threading.Thread(target=run_scheduled_tasks).start()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/alarmClockOff', methods=['GET'])
def alarm_clock_off():
    try:
        command = "clockOff"
        mqtt_client.publish("topic/db/clock", command)
        socketio.emit('alarmClock', "clockOff")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
