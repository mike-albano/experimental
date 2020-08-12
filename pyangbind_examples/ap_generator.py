"""Module used to generate intermediate configuration blobs for
Access Points.

Uses Python bindings generated from openconfig-access-points.yang
With pyang 1.6 & oc-pyang installed:
pyang --plugindir $PYBINDPLUGIN -f pybind -o access_points_bindings.py ./public/release/models/wifi/access-points/openconfig-access-points.yang public/release/models/wifi/access-points/openconfig-ap-interfaces.yang -p ./public/
"""

import pyangbind.lib.pybindJSON as pybindJSON
from access_points_bindings import openconfig_access_points
import json
from pyangbind.lib.serialise import pybindJSONDecoder


configs = openconfig_access_points()

def main():
  all_configs = CreateConfigs()
  print(pybindJSON.dumps(all_configs, mode='ietf', indent=2))

def CreateConfigs():
  ap_conf = configs.access_points.access_point.add('tester-01.example.net')
  ## 5GHz Radio
  ap_conf_phy5G = ap_conf.radios.radio.add(id=0, operating_frequency='FREQ_5GHZ')
  ap_conf_phy5G.config.id = 0
  ap_conf_phy5G.config.operating_frequency = 'FREQ_5GHZ'
  ap_conf_phy5G.config.enabled = True
  ap_conf_phy5G.config.transmit_power = 5
  ap_conf_phy5G.config.channel = 44
  ap_conf_phy5G.config.channel_width = 40
  ap_conf_phy5G.config.dca = False
  return configs
  # Play with ordering the JSON for some human readability
  #configsJson = json.loads(pybindJSON.dumps(configs, mode="ietf"))
  #sortedJson = OrderedDict()
  #sortedJson['config-ids'] = configsJson['config-ids']

if __name__ == '__main__':
  main()
