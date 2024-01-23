from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

from flask_cors import CORS 
from flask_socketio import SocketIO, emit  


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*") 

# InfluxDB Configuration
token = "DyyA4waY92fqqL4sVcps8EI1_Mb4tKR_6WqfSOYuCy_7cZUUhZW0H_7YubRUYNXbhfs_i7gpOjhiZJs9lcQ0JA=="
org = "iot"
url = "http://localhost:8086"
bucket = "measurements"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

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

def save_to_db(data, verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    if(msg.topic == "topic/alarm"):
        point = (Point("alarm").field("measurement", msg.payload.decode("utf-8")))
        write_api.write(bucket=bucket, org=org, record=point)
        if msg.payload.decode("utf-8") == "on":
            socketio.emit('alarm', "on")
        else :
            socketio.emit('alarm', "off")
    else:
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
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
