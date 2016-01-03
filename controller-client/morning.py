import time
import urllib2
import json

# Example cron command to run every weekday at 7:50AM
# 50 7 * * 1-5 /usr/bin/python /path/to/morning.py

start_hsv = (33, 12, 0)
end_hsv = (33, 12, 100)

LIGHT_SERVER_URL = "http://localhost:9090"

# Go via the server to keep state in one place.
def display_color(h,s,v):
  display_hue(h)
  display_saturation(s)
  display_value(v)

def display_hue(h):
  req = urllib2.Request("{}/hue".format(LIGHT_SERVER_URL))
  req.add_header('Content-Type', 'application/json')
  data = {"hue": h}
  response = urllib2.urlopen(req, json.dumps(data))

def display_saturation(s):
  req = urllib2.Request("{}/saturation".format(LIGHT_SERVER_URL))
  req.add_header('Content-Type', 'application/json')
  data = {"saturation": s}
  response = urllib2.urlopen(req, json.dumps(data))

def display_value(v):
  req = urllib2.Request("{}/brightness".format(LIGHT_SERVER_URL))
  req.add_header('Content-Type', 'application/json')
  data = {"brightness": v}
  response = urllib2.urlopen(req, json.dumps(data))

# state: "on" or "off"
def set_state(state):
  if state not in ["on", "off"]:
    print "Invalid state: {}".format(state)
    return

  req = urllib2.Request("{}/state".format(LIGHT_SERVER_URL))
  req.add_header('Content-Type', 'application/json')

  data = {"state": state}
  response = urllib2.urlopen(req, json.dumps(data))

def should_run():
  try:
    urllib2.urlopen("{}/state".format(LIGHT_SERVER_URL))
  except :
    return False

  return True

def run():
  # Time to go from the start color to the end color.
  TRANSITION_TIME_SECS = 5*60

  num_steps = end_hsv[2] - start_hsv[2]
  step_duration = float(TRANSITION_TIME_SECS) / float(num_steps)

  set_state("on")

  current_hsv = start_hsv
  while current_hsv[2] <= end_hsv[2]:
    display_color(*current_hsv)
    time.sleep(step_duration)
    h,s,v = current_hsv
    current_hsv = (h,s,v+1)

if __name__ == '__main__':
  if should_run():
    run()




