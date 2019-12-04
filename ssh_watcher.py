# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#####

# Pexpect script, used to get various output and parse.
import os
import sys
import getpass
import argparse
import time
import datetime
import io

try:  # Make sure pexpect installed.
  import pexpect
except ImportError:
  print('****ERROR****\npexpect not installed. Use: pip3 install pexpect')
  sys.exit(1)


def _create_parser():
  """Create parser for arguments passed into the program from the CLI.

  Returns:
    Argparse object.
  """
  parser = argparse.ArgumentParser(description='SSH to a device and '
                                   'parse output')
  parser = argparse.ArgumentParser(formatter_class=argparse.
                                   RawDescriptionHelpFormatter,epilog=
                                   'longer description here')
  parser.add_argument('-u', '--unattended', action='store_true', help=
                      'Continuously run every 60 seconds', required=False)
  parser.add_argument('-f', '--filename', type=str, help='Filename '
                         'to store output(s)', required=True)
  parser.add_argument('-d', '--device', type=str, help='Device to SSH to.',
                      required=True)
  parser.add_argument('-k', '--keyfile', help='2-line GPG encrypted keyfile '
                         'line 1 = user & line 2 = password', required=False)
  parser.add_argument('-c', '--cli_cmd', help='Command to run', required=True)
  parser.add_argument('-p', '--port', help='SSH port to use', required=False,
                      default='22')

  return parser


def _get_creds(keyfile):
  """Get creds from gpg encrypted file.

  Args:
    keyfile: (str) filename in users home dir.
  Returns:
    creds: (dict) username/password for logging in to devices.
  """
  creds = {}
  if keyfile and os.path.isfile(keyfile):
    # open the gpg file, and define some variables to be used later for credentials.
    credsfile = os.popen('gpg -d --quiet --batch ' + keyfile)
    credsfile_decrypted = credsfile.readlines()
    creds['user'] = credsfile_decrypted[0].strip('\n')
    creds['password'] = credsfile_decrypted[1].strip('\n')
    credsfile.close()
  elif keyfile and not os.path.isfile(keyfile):
    print('keyfile specified but does not exist')
    sys.exit(1)
  else:  # Prompt for creds.
    creds['user'] = getpass.getpass(prompt='User: ', stream=None)
    creds['password'] = getpass.getpass()

  return creds


def ssh_to(creds, host, port, cli_cmd):
  """SSH to the host and collect output.

  Args:
    creds: (dict) username/password for logging in to the device.
    host: (str) Hostname or IP of device.
    port: (str) SSH port to use when logging in to device.
    cli_cmd: (str) CLI command to run after logging in to device.
  Returns:
    output: (str) Output of CLI command.
  """
  child = pexpect.spawn('/usr/bin/ssh -o StrictHostKeyChecking=no -p %s %s@%s' %
                        (port, creds['user'], host))
  child.logfile = None
  #child.logfile = sys.stdout.buffer  # Print output to stdout. INCLUDES creds.
  initial = child.expect([pexpect.TIMEOUT, 'Connection refused', 'Connection'
                          'reset by peer', 'No route to host',
                          'Connection closed by remote host', 'not known\r\r\n',
                          'assword: '], timeout=10)
  if initial == 0:
    print('Waiting for SSH to return a prompt...(taking long)...')
    child.kill(0)
  elif initial == 1:
    print('Connection Refused from host')
    sys.exit(1)
  elif initial == 2:
    print('Connection reset by peer')
    sys.exit(1)
  elif initial == 3:
    print('No route to host')
    sys.exit(1)
  elif initial == 4:
    print('Connection closed by remote host')
    sys.exit(1)
  elif initial == 5:
    print('Could not resolve hostname: %s' % host)
    child.kill(0)
    sys.exit(1)
  elif initial == 6:
    child.sendline(creds['password'])
  # After sending passowrd, expect/do the following
  offer = child.expect(['interactive\).', '#', pexpect.TIMEOUT], timeout=10)
  if offer == 0:
    print('Permission Denied (failed login) for %s' % host)
    child.kill(0)
    sys.exit(1)
  elif offer == 1:
    print('logged in successfully, running command(s) on: %s...' % host)
    child.sendline('no paging')  # Change this to suite your needs.
    child.expect('#')
    sys.stdout.write('Collecting output...')
    child.sendline(cli_cmd)
    child.expect('#')
    cmd_output = child.before
    sys.stdout.write('Done.\n')
    child.kill(0)
    return cmd_output
  elif offer == 2:
    print('ssh connection timed out on %s' % host)
    child.kill(0)
    sys.exit(1)


def _parse_output(cmd_output):
  """Parse CLI command output."""
  if 'Total IPSEC SAs: 1' in str(cmd_output):  # Change this to suit your needs.
    return True
  return False


def _take_action(parsed_output, filename, creds, host, port):
  """Do something after collecting & parsing CLI output."""
  print('The current time is: ', datetime.datetime.now().time())
  if parsed_output:  # Change this to suite your needs.
    print('Output check succeeded.')
  else:  # parsed_output is False.
    print('Output check failed.')
    outfile = open(filename + str(datetime.datetime.now().time()), 'wb')
    # Get more output to write to file.
    cmd_output = ssh_to(creds, host, port, 'show log security all')
    outfile.write(cmd_output)
    outfile.close()
    sys.exit()


def main():
  argparser = _create_parser()
  args = vars(argparser.parse_args())
  # Assign variables to the arguments provided
  host = args['device']
  filename = args['filename']
  unattended = args['unattended']
  keyfile = args['keyfile']
  cli_cmd = args['cli_cmd']
  port = args['port']
  creds = _get_creds(keyfile)
  if unattended:
    print('Will run continuously, every 60 seconds. Ctrl-C to break.')
    while True:
      cmd_output = ssh_to(creds, host, port, cli_cmd)
      _take_action(_parse_output(cmd_output), filename, creds, host, port)  # Change this to suit.
      time.sleep(60)
  else:
    cmd_output = ssh_to(creds, host, port, cli_cmd)
    _take_action(_parse_output(cmd_output), filename, creds, host, port)  # Change this to suit.



if __name__ == '__main__':
  main()
