import sys
import subprocess
import time

ap_list = open(sys.argv[1]).readlines()

for ap in ap_list:
  # Disable with this command
  #cmd = 'python3 /Users/albanom/Documents/GitHub/gnxi/gnmi_cli_py/py_gnmicli.py -t openconfig.mist.com -p 443 -m set-update -x /access-points/access-point[hostname=' + ap.strip('\n').strip() + ']/ssids/ssid[name=ssid-name]/config/enabled -user *snip* -pass *snip* -val False'
  # Enable with this command
  cmd = 'python3 /Users/albanom/Documents/GitHub/gnxi/gnmi_cli_py/py_gnmicli.py -t openconfig.mist.com -p 443 -m set-update -x /access-points/access-point[hostname=' + ap.strip('\n').strip() + ']/ssids/ssid[name=ssid-name]/config/enabled -user *snip* -pass *snip* -val True'
  subprocess.run(cmd, shell=True, encoding='utf-8', stdout=subprocess.PIPE)
  print('Disabled ssid on %s' % ap)
  time.sleep(.5)
