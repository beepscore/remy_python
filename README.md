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

## Remy
Remote control television by sending commands from iOS device to a server.
https://github.com/beepscore/Remy

## Flask

### Build a Python-powered web server with Flask
https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet

### basic_flask
https://github.com/beepscore/basic_flask
https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet

## Raspberry Pi
### Using a Raspberry Pi to end an iPhone phone call
http://beepscore.com/using-raspberry-pi-to-end-iphone-phone-call/

### Serving Raspberry Pi with Flask
http://mattrichardson.com/Raspberry-Pi-Flask/

## Remote controls

### LIRC

#### LIRC Linux Infrared Remote Control
http://lirc.org/

#### Raspberry Pi IR Remote Control
2018, uses Go
https://github.com/mtraver/rpi-ir-remote

#### LIRC Debian Stretch Raspberry Pi 2018
https://www.raspberrypi.org/forums/viewtopic.php?t=202375

#### pylirc
https://github.com/project-owner/Peppy.doc/wiki/Pylirc

#### How to get LIRC running on the Raspberry Pi 2017
https://andicelabs.com/2017/11/lirc-raspberry-pi/

#### Setting up a remote control using lirc
https://raspberrypi.stackexchange.com/questions/70945/setting-up-a-remote-control-using-lirc

#### Raspberry Pi IR remote 2015
http://www.raspberry-pi-geek.com/Archive/2015/10/Raspberry-Pi-IR-remote

### Creating A Raspberry Pi Universal Remote With LIRC 2017
https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581

#### Open Source Universal Remote 2013
http://opensourceuniversalremote.com/

##### Open Source Universal Remote - Parts & Pictures
http://alexba.in/blog/2013/06/08/open-source-universal-remote-parts-and-pictures/

##### lirc_node
lirc_node is an npm module that acts as a very thin shim between LIRC and Node.
https://github.com/alexbain/lirc_node

## IR board

### Icstation 38KHz IR Infrared Remote Control Transceiver Shield for Raspberry Pi 2 3 Module B B+ 
https://www.amazon.com/IR-Remote-Control-Transceiver-Raspberry/dp/B0713SK7RJ/ref=pd_cp_147_1?pd_rd_w=nydwe&pf_rd_p=ef4dc990-a9ca-4945-ae0b-f8d549198ed6&pf_rd_r=NPTQR2NR66SZXGEC1CFF&pd_rd_r=dc222ec9-1d1f-11e9-82b3-7117715d74e2&pd_rd_wg=OnVSD&pd_rd_i=B0713SK7RJ&psc=1&refRID=NPTQR2NR66SZXGEC1CFF

### Raspberry Pi IR Control Expansion Board
http://www.raspberrypiwiki.com/index.php/Raspberry_Pi_IR_Control_Expansion_Board

### Raspberry pi 3 B+ 38KHz IR Infrared Remote Expansion Board
https://www.amazon.com/Raspberry-Controller-Transmitter-Transceiver-Geekworm/dp/B076BDR34K

### WINGONEER 38KHz IR Infrared Remote Control Transceiver Shield for Raspberry Pi 2 3 Module B
https://www.amazon.com/WINGONEER-Infrared-Control-Transceiver-Raspberry/dp/B072QWXLK2

### Raspberry Pi Zero Universal Remote 2018
https://www.instructables.com/id/Raspberry-Pi-Zero-Universal-Remote/
#### parts list
- IR LED 5mm (940nm) - TSAL6200 
- 2N2222 NPN transistor 
- r1 10k ohm 1/4 watt
- r2 680 ohm
- r3 36 ohm 1/4 watt

### IR Board for Arduino
SparkFun WiFi IR Blaster (ESP8266)
https://www.sparkfun.com/products/15031
#### software
https://github.com/mdhiggins/ESP8266-HTTP-IR-Blaster

### GPIO

#### pi_gpio_service
A simple Python flask web service to read and write Raspberry Pi GPIO.
https://github.com/beepscore/pi_gpio_service

#### Raspberry Pi GPIO API
https://github.com/CorrosiveKid/raspberrypi-gpio-api

#### Raspberry Pi Web Server using Flask to Control GPIOs
http://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/

