"""Play MP3s from running directory on Cast devices/speaker groups.

Requires pychromecast.
"""

import time
import pychromecast
import http.server
import socketserver
import sys
import threading

IP_ADDR = '192.168.0.12'  # Replace w/ your hosts IP.
MP3_1 = 'sample_sound.mp3'  # Replace with your own MP3s.


def start_webserver():
  """Starts a simple webserver on localhost."""
  port = 80
  handler = http.server.SimpleHTTPRequestHandler
  httpd = socketserver.TCPServer(("", port), handler)
  print("serving at port:" + str(port))
  httpd.serve_forever()


def cast_mp3(chromecasts, target_device, mp3):
  """Play an MP3 on CC or Speaker Group."""
  cast = next(cc for cc in chromecasts if cc.device.friendly_name == target_device)
  cast.wait()
  print('setting volume to max')
  cast.set_volume(1)  # Set volume to Max (1)
  time.sleep(2)
  cast.media_controller.play_media('http://{ip}/{mp3_file}'.format(
    ip=IP_ADDR, mp3_file=mp3), 'audio/mp3')
  time.sleep(5)
  print('setting volume back to half')
  cast.set_volume(.5)  # Set volume to middle.


def main():
  threading.Thread(target=start_webserver).start()
  chromecasts = pychromecast.get_chromecasts()
  cast_mp3(chromecasts, 'all_not_livingroom', MP3_1)


if __name__ == '__main__':
  main()
