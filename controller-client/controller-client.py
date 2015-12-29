import websocket
import time

WEBSOCKET_HOST="YOUR_ESP_IP_ADDRESS"
WEBSOCKET_URL="ws://{host}:81".format(WEBSOCKET_HOST)

# ws = websocket.WebSocket()
# ws.connect(WEBSOCKET_URL)

class Color(object):
   def __init__(self, r, g, b):
       self._color = (r,g,b)

def safely_send_colors(colors, retry=0):
  RETRY_SLEEP_SECS = 1
  MAX_RETRIES = 5

  if not _colors_are_valid(colors):
    return

  LEADER="colors:"
  to_send = "{}{}".format(LEADER, _color_list_to_string(colors))
  try:
    ws.send(to_send)
  except Exception, e:
    if retry == MAX_RETRIES:
      print "Failed to send colors."
      raise e
    else:
      print "Failed, retrying #{} after {} seconds".format(retry, RETRY_SLEEP_SECS*retry)
      time.sleep(RETRY_SLEEP_SECS*retry)
      safely_send_colors(colors, retry=retry+1)
      return

def _colors_are_valid(colors):
  NUM_LEDS = 60
  if len(colors) != NUM_LEDS:
    print "Not sending: wrong number of LEDs: {}".format(len(colors))
    return False
  for c in colors:
    if len(c) != 3:
      print "Not sending: invalid color: {}".format(c)
      return False
    for component in c:
      if component < 0 or component > 254:
        print "Not sending: invalid color component: {}".format(component)
        return False
  return True

def _color_list_to_string(colors):
  b_arr = bytearray([])
  for c in colors:
    bytearray.extend(c)
  return str(b_arr)