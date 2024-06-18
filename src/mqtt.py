import time
import json
import paho.mqtt.client as mqtt
import requests
import signal
import sys

import logging
from sys import stdout

def setup_logging():
    log = logging.getLogger('logger')
    log.setLevel(logging.DEBUG) # set logger level
    logFormatter = logging.Formatter("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
    consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
    consoleHandler.setFormatter(logFormatter)
    log.addHandler(consoleHandler)
    return log

log = setup_logging()

def load_config():
    try:
        with open("src/config.json") as f:
            cfg = json.load(f)
            log.info("Config loaded")
    except Exception as e:
        log.error("Failed to load config: %s", e)
        sys.exit(1)
    return cfg

cfg = load_config()

def signal_handler(sig, frame):
    log.info("Received signal {}. Exiting...".format(sig))
    mqttc.disconnect()
    mqttc.loop_stop()
    sys.exit(0)

def get_wiser_headers():
    return {
        'SECRET': cfg['wiser_gw_token'],
        'Content-Type': 'application/json;charset=UTF-8',
    }

def get_wiser_data():
    try:
        headers = get_wiser_headers()    
        req = requests.get('http://{}/data/domain/'.format(cfg['wiser_gw_ip']), headers=headers)
        data = req.json()
    except Exception as e:
        log.error(f"Error occurred while retreiving the gateway system data: {e}")
        return {}

    wiser_gw = {}
    if "System" in data:
        log.debug(f"Gateway system data received")
        wiser_gw["mode"] = data["System"].get("OverrideType")
        wiser_gw["connection"] = data["System"].get("CloudConnectionStatus")
        wiser_gw["Room"] = []
        for rooms in req.json()["Room"]:
            if rooms["CalculatedTemperature"] > 0:
                wiser_gw["Room"].append({"id": rooms["id"], "name": rooms["Name"], "temperature": rooms["CalculatedTemperature"]})
            else:
                log.error(f"Error occurred while parsing the gateway room data: {rooms}")
    else:
        log.error(f"Error occurred while parsing the gateway system data: {data}")
    
    return wiser_gw

def set_wiser_home(state):
    headers = get_wiser_headers()    
    payload = {}

    if state == "Away":
        payload = { "type": "Away", "setPoint": cfg['wiser_gw_away_temp'] }
    else:
        payload = { "type": "None", "setPoint": 0 }

    try:
        url = 'http://{}/data/domain/System/RequestOverride'.format(cfg['wiser_gw_ip'])
        req = requests.patch(url, data=json.dumps(payload), headers=headers)
        req.raise_for_status() # Raises a HTTPError if the response was unsuccessful
    except requests.exceptions.RequestException as e:
        log.error(f"Error occurred while setting the home state: {e}")

def on_connect(client, userdata, flags, reason_code, properties):
    log.debug(f"Connected with result code {reason_code}")
    #client.subscribe("$SYS/#")
    client.subscribe("wiser_gw/mode")

def on_message(client, userdata, msg):
    log.info(msg.topic+" "+str(msg.payload))
    if msg.topic == "wiser_gw/mode":
        mode = json.loads(msg.payload.decode())["mode"]
        log.info(f"Setting mode to {mode}")
        set_wiser_home(mode)

def on_publish(client, userdata, mid, reason_code, properties):
    try:
        log.debug(f"mid: {mid} reason_code: {reason_code}")
        userdata.remove(mid)
    except KeyError:
        log.error("on_publish() is called with a mid not present in unacked_publish")

# signal handling
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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

while True:
    wiser_gw = get_wiser_data()

    msg_info = mqttc.publish(cfg["mqtt_broker_topic"], json.dumps(wiser_gw), qos=1)
    unacked_publish.add(msg_info.mid)

    while len(unacked_publish):
        time.sleep(0.1)

    msg_info.wait_for_publish()

    time.sleep(cfg["wiser_gw_refresh"])
