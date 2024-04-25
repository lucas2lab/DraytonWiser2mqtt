# Daytonawiser2mqtt

## Introduction
Daytonawiser2mqtt is a Python-based service designed to establish a bidirectional communication link between a local Wiser gateway and an MQTT broker. It enables the publishing of temperature data and the sending of commands to and from the Wiser heating system. This project utilizes Docker for easy deployment and management.

## Features
- **Bidirectional Communication:** Send and receive commands between Wiser gateway and MQTT.
- **Temperature Publishing:** Automatically publish temperature readings to MQTT.
- **Away mode Command:** Send command to control away and home mode.
- **Docker Support:** Run as a container for easy setup and scalability.

## Prerequisites
Before you begin, ensure you have Docker installed on your system. You can download it from [Docker's official website](https://www.docker.com/get-started).

## Installation

### Using Docker

1. Clone this repository

```
to do
```
   
2. Build the Docker image:

```
to do
```

3. Run the Docker container:

```
to do
```

## Usage

To start using Daytonawiser2mqtt, configure your MQTT broker details and Wiser gateway settings in the configuration file (config.ini). Here's an example of how to set it up:

```
[mqtt]
broker = your.mqtt.broker.ip
port = 1883
username = yourusername
password = yourpassword

[wiser]
host = your.wiser.gateway.ip
secret = yoursecretkey
```

After setting up your configuration, restart the Docker container to apply changes:

```
docker restart daytonawiser2mqtt
```

## Libraries Used

* Paho MQTT Python: For interacting with MQTT brokers.
* Wiser Heating API: For interfacing with the Wiser Heating system.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

##Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

## License

To be defined

##Acknowledgements

* Paho MQTT Python
* Wiser Heating API

## ToDo

* [ ] Complete and extend this Readme
* [ ] Implement best practice https://testdriven.io/blog/docker-best-practices/#run-only-one-process-per-container
