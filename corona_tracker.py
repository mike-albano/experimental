""" Python3 tracker script to alert when number of positive
cases increases in your state.
"""

import datetime
import json
import time
import requests
import sys


if len(sys.argv) < 2:
  print('USAGE:\npython corona_tracker.py <your_state_here>')
my_state = sys.argv[1]

def get_data(my_state):
  """Get the raw data from API."""
  raw_data = json.loads(requests.get( # Get the list of dicts
    'https://covidtracking.com/api/states').text)
  return next(state for state in raw_data if state['state'] == my_state)


def parse_data(state_data, initial_num):
  """Detrmine if reported cases has increased."""
  new_num = state_data['positive']
  if new_num > initial_num:
    print('Increase in positive cases.\nOld num: %i\nNew number: %i'
          % (initial_num, new_num))
    print('Number of deaths: %i' % state_data['death'])
  else:
    print('No change as of: %s. The current number is still %i'
          % (datetime.datetime.now().strftime("%D:%H:%M:%S"), initial_num))


if __name__ == '__main__':
  state_data = get_data(my_state.upper())  # Argument passed in.
  initial_num = state_data['positive']
  print('The starting number of positive cases is %i: ' % initial_num)
  while True:
    time.sleep(60)  # Perform the check every 60s
    state_data = get_data(my_state.upper())  # Argument passed in.
    parse_data(state_data, initial_num)
    initial_num = state_data['positive']  # Set new initial number.
