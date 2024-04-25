import time
import json
import paho.mqtt.client as mqtt
import requests

with open("src/config.json") as f:
    cfg = json.load(f)

def get_wiser_data():
    headers = {
        'SECRET': cfg['wiser_gw_token'],
        'Content-Type': 'application/json;charset=UTF-8',
        }
    req = requests.get('http://{}/data/domain/'.format(cfg['wiser_gw_ip']), headers=headers)

    wiser_gw = {}
    wiser_gw["mode"] = req.json()["System"]["OverrideType"]
    wiser_gw["connection"] = req.json()["System"]["CloudConnectionStatus"]
    wiser_gw["Room"] = []
    for rooms in req.json()["Room"]:
        wiser_gw["Room"].append({"id": rooms["id"], "name": rooms["Name"], "temperature": rooms["CalculatedTemperature"]})
    
    return wiser_gw

def set_wiser_home(state):
    headers = {
        'SECRET': cfg['wiser_gw_token'],
        'Content-Type': 'application/json;charset=UTF-8',
        }
    
    data = {}
    if state == "Away":
        data = { "type": "Away", "setPoint": cfg['wiser_gw_away_temp'] }
    else:
        data = { "type": "None", "setPoint": 0 }

    req = requests.patch('http://{}/data/domain/System/RequestOverride'.format(cfg['wiser_gw_ip']), data=json.dumps(data), headers=headers)
    print(req.text)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    #client.subscribe("$SYS/#")
    client.subscribe("wiser_gw/mode")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "wiser_gw/mode":
        mode = json.loads(msg.payload.decode())["mode"]
        print(f"Setting mode to {mode}")
        set_wiser_home(mode)

def on_publish(client, userdata, mid, reason_code, properties):
    try:
        print(f"mid: {mid} reason_code: {reason_code}")
        userdata.remove(mid)
    except KeyError:
        print("on_publish() is called with a mid not present in unacked_publish")

# mqtt setup
unacked_publish = set()

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.user_data_set(unacked_publish)

mqttc.username_pw_set(cfg["mqtt_broker_user"], cfg["mqtt_broker_pass"])

# mqtt & wiser logic
mqttc.connect(cfg["mqtt_broker_ip"], cfg["mqtt_broker_port"], 60)


mqttc.loop_start()

while(1):
    wiser_gw = get_wiser_data()

    msg_info = mqttc.publish(cfg["mqtt_broker_topic"], json.dumps(wiser_gw), qos=1)
    unacked_publish.add(msg_info.mid)

    while len(unacked_publish):
        time.sleep(0.1)

    msg_info.wait_for_publish()

    time.sleep(cfg["wiser_gw_refresh"])

mqttc.disconnect()
mqttc.loop_stop()