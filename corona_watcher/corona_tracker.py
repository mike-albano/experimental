""" Python3 tracker script to alert when number of positive
cases increases in your country & state.
"""

import datetime
import json
import os
import time
import requests
import sys
from playsound import playsound
from gtts import gTTS
import urllib3
urllib3.disable_warnings()  # Don't care much for cert validity here.


OFF_HOURS = ['23', '00', '01', '02', '03', '04', '05', '06', '07', '08']

# (TODO): Replace with argparse
if len(sys.argv) < 2:
  print('USAGE:\npython corona_tracker.py <state_code_here> <country_code_here')
my_state = sys.argv[1]  # Two letter state code (eg CO)
my_country = sys.argv[2]  # Three letter country designation (eg USA)

class StatsObject(object):
  """ Represents a stats objects for storing data results.

  Attributes:
    stats: data of interest; state, country, etc.
    initial_num: Initial number per stat.
    new_num: New number per stat.
  """

  def __init__(self, stat):
    """Initializes a stats Object with given attributes.

    Args:
      stat: (str) name of the statistic.
    """
    self.stat = stat
    self.initial_pos = None
    self.initial_neg = None
    self.initial_death = None
    self.new_pos = None
    self.new_neg = None
    self.new_death = None
    self.pos_delta = None
    self.neg_delta = None
    self.death_delta = None
    self.last_check = None


def text_to_speech(text, id):
  """Convert string to audio using Google Text-to-speech.

  Writes each audio file, to filesystem.

  Args:
    text: (str) To be converted to audio file.
    id: (str) Increment for audio  file being written.
  """
  speech = gTTS(text=text, lang='en', slow=False)
  speech.save(id + '.mp3')


def get_state_data(my_state):
  """Get the raw data from API."""
  url = 'https://covidtracking.com/api/states'
  raw_data = None
  while raw_data is None:
    try:
      raw_data = json.loads(requests.request('GET', url, verify=False).text)
    except:
      print('API Get for state-data failed.')
      pass
      time.sleep(5)  # If HTTP Request fails, wait 5s and try again.

  return next(state for state in raw_data if state['state'] == my_state)


def get_world_data():
  """Get the raw data from corona-stats.online (updates faster)"""
  url = ('https://corona-stats.online/?format=json')
  raw_data = None
  while raw_data is None:
    try:
      raw_data = json.loads(requests.request('GET', url, verify=False).text)
    except:
      print('API Get for country-data failed.')
      pass
      time.sleep(5)  # If HTTP Request fails, wait 5s and try again.

  return raw_data


def parse_data():
  """Detrmine if reported cases has increased."""
  # Parse state data.
  state_obj.pos_delta = state_obj.new_pos - state_obj.initial_pos
  state_obj.neg_delta = state_obj.new_neg - state_obj.initial_neg
  state_obj.death_delta = state_obj.new_death - state_obj.initial_death

  country_obj.pos_delta = country_obj.new_pos - country_obj.initial_pos
  country_obj.death_delta = country_obj.new_death - country_obj.initial_death
  # Process state data.
  if state_obj.pos_delta > 0:
    print('Increase in positive cases in yuor state by %i' % state_obj.pos_delta)
    # Comment out this line to disable sound playing.
    if datetime.datetime.now().strftime("%H") not in OFF_HOURS:
      text_to_speech('Increase of %i positive cases in your state.' %
                     state_obj.pos_delta, '0')
      playsound('0.mp3')

  if state_obj.neg_delta > 0:
    print('Increase in negative cases. by %i' % state_obj.neg_delta)
    # Comment out this line to disable sound playing.
    if datetime.datetime.now().strftime("%H") not in OFF_HOURS:
      text_to_speech('Increase of %i negative cases in your state' %
                     state_obj.neg_delta, '1')
      playsound('1.mp3')
  if state_obj.death_delta > 0:
    print('Increase in deaths by %i' % state_obj.death_delta)
    # Comment out this line to disable sound playing.
    if datetime.datetime.now().strftime("%H") not in OFF_HOURS:
      text_to_speech('Increase of %i more dead people.' %
                     state_obj.death_delta, '2')
      playsound('2.mp3')

  print('As of %s, the current totals are:\n%i positve'
          '\n%i negative\n%i deaths'
          % (datetime.datetime.now().strftime("%D:%H:%M:%S"), state_obj.new_pos,
             state_obj.new_neg, state_obj.new_death))

  # Process country data.
  if country_obj.death_delta > 0:
    print('Increase in deaths in your country by %i' % country_obj.death_delta)
    # Comment out this line to disable sound playing.
    if datetime.datetime.now().strftime("%H") not in OFF_HOURS:
      text_to_speech('Increase of %i more dead people in your country.' %
                     country_obj.death_delta, '3')
      playsound('3.mp3')

  # TODO: Clean up all temp MP3 files.
def get_data(initial):
  """Get initial data points from APIs.

  Args:
    initial: (bool) Whether this is initial run or not.
  Returns:
    state_obj: (class) Representing state data points.
    country_obj: (class) Representing country data points.
  """
  state_data = get_state_data(my_state.upper())  # Argument passed in.
  world_data = get_world_data()
  print(next(cases['cases'] for cases in world_data['data'] if cases['country'] == 'USA'))
  sys.exit()
  #country_data = world_data['data'][0]['country'] == my_cc.upper():
  #print(country_data)
  if initial:
    state_obj.initial_pos = state_data['positive']
    state_obj.initial_neg = state_data['negative']
    state_obj.initial_death = state_data['death']
    country_obj.initial_pos = next(cases['cases'] for cases in world_data['data']
                                   if cases['country'] == my_country)
    country_obj.initial_death = next(deaths['deaths'] for deaths in world_data['data']
                                   if cases['country'] == my_country)
  else:
    state_obj.new_pos = state_data['positive']
    state_obj.new_neg = state_data['negative']
    state_obj.new_death = state_data['death']
    country_obj.new_pos = next(cases['cases'] for cases in world_data['data']
                                   if cases['country'] == my_country)
    country_obj.new_death = next(cases['cases'] for cases in world_data['data']
                                   if cases['country'] == my_country)


if __name__ == '__main__':
  # Build objects to store data points.
  state_obj = StatsObject('state_data')
  country_obj = StatsObject('country_data')
  world_obj = StatsObject('world_data')
  get_data(True)  # Get initial data points.
  print('Starting number of positive cases is: %i' % state_obj.initial_pos)
  print('Starting number of negative cases is: %i' % state_obj.initial_neg)
  print('Starting number of deaths is: %i' % state_obj.initial_death)
  while True:
    time.sleep(3600)  # Perform the check every hour.
    get_data(False)  # Get new data points.
    state_obj.last_check = time.time()
    parse_data()
    get_data(True)  # Reset initial numbers to last loop run.
