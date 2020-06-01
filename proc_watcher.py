"""Look for a running process and text if not running."""

import sys
import subprocess
import time
from twilio.rest import Client

def run_cmds():
  """Run commands to include in the email message.

  Args:
    commands: tuple of commands to run.
  Returns:
    outputs: tuple of outputs.
  """
  outputs = []
  p = subprocess.check_output(['ps', 'auxw']).splitlines()
  # Add more commands here if interested in other output.
  return p

def check_outputs(outputs):
  """Check output to determine if we need to send an alert email."""
  string_found = False
  alerts = []
  for line in outputs:
    if 'smart_things_watcher.py' in str(line):  # Change this to suit your needs.
      string_found = True
  if not string_found:   # Send alert.
    return True
  return False  # No need to alert.


def send_alert():
  client = Client('your_account_sid', 'your_auth_token')
  client.messages.create(to='<your_phone#', from_='twilio_#', body='your_msg')
  print('Text message sent. Exiting', time.time())
  sys.exit()


def main():
  while True:
    outputs = run_cmds()  # Run commands we're interested in.
    alert = check_outputs(outputs)  # Determine if we need to email/alert.
    if alert:
      send_alert()
    time.sleep(5)


if __name__ == '__main__':
  main()
