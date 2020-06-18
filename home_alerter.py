"""Watch various APIs (smartthings, openweather, etc.)and annouce on events."""

import time
import constants  # Use a 'constants.py' file to stash sensitive info.
import datetime
import json
import pychromecast
import requests
import time
import threading
import urllib3
urllib3.disable_warnings()  # Don't care much for cert validity here.
from twilio.rest import Client
import sys

GARAGE_ALERT_HOURS = ['20', '21', '22', '23']
QUIET_HOURS = ['23', '00', '01', '02', '03', '04', '05', '06']
WEEKDAYS = [0, 1, 2, 3, 6]  # Mon-Thurs & Sun
WEEKENDS = [4, 5]


def get_st_data(device_id):
  """Get the raw data from SmartThings API."""
  url = 'https://api.smartthings.com/v1/devices/{device_id}/status'.format(
    device_id = device_id)
  headers = {'Authorization': constants.ST_BEARER}
  raw_data = None
  while raw_data is None:
    try:
      raw_data = json.loads(requests.request('GET', url, headers=headers,
                                             verify=False).text)
    except:
      print('API Get for smartthings-data failed.')
      pass
      time.sleep(5)  # If HTTP Request fails, wait 5s and try again.

  return raw_data


def get_weather_data(api_key):
  """Get the raw data from openweathermap.org API."""
  url = 'https://api.openweathermap.org/data/2.5/onecall?lat=40.02&lon=-105.27&units=imperial&appid={api_key}'.format(
    api_key = api_key)
  raw_data = None
  while raw_data is None:
    try:
      raw_data = json.loads(requests.request('GET', url, verify=False).text)
    except:
      print('API Get for weather-data failed.')
      pass
      time.sleep(5)  # If HTTP Request fails, wait 5s and try again.

  return raw_data


def cast_mp3(chromecasts, target_device, mp3_url, initial_volume, return_volume):
  """Play an MP3 on CC or Speaker Group."""
  cast = next(cc for cc in chromecasts if cc.device.friendly_name == target_device)
  cast.wait()
  if initial_volume:
    cast.set_volume(1)  # Set volume to Max (1)
    time.sleep(2)
  cast.media_controller.play_media(mp3_url, 'audio/mp3')
  time.sleep(5)  # Ensure cast devices connect.
  if return_volume:
    cast.set_volume(.5)  # Set volume to middle.


def send_alert(mp3_file, cc):
  """Sound the alarm."""
  url = 'http://192.168.0.40/{mp3}'.format(mp3=mp3_file)
  chromecasts = pychromecast.get_chromecasts()
  cast = cast_mp3(chromecasts, cc, url, True, True)

def check_right_garage():
  """Parse the data and do something with it."""
  while True:
    if datetime.datetime.now().strftime("%H") in GARAGE_ALERT_HOURS:
      garage_right_data = get_st_data(constants.RIGHT_GARAGE_ID)
      if garage_right_data['components']['main']['contactSensor']['contact']['value'] == 'closed':
        print('Right Garage sensor is closed as of {time_now}.'.format(
          time_now=datetime.datetime.now().strftime("%D:%H:%M:%S")))
      else:
        send_alert('right_garage.mp3', 'all_not_livingroom')
    time.sleep(1800)  # Check garage every half hour.


def check_left_garage():
  """Parse the data and do something with it."""
  while True:
    if datetime.datetime.now().strftime("%H") in GARAGE_ALERT_HOURS:
      garage_left_data = get_st_data(constants.LEFT_GARAGE_ID)
      if garage_left_data['components']['main']['contactSensor']['contact']['value'] == 'closed':
        print('Left Garage sensor is closed as of {time_now}.'.format(
          time_now=datetime.datetime.now().strftime("%D:%H:%M:%S")))
      else:
        send_alert('left_garage.mp3', 'all_not_livingroom')
    time.sleep(1800)  # Check garage every half hour.


def device_reminder():
  """Reminder to put away devices."""
  last_broadcast = False  # Set last broadcast to null.
  while True:
    today = datetime.datetime.now().strftime("%D")
    if datetime.datetime.today().weekday() in WEEKDAYS and datetime.datetime.now().strftime("%H") == '20':
      if not last_broadcast == today:  # Don't bcast more than once/day.
        print('Broadcasting weekday device warning.')
        send_alert('put_away_devices.mp3', 'all_not_livingroom')
        last_broadcast = datetime.datetime.now().strftime("%D")
    elif datetime.datetime.today().weekday() in WEEKENDS and datetime.datetime.now().strftime("%H") == '22':
      if not last_broadcast == today:
        print('Broadcasting weekend device warning.')
        send_alert('put_away_devices.mp3', 'all_not_livingroom')
        last_broadcast = datetime.datetime.now().strftime("%D")
    time.sleep(10)  # Check 10s.


def check_weather():
  """Check openweathermap.org weather conditions."""
  while True:
    if datetime.datetime.now().strftime("%H") not in QUIET_HOURS:
      weather_data = get_weather_data(constants.WEATHER_APIKEY)
      for hour in weather_data['hourly']:
        # Only interested in wind_speed within the next hour
        if hour['dt'] - int(time.time()) > 1 and hour['dt'] - int(time.time()) < 3600:
          if hour['wind_speed'] > 15:  # Alert based on > 15MPH winds.
            print('Its getting windy! {wind_speed} MPH.'.format(wind_speed = hour['wind_speed']))
            send_alert('wind_alert.mp3', 'all_not_livingroom')
    time.sleep(3600)  # Check wind speed every hour.


def thread_monitor():
  """Monitor the state of threads and alert."""
  while True:
    mythreads = threading.enumerate()
    if len(mythreads) < 6:  # A thread has failed.
      print('A thread has died. Here are the current threads:\n')
      print(mythreads)
      client = Client(constants.TWILIO_SID, constants.TWILIO_AUTHTOKEN)
      client.messages.create(to=constants.TO_PHONE, from_=constants.FROM_PHONE,
                             body='Thread dead on smart_things_watcher script')
      sys.exit()
    time.sleep(2)


if __name__ == '__main__':
  r_garage_check = threading.Thread(target=check_right_garage, name='r_garage')
  l_garage_check = threading.Thread(target=check_left_garage, name='l_garage')
  device_reminder_check = threading.Thread(target=device_reminder, name='reminder')
  weather_check = threading.Thread(target=check_weather, name='weather')
  monitor = threading.Thread(target=thread_monitor, name='thread_monitor')
  r_garage_check.start()
  l_garage_check.start()
  device_reminder_check.start()
  weather_check.start()
  monitor.start()
