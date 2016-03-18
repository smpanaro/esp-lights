import socket
import time
import sys
import colorsys

LIGHT_IP = "YOUR_ESP_IP_ADDRESS"
LIGHT_PORT = 9090
NUM_LEDS = 60 # Used for validation.

class Color(object):
  def __init__(self, r, g, b):
    self._color = (r,g,b)
    self.r = r
    self.g = g
    self.b = b

  @classmethod
  def from_hsv(cls, h,s,v):
    hsv_percents = (h/360.0, s/100.0, v/100.0)
    rgb_percents = colorsys.hsv_to_rgb(*hsv_percents)
    rgb_values = tuple([int(c*254) for c in rgb_percents]) # 0 - 254
    return cls(*rgb_values)

  def __len__(self):
    return len(self._color)

  def __iter__(self):
    for c in self._color:
      yield c

def safely_send_colors(colors):
  if not _colors_are_valid(colors):
    return

  _dangerously_send_colors(colors)

def _dangerously_send_colors(colors):
  LEADER="colors:"
  message = "{}{}".format(LEADER, _color_list_to_string(colors))

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(message, (LIGHT_IP, LIGHT_PORT))

def _colors_are_valid(colors):
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
    b_arr.append(c.r)
    b_arr.append(c.g)
    b_arr.append(c.b)
  return str(b_arr)

if __name__ == '__main__':
  colors = []

  arg = sys.argv[1] if len(sys.argv) > 1 else None

  if arg == "--bad-packet":
    for _ in range (0, 2):
      colors.append(Color(10,10,10))
      _dangerously_send_colors(colors)
  elif arg == "--red":
    for _ in range(0, NUM_LEDS):
      colors.append(Color(30,0,0))
    safely_send_colors(colors)
  elif arg == "--green":
    for _ in range(0, NUM_LEDS):
      colors.append(Color(0,30,0))
    safely_send_colors(colors)
  elif arg == "--blue":
    for _ in range(0, NUM_LEDS):
      colors.append(Color(0,0,30))
    safely_send_colors(colors)
  elif arg == "--white":
    for _ in range(0, NUM_LEDS):
      colors.append(Color(30,30,30))
    safely_send_colors(colors)