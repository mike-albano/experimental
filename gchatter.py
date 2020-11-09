from httplib2 import Http
import pydig
import json
import sys

#
# From Hangouts Chat incoming webhook quickstart
#
# Edit your URL (get this from webhook in the Chat room settings)
GCHAT_URL = 'https://chat.googleapis.com/v1/spaces/...'

CURRENT_LIST = ['3.11.192.175', '13.52.28.201', '15.206.10.168',
                '52.64.207.242', '13.113.247.134', '35.154.33.182',
                '52.199.251.150', '52.203.51.183', '52.200.63.237',
                '52.8.155.239', '52.29.194.192', '52.58.63.144', '3.106.40.11',
                '52.56.61.130']


def _send_msg(message):
  """Send a message to Google Chat."""
  bot_message = {'text' : message}
  message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
  http_obj = Http()
  url = GCHAT_URL
  response = http_obj.request(
      uri=url,
      method='POST',
      headers=message_headers,
      body=json.dumps(bot_message),
  )


def _find_diff(a_record):
  """Find the difference between existing & new A records."""
  new_list = pydig.query(a_record, 'A')
  ips_removed = set(CURRENT_LIST) - set(new_list)
  ips_added = set(new_list) - set(CURRENT_LIST)
  if ips_removed:
    return ips_removed, 'IPs removed'
  elif ips_added:
    return ips_added, 'IPs added'
  return None, None


def main():
  diff, change_type = _find_diff('redirector.online.spectraguard.net')
  if diff:
    _send_msg('IP Change for Arista redirector\n %s\n %s' % (change_type, diff))


if __name__ == '__main__':
    main()
