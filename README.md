# Purpose
Make a Raspberry Pi infrared remote control.
The device can programmatically control television sound bar audio volume.
The Raspberry Pi uses LIRC (Linux Infrared Remote Control) to send commands to an attached infrared transmitter.

The Python app has two parts:

- Functions to send commands to the infrared transmitter, which then transmits the commands to the television sound bar
- A Flask web service to accept television command requests (e.g. volume decrease, volume increase).

# Results

## LIRC
Raspberry Pi IR Remote Control https://github.com/mtraver/rpi-ir-remote has helpful up to date suggestions for configuring current versions of LIRC (0.94) and Raspbian (Stretch) and warnings about outdated online info.

    sudo apt-get install lirc
    The following additional packages will be installed:
      libftdi102 liblirc0 python3-yaml
    Suggested packages:
      lirc-compat-remotes lirc-drv-irman lirc-doc lirc-x setserial ir-keytable

Add the following content to /boot/config.txt

    dtoverlay=lirc-rpi,gpio_in_pin=18,gpio_out_pin=17
    
### lirc-compat-remotes (outdated)
This package contains the remote definitions which were part of lirc up to 0.9.0.
    
### lirc-remotes
https://sourceforge.net/projects/lirc-remotes/

LIRC 0.9.4 does not use hardware.conf

https://sourceforge.net/p/lirc/wiki/Drivers/

I copied a lirc configuration file
    pi@raspberrypi:/etc/lirc/lircd.conf.d $ sudo cp ~/beepscore/rpi-ir-remote/config/lirc/cxa_cxc_cxn.lircd.conf .

Ran lirc command irsend

    irsend list cambridge_cxa ""

    000000000000140c KEY_POWER
    000000000000140e KEY_POWER_ON
    000000000000140f KEY_POWER_OFF
    000000000000140d KEY_MUTE
    0000000000001432 KEY_MUTE_ON
    0000000000001433 KEY_MUTE_OFF
    0000000000001410 KEY_VOLUMEUP
    0000000000001411 KEY_VOLUMEDOWN
    
#### execute a lirc command

    irsend SEND_ONCE cambridge_cxa KEY_VOLUMEDOWN

The front facing camera on iPhone doesn't filter IR.
It showed the raspberry pi is lighting the transmit infrared LED.
However the remote configuration cambridge_cxa doesn't work with my Polk receiver.
    
#### Disable incorrect remote configuration files
https://learn.adafruit.com/using-an-ir-remote-with-a-raspberry-pi-media-center/using-other-remotes
lirc looks in .conf.d directory for files ending in .conf
To disable a file change extension from .conf to e.g. .dist

    cd /etc/lirc/lircd.conf.d
    sudo mv devinput.lircd.conf devinput.lircd.dist
    
### irrecord
http://www.lirc.org/html/irrecord.html

lirc-remotes has lots of files, but none named polk.
Could try existing ones but this could be time consuming.
Instead record existing physical remote.

#### error need to stop lirc daemon

    irrecord -d /dev/lirc0 ~/lircd.conf

    Using driver default on device /dev/lirc0
    Could not init hardware (lircd running ? --> close it, check permissions)

##### view running processes

    htop
    ^C

##### stop lirc daemon process by name

    sudo killall -9 lircd

##### irrecord -d didn't work with polk remote, it never got enough info to make a .conf file.

    irrecord -d /dev/lirc0 ~/lircd.conf

##### fix recording failing using option -f --force raw mode

    irrecord -f -d /dev/lirc0 ~/polk.lircd.conf

Enter valid key names e.g. KEY_VOLUMEDOWN

Copied file to /etc/lirc/lircd.conf.d/polk.lircd.conf

### add more keys using option -u --update

    cd /etc/lirc/lircd.conf.d
    irrecord -f -u ./polk.lircd.conf

### list valid key names

    irrecord --list-namespace

## Remote control service

cd to project directory

    cd ~/beepscore/remy_python

If using conda (e.g. via miniconda), activate environment

    source activate beepscore

start Flask web server

    python3 service.py
    * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    * Restarting with stat

Now clients on local network can see the remote control service.

### endpoints

#### GET

    http://10.0.0.4:5000/api/v1/tv/ping/
    
#### POST
Send a remote control command.

    http://10.0.0.4:5000/api/v1/tv/mute/
                        /api/v1/tv/power/
                        /api/v1/tv/voice-decrease/
                        /api/v1/tv/voice-increase/
                        /api/v1/tv/volume-decrease/
                        /api/v1/tv/volume-increase/

### client
GET requests can be made via a browser such as Firefox or mobile Safari
POST requests can be made via terminal curl or POSTMAN or iOS Remy.app

    curl --request POST http://10.0.0.4:5000/api/v1/tv/volume-decrease/
    
### server log
pi terminal shows client's ip address and request info

    10.0.0.3 - - [23/Jan/2019 23:39:22] "POST /api/v1/tv/volume-decrease/ HTTP/1.1" 200 -
    10.0.0.3 - - [23/Jan/2019 23:39:26] "POST /api/v1/tv/volume-increase/ HTTP/1.1" 200 -

## unit tests
Can run tests on macOS by temporarily disabling service.py subprocess.call(irsend)
Not sure how to run tests on pi yet.

    python -m unittest discover

throws RuntimeError: working outside of request context

# References

## Raspberry Pi infrared remote control for a television sound bar
http://beepscore.com/website/2019/02/03/raspberry-pi-infrared-remote-control-tv.html

## Remy
Remote control television by sending commands from iOS device to a server.
https://github.com/beepscore/Remy

## Similar remote control projects

### Raspberry Pi IR Remote Control 2018, uses Go
https://github.com/mtraver/rpi-ir-remote

### LIRC Debian Stretch Raspberry Pi 2018
https://www.raspberrypi.org/forums/viewtopic.php?t=202375

### How to get LIRC running on the Raspberry Pi 2017
https://andicelabs.com/2017/11/lirc-raspberry-pi/

### Setting up a remote control using lirc
https://raspberrypi.stackexchange.com/questions/70945/setting-up-a-remote-control-using-lirc

### Raspberry Pi IR remote 2015
http://www.raspberry-pi-geek.com/Archive/2015/10/Raspberry-Pi-IR-remote

### Creating A Raspberry Pi Universal Remote With LIRC 2017
https://www.hackster.io/austin-stanton/creating-a-raspberry-pi-universal-remote-with-lirc-2fd581

### Open Source Universal Remote 2013
http://opensourceuniversalremote.com/

### Open Source Universal Remote - Parts & Pictures 2013
http://alexba.in/blog/2013/06/08/open-source-universal-remote-parts-and-pictures/

### pylirc
https://github.com/project-owner/Peppy.doc/wiki/Pylirc

### lirc_node
lirc_node is an npm module that acts as a very thin shim between LIRC and Node.
https://github.com/alexbain/lirc_node

## LIRC Linux Infrared Remote Control
http://lirc.org/

## Infrared remote control hardware

### Raspberry Pi IR Control Expansion Board
http://www.raspberrypiwiki.com/index.php/Raspberry_Pi_IR_Control_Expansion_Board

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

### IR Board for Arduino
SparkFun WiFi IR Blaster (ESP8266)
https://www.sparkfun.com/products/15031
#### ir blaster software
https://github.com/mdhiggins/ESP8266-HTTP-IR-Blaster

## Flask

### Build a Python-powered web server with Flask
https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet

### basic_flask
https://github.com/beepscore/basic_flask
https://www.raspberrypi.org/learning/python-web-server-with-flask/worksheet

### Serving Raspberry Pi with Flask
http://mattrichardson.com/Raspberry-Pi-Flask/

### Using a Raspberry Pi to end an iPhone phone call
http://beepscore.com/using-raspberry-pi-to-end-iphone-phone-call/

## Raspberry Pi GPIO projects

#### pi_gpio_service
A simple Python flask web service to read and write Raspberry Pi GPIO.
https://github.com/beepscore/pi_gpio_service

#### Raspberry Pi GPIO API
https://github.com/CorrosiveKid/raspberrypi-gpio-api

#### Raspberry Pi Web Server using Flask to Control GPIOs
http://randomnerdtutorials.com/raspberry-pi-web-server-using-flask-to-control-gpios/

