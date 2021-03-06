print("Smart Car")
import paho.mqtt.client as mqttclient
import time
import json
import winrt.windows.devices.geolocation as wdg, asyncio

async def getCoords():
    loc = wdg.Geolocator()
    pos = await loc.get_geoposition_async()
    return [pos.coordinate.latitude, pos.coordinate.longitude]
def getLoc():
    return asyncio.run(getCoords())

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "JQR04ZL00AVOPdhep1v5"


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)

client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()

client.on_subscribe = subscribed
client.on_message = recv_message

speed = 30
petrol= 100

counter = 0
while True:
    latitude = getLoc()[0]
    longitude = getLoc()[1]
    collect_data = {'speed': speed, 'petrol': petrol,'latitude': latitude,'longitude': longitude}
    speed += 1
    petrol -= 1
    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(10)