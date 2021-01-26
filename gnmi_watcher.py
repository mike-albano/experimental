"""Simple utility to watch gNMI output and ping gChat if condition."""

import json
import subprocess
import sys
import time
from httplib2 import Http

# The following is the gChat WebHook URL.
_GCHAT_URL = ''

def get_radiostats():
  raw_data = None
  while raw_data is None:
    try:
      raw_data = subprocess.check_output(['python3', 'py_gnmicli.py', '-t', '192.168.0.55', '-p', '8080', '-m', 'get', '-x', '/access-points/access-point[hostname=foo]/radios/radio[id=0][operating-frequency=FREQ_5GHZ]/state/dfs-hit-time', '-pass', 'admin', '-user', 'admin', '-o', 'openconfig.mojonetworks.com', '-g'])
    except:
      print('gNMI GetRequest failed.')
      pass
      time.sleep(5)  # If HTTP Request fails, wait 5s and try again.

  return raw_data

def _send_msg(message):
  """Send a message to Google Chat.

  Args:
    message: (str) Message to send to gChat
  """
  bot_message = {'text': message}
  message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
  http_obj = Http()
  url = _GCHAT_URL
  http_obj.request(
      uri=url,
      method='POST',
      headers=message_headers,
      body=json.dumps(bot_message),
      )


def main():
  while True:
    stats = get_radiostats()
    if '1611669605' not in str(stats):
      _send_msg('DFS Hit Occurred')
      sys.exit()
    time.sleep(5)


if __name__ == '__main__':
  main()
