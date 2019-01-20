# Purpose
Make a Python app with two parts:
- A Flask web service to accept television command requests (e.g. volume decrease, volume increase).
- A way to send commands to a transmitter, which then transmits the commands to the television (e.g. via infrared light).
The app may run on a Raspberry Pi with an attached infrared transmitter.

# Results

## endpoints

### GET
e.g. use client browser or curl

    http://10.0.0.4:5000/api/v1/tv/ping/
    http://10.0.0.4:5000/api/v1/tv/status/

### POST
Send a television command
e.g. use curl or iOS app

    http://10.0.0.4:5000/api/v1/tv/volume-decrease/
    http://10.0.0.4:5000/api/v1/tv/volume-increase/

# References

## pi_gpio_service
A simple Python flask web service to read and write Raspberry Pi GPIO.
https://github.com/beepscore/pi_gpio_service

## Remy
Remote control television by sending commands from iOS device to a server.
https://github.com/beepscore/Remy

## Using a Raspberry Pi to end an iPhone phone call
http://beepscore.com/using-raspberry-pi-to-end-iphone-phone-call/

## Serving Raspberry Pi with Flask
http://mattrichardson.com/Raspberry-Pi-Flask/

## Raspberry Pi GPIO API
https://github.com/CorrosiveKid/raspberrypi-gpio-api

## Raspberry Pi Web Server using Flask to Control GPIOs
http://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/

## Build a Python-powered web server with Flask
https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet

## basic_flask
https://github.com/beepscore/basic_flask
https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet
