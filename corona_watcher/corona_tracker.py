""" Python3 tracker script to alert when number of positive
cases increases in your state.
"""

import datetime
import json
import os
import time
import requests
import sys


if len(sys.argv) < 2:
  print('USAGE:\npython corona_tracker.py <state_code_here>')
my_state = sys.argv[1]

def get_data(my_state):
  """Get the raw data from API."""
  raw_data = None
  while raw_data is None:
    try:
      raw_data = json.loads(requests.get( # Get the list of dicts
        'https://covidtracking.com/api/states').text)
    except:
      pass
      time.sleep(5)  # If HTTP Request fails, wait 5s and try again.

  return next(state for state in raw_data if state['state'] == my_state)


def parse_data(state_data, initial_posnum, initial_negnum, initial_deathnum):
  """Detrmine if reported cases has increased."""
  new_positive = False
  new_negative = False
  new_death = False
  new_posnum = state_data['positive']
  new_negnum = state_data['positive']
  new_deathnum = state_data['death']
  if new_posnum > initial_posnum:
    new_positive = True
  if new_negnum > initial_negnum:
    new_negative = True
  if new_deathnum > initial_deathnum:
    new_death = True

  if new_positive:
    print('Increase in positive cases.\nOld num: %i\nNew number: %i'
          % (initial_posnum, new_posnum))
    # Comment in this line to play a souond (Works on OSX only)
    # os.popen('open pos-sound.mp3')
  if new_negative:
    print('Increase in negative cases.\nOld num: %i\nNew number: %i'
          % (initial_negnum, new_negnum))
    # Comment in this line to play a souond (Works on OSX only)
    # os.popen('open neg-sound.mp3')
  if new_death:
    print('Increase in number of deaths..\nOld num: %i\nNew number: %i'
          % (initial_deathnum, new_deathnum))
    # Comment in this line to play a souond (Works on OSX only)
    # os.popen('open death-sound.mp3')

  if not new_positive and not new_negative and not new_death:
    print('No change as of: %s. The current numbers are still:\n%i positve'
          '\n%i negative\n%i deaths'
          % (datetime.datetime.now().strftime("%D:%H:%M:%S"), initial_posnum,
             initial_negnum, initial_deathnum))


if __name__ == '__main__':
  state_data = get_data(my_state.upper())  # Argument passed in.
  initial_posnum = state_data['positive']
  initial_negnum = state_data['negative']
  initial_deathnum = state_data['death']
  print('Starting number of positive cases is: %i' % initial_posnum)
  print('Starting number of negative cases is: %i' % initial_negnum)
  print('Starting number of deaths is: %i' % initial_deathnum)
  while True:
    time.sleep(300)  # Perform the check every 5m
    state_data = get_data(my_state.upper())  # Argument passed in.
    parse_data(state_data, initial_posnum, initial_negnum, initial_deathnum)
    initial_posnum = state_data['positive']  # Set new initial number.
    initial_negnum = state_data['negative']  # Set new negative number.
    initial_deathnum = state_data['death']  # Set new death number.
