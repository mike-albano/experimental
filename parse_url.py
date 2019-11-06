"""
Simple script to login to a web page and scrape data.

See "<form" on the login page to determine what the url is
to pass to get_url func.
See "<input name" to determine what the user/password keys
should be for the CREDS.
The particular example used in this script is for a CenturyLink
ZYXEL C3000Z NAT table.
"""

import os
import requests
import time

CREDS = {'admin_username': 'admin', 'admin_password': 'change_me'}

def login(url):
  """Do a POST to login first (if required)

  Args:
    url: (str) of the URL used for Login.
  Returns: (class) Requsts response.
  """
  with requests.Session() as session:
    session.post(url, data=CREDS)
  return session

def get_url(session, url):
  """Get HTML after logging in.

  Args:
    session: (class) Requests session.
    url: (str) URL with the data we want to analyze.
  Returns: (str) HTML data.
  """
  return session.get(url).text

def parse_url(data):
  """Parse the HTML data for what we're interested in."""
  lines = data.split('\n')  # Turn HTML string into list of lines.
  for line in lines:
    if 'getnatTable' in line:
      line_of_interest = line
      break  # Stop looking for our string
  nat_table = line_of_interest.split('\'')[1].split('|')  # Further process the string
  return nat_table

def format_results(parsed_data):
  """Print, write etc."""
  named_tuple = time.localtime() # get struct_time
  time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
  print(time_string)
  print('PROTO' + '|' + 'TIMEOUT' + '|' + 'SourceIP' + '|' + 'SourcePort' +
        '|' + 'DestIP' + '|' + 'DestPort')
  for entry in parsed_data:
    print(entry)

if __name__ == '__main__':
  session = login('http://192.168.86.1/login.cgi')
  while True:  # Remove this while loop to only do it once.
    data = get_url(session, 'http://192.168.86.1/modemstatus_nattable.html')
    parsed_data = parse_url(data)
    format_results(parsed_data)
    time.sleep(8)
