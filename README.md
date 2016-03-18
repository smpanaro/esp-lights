Control WS2812b light strip via Wifi.

# Components

## light-controller
An Arduino sketch to be run on the ESP8266 that controls a strip of WS2812b LEDs.
Listens for UDP packets on port 9090 of the form: (bracketed values represent 1 byte)
`colors:\[first LED red value\]\[first LED green value\]\[first LED blue value\]\[second LED red value\][repeat]`

## controller-client
A Python client for converting and sending color lists into UDP packets recognized by the light-controller.
`server.py`: Runs a server on port 9090 that allows get/set of state, hue, saturation and brightness.
`colors.py`: Contains a color class and a method for sending colors to the light strip.
`morning.py`: A script that raises the lights from off to a warm-light for a gradual wake up.

## homebridge-simple-ledstrip
A plugin for homebridge that enables control of the lights.
Install with `sudo npm link` in this folder on the machine running homebridge.

## homebridge
Various configuration files for running homebridge.
`homebridge`: An init.d script to run homebridge on launch.
`config.json`: For configuring homebridge accessories. Place in `~/.homebridge/config.json`.
