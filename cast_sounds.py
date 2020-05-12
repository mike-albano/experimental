"""Play MP3s from running directory on Cast devices/speaker groups.

Requires pychromecast.
"""

import argparse
import time
import datetime
import pychromecast
import http.server
import socketserver
import sys
import threading

IP_ADDR = '192.168.0.12'  # Replace w/ your hosts IP.
MP3_1 = 'sample_sound.mp3'  # Replace with your own MP3s.

def _create_parser():
  """Create parser for arguments passed into the program from the CLI.
  Returns:
    Argparse object.
  """
  parser = argparse.ArgumentParser(description='Cast to cast-capable devices')
  parser = argparse.ArgumentParser(formatter_class=argparse.
                                   RawDescriptionHelpFormatter,epilog='Use this'
                                   ' to cast MP3 files to Cast devices such as'
                                   'Chromecasts, Google Homes, Nest Home etc.'
                                   'EXAMPLE\n'
                                   'python3 cast_sounds.py -s -u http://192.168.0.12/sample_sound.mp3 -c "Game Room speaker" -v 9 -rv .5')
  parser.add_argument('-u', '--url', type=str, help='URL to the hosted MP3',
                      required=True)
  parser.add_argument('-c', '--cast_name', type=str, help='Name of the Cast device'
                      'to play on. Can be speaker-group as well', required=True)
  parser.add_argument('-s', '--serve', help='Run a local webserver for'
                      'serving up MP3 files.', action='store_true')
  parser.add_argument('-v', '--volume', type=str, help='Cast Volume for playing (0..1)',
                      required=False)
  parser.add_argument('-rv', '--return_volume', type=str, help='Cast Volume to'
                      'set the device(s) back to after playing (0..1)', required=False)

  return parser


def start_webserver():
  """Starts a simple webserver on localhost."""
  port = 80
  handler = http.server.SimpleHTTPRequestHandler
  httpd = socketserver.TCPServer(("", port), handler)
  print("serving at port:" + str(port) + '\nCtrl-c to quit.')
  httpd.serve_forever()


def cast_mp3(chromecasts, target_device, mp3_url, initial_volume, return_volume):
  """Play an MP3 on CC or Speaker Group."""
  cast = next(cc for cc in chromecasts if cc.device.friendly_name == target_device)
  cast.wait()
  if initial_volume:
    print('setting initial volume.')
    cast.set_volume(1)  # Set volume to Max (1)
  time.sleep(2)
  cast.media_controller.play_media(mp3_url, 'audio/mp3')
  #time.sleep(5)
  if return_volume:
    print('setting return volume.')
    cast.set_volume(.5)  # Set volume to middle.

  return cast


def main():
  argparser = _create_parser()
  args = vars(argparser.parse_args())
  # Assign variables to the arguments provided
  mp3_url = args['url']
  cast_name = args['cast_name']
  initial_volume = args['volume']
  return_volume = args['return_volume']
  #serve = args['serve']
  if args['serve']:  # Start a local webserver for serving MP3s
    threading.Thread(target=start_webserver).start()
  chromecasts = pychromecast.get_chromecasts()
  cast = cast_mp3(chromecasts, cast_name, mp3_url, initial_volume, return_volume)
  if cast.media_controller.status.player_state == 'IDLE':
    # Kill the thread
    cast.quit_app()
    sys.exit()


if __name__ == '__main__':
  main()
