"""Module used to generate intermediate configuration blobs for
Access Points.

Uses Python bindings generated from openconfig-access-points.yang
With pyang 1.6 & oc-pyang installed:
pyang --plugindir $PYBINDPLUGIN -f pybind -o access_points_augbindings.py openconfig-access-points.yang arista-wifi-augments.yang -p ~/openconfig
"""

import pyangbind.lib.pybindJSON as pybindJSON
from access_points_augbindings import openconfig_access_points

configs = openconfig_access_points()

def main():
  all_configs = CreateConfigs()
  print(pybindJSON.dumps(all_configs, indent=2, mode='ietf'))

def CreateConfigs():
  ap_conf = configs.access_points.access_point.add('link022-pi-ap')
  ## 5GHz Radio
  ap_conf_phy5G = ap_conf.radios.radio.add(id=0, operating_frequency='FREQ_5GHZ')
  ap_conf_phy5G.config.id = 0
  ap_conf_phy5G.config.operating_frequency = 'FREQ_5GHZ'
  ap_conf_phy5G.config.enabled = True
  ap_conf_phy5G.config.transmit_power = 9
  #ap_conf_phy5G.config.transmit_power._mchanged = True
  #ap_conf_phy5G.config.channel = 44
  #ap_conf_phy5G.config.channel_width = 40
  # TEST DELETING and adding an AP OBJ
  #configs.access_points.access_point.delete('link022-pi-ap')
  #configs.access_points.access_point.add('link022-pi-ap')

  ## Add MAC config
  ap_conf_company_a = ap_conf.ssids.ssid.add('Auth-Link022')
  ap_conf_company_a.config.name = 'Auth-Link022'
  ap_conf_company_a.config.enabled = True
  ap_conf_company_a.config.remote_bridging = True
  return configs
  # Play with ordering the JSON for some human readability
  #configsJson = json.loads(pybindJSON.dumps(configs, mode="ietf"))
  #sortedJson = OrderedDict()
  #sortedJson['config-ids'] = configsJson['config-ids']

if __name__ == '__main__':
  main()
