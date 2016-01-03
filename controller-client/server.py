from bottle import route, run, template, request, response, hook
import json
import colorsys

from colors import Color, NUM_LEDS, safely_send_colors

# TODO:
# - Retry in case UDP gets dropped.
# - iOS app (uneccessary imho)

ON_STATE = "on"
OFF_STATE = "off"
VALID_STATES = [ON_STATE, OFF_STATE]
STATE_KEY = "state"

HUE_KEY = "hue"
SATURATION_KEY = "saturation"
BRIGHTNESS_KEY = "brightness"

HUE_INDEX = 0
SATURATION_INDEX = 1
BRIGHTNESS_INDEX = 2

# Lights state
current_color_hsb = [0,0,0]
current_state = OFF_STATE

# On/Off state

@route("/state", method=["POST"])
def index():
  global current_state

  params = request.json
  if not params:
    response.status = 400
    return

  new_state = params.get(STATE_KEY, None)
  if new_state in VALID_STATES:
    current_state = new_state

    if current_state == ON_STATE:
      display_current_color()
    else:
      turn_off()

    response.status = 200
  else:
    response.status = 400

@route("/state")
def index():
  global current_state
  response.headers["Content-type"] = "application/json"
  response.status = 200
  return json.dumps({STATE_KEY: current_state})

# Hue
@route("/hue", method=["POST"])
def index():
  global current_state

  params = request.json
  if not params:
    response.status = 400
    return

  new_hue = params.get(HUE_KEY, None)
  if new_hue >= 0 and new_hue <= 360:
    current_color_hsb[HUE_INDEX] = new_hue
    display_current_color()

    response.status = 200
  else:
    response.status = 400

@route("/hue")
def index():
  global current_state
  response.headers["Content-type"] = "application/json"
  response.status = 200
  return json.dumps({HUE_KEY: current_color_hsb[HUE_INDEX]})

# Saturation
@route("/saturation", method=["POST"])
def index():
  global current_state

  params = request.json
  if not params:
    response.status = 400
    return

  new_saturation = params.get(SATURATION_KEY, None)
  if new_saturation >= 0 and new_saturation <= 360:
    current_color_hsb[SATURATION_INDEX] = new_saturation
    display_current_color()

    response.status = 200
  else:
    response.status = 400

@route("/saturation")
def index():
  global current_state
  response.headers["Content-type"] = "application/json"
  response.status = 200
  return json.dumps({SATURATION_KEY: current_color_hsb[SATURATION_INDEX]})

# Saturation
@route("/brightness", method=["POST"])
def index():
  global current_state

  params = request.json
  if not params:
    response.status = 400
    return

  new_brightness = params.get(BRIGHTNESS_KEY, None)
  if new_brightness >= 0 and new_brightness <= 360:
    current_color_hsb[BRIGHTNESS_INDEX] = new_brightness
    display_current_color()

    response.status = 200
  else:
    response.status = 400

@route("/brightness")
def index():
  global current_state
  response.headers["Content-type"] = "application/json"
  response.status = 200
  return json.dumps({BRIGHTNESS_KEY: current_color_hsb[BRIGHTNESS_INDEX]})

# light helpers

def get_current_color_rgb():
  hsb_percents = (current_color_hsb[0]/360.0, current_color_hsb[1]/100.0, current_color_hsb[2]/100.0)
  rgb_percents = colorsys.hsv_to_rgb(*hsb_percents)
  rgb_values = tuple([int(c*254) for c in rgb_percents]) # 0 - 254
  return Color(*rgb_values)

def turn_off():
  display_single_color(Color(0,0,0))

def display_current_color():
  c = get_current_color_rgb()
  MAX_RGB = 30 # Don't burn out the power supply.
  c.r = min(c.r, MAX_RGB)
  c.g = min(c.g, MAX_RGB)
  c.b = min(c.b, MAX_RGB)
  display_single_color(c)

def display_single_color(color):
  colors = [color] * NUM_LEDS
  safely_send_colors(colors)

# Use 0.0.0.0 to listen on localhost and externally.
run(host="0.0.0.0", port=9090)

