Control WS2812b light strip via Wifi.

# Components

## light-controller
An Arduino sketch to be run on the ESP8266 that controls a strip of WS2812b LEDs.
Listens for UDP packets on port 9090 of the form: (bracketed values represent 1 byte)
colors:\[first LED red value\]\[first LED green value\]\[first LED blue value\]\[second LED red value\][repeat]

## controller-client
A Python client for converting and sending color lists into UDP packets recognized by the light-controller.