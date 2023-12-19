from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# InfluxDB Configuration
token = "0U_1-rRg4t59bja0vIqDB6jghIc4vayimVm7nQhrO3NyM11v2gfWH1fVCxHx9VbPKJm2wdhjY380gyWVx_APlg=="
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


def save_to_db(data, verbose=True):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
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
    # Handle the exception and retrieve the exception message using args
        exception_message = str(e)
        print(exception_message)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: save_to_db(json.loads(msg.payload.decode('utf-8')))
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
