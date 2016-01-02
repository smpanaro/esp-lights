from bottle import route, run, template, request, response, hook
import json
from colors import Color, NUM_LEDS, safely_send_colors

current_color = {
  "h":0,
  "s":0,
  "b":0
}
current_state = OFF_STATE

ON_STATE = "on"
OFF_STATE = "off"
VALID_STATES = [ON_STATE, OFF_STATE]
STATE_KEY = "state"

# Called from the website to submit a new lighting configuration.
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

# Called from the light_client to get the current configuration.
@route("/state")
def index():
  global current_state
  response.headers["Content-type"] = "application/json"
  response.status = 200
  return json.dumps({STATE_KEY: current_state})

# light helpers

def turn_off():
  display_single_color(Color(0,0,0))

def display_current_color():
  display_single_color(Color(30,0,0))

def display_single_color(color):
  colors = [color] * NUM_LEDS
  safely_send_colors(colors)

# Use 0.0.0.0 to listen on localhost and externally.
run(host="0.0.0.0", port=9090)

