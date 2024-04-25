# Daytonawiser2mqtt

## Introduction

Daytonawiser2mqtt is a Python-based service designed to establish a bidirectional communication link between a local Wiser gateway and an MQTT broker. It enables the publishing of temperature data and the sending of commands to and from the Wiser heating system. This project utilizes Docker for easy deployment and management.

## Features

- **Temperature Publishing:** Automatically publish temperature readings to MQTT.
- **Away mode Command:** Send command to control away and home mode.
- **Docker Support:** Run as a container for easy setup and scalability.

## Prerequisites

The script can run with python or docker.

Before you begin, ensure you have Docker installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

## Installation

### Setup the service using the config.json

To start using Daytonawiser2mqtt, configure your MQTT broker details and Wiser gateway settings in the configuration file (config.json). You can do so by renaming the config.json.example file and editing your configuration:

```
{
    "wiser_gw_ip"        : "1.1.1.1",
    "wiser_gw_token"     : "aaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccccccccccccccdddddddddddddddddddddddddd",
    "wiser_gw_away_temp" : 150,

    "mqtt_broker_ip"     : "1.1.1.2",
    "mqtt_broker_port"   : 1883,
    "mqtt_broker_user"   : "username",
    "mqtt_broker_pass"   : "password",
    "mqtt_broker_topic"  : "wiser_gw"
}
```

After setting up your configuration run it following the python or docker instructions.

### Using Python

```
pip install --no-cache-dir -r requirements.txt
cd src
python mqtt.py
```

### Using Docker

1. Build the Docker image:

```
docker build -t wiser2mqtt .
```

2. Run the Docker container:

```
docker run -d wiser2mqtt
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

##Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

## License

BSD 3-Clause License

## Acknowledgements

* Wiser Heating API https://github.com/asantaga/wiserheatingapi for the endpoints to call on the wiser gateway
* Paho MQTT Python https://github.com/eclipse/paho.mqtt.python 

## ToDo

* [x] Complete and extend this Readme
* [ ] Implement best practice https://testdriven.io/blog/docker-best-practices/#run-only-one-process-per-container
* [ ] Add TRV management
* [ ] Add light switch management
* [ ] Add shutters swictch management
