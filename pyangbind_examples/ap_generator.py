"""Module used to generate intermediate configuration blobs for
Access Points.

Uses Python bindings generated from openconfig-access-points.yang
With pyang 1.6 & oc-pyang installed:
pyang --plugindir $PYBINDPLUGIN -f pybind -o access_points_bindings.py ./public/release/models/wifi/access-points/openconfig-access-points.yang public/release/models/wifi/access-points/openconfig-ap-interfaces.yang -p ./public/
"""

import pyangbind.lib.pybindJSON as pybindJSON
from access_points_bindings import openconfig_access_points

configs = openconfig_access_points()

def main():
  all_configs = CreateConfigs()
  #chan_change = ChangeChan()
  print(pybindJSON.dumps(all_configs, indent=2, mode='ietf'))
  #print(pybindJSON.dumps(assign_txpower, indent=2, mode='ietf'))

def CreateConfigs():
  ap_conf = configs.access_points.access_point.add('link022-pi-ap')
  ## 5GHz Radio
  ap_conf_phy5G = ap_conf.radios.radio.add(id=0, operating_frequency='FREQ_5GHZ')
  ap_conf_phy5G.config.id = 0
  ap_conf_phy5G.config.operating_frequency = 'FREQ_5GHZ'
  ap_conf_phy5G.config.enabled = True
  ap_conf_phy5G.config.transmit_power = 3
  ap_conf_phy5G.config.channel = 44
  ap_conf_phy5G.config.channel_width = 40
  # TEST DELETING and adding an AP OBJ
  #configs.access_points.access_point.delete('link022-pi-ap')
  #configs.access_points.access_point.add('link022-pi-ap')

  #ap_conf2 = configs.access_points.access_point.add('ap2.example.com')
  # deviated/not supported hostname
  #ap_conf.system.config.hostname = 'foohost'
  #ap_conf2.system.config.hostname = 'foohost2'
  # ap-manager config
  #ap_conf_apmanager = ap_conf.assigned_ap_managers.ap_manager.add('primary')
  #ap_conf_apmanager2 = ap_conf.assigned_ap_managers.ap_manager.add('secondary')
  #ap_conf_apmanager.config.id = 'primary'
  #ap_conf_apmanager2.config.id = 'secondary'
  #ap_conf_apmanager.config.ap_manager_ipv4_address = '192.168.1.2'
  #ap_conf_apmanager2.config.ap_manager_ipv4_address = '192.168.2.2'
  #ap_conf_apmanager.config.fqdn = 'primary-manager.example.com'
  #ap_conf_apmanager2.config.fqdn = 'secondary-manager.example.com'
  ## Systems config
  #ap_conf_srvgrp = ap_conf.system.aaa.server_groups.server_group.add('prod-radius')
  #ap_conf_srvgrp.config.name = 'Radius-Group'
  #ap_conf_srvgrp.config.type = ('RADIUS')
  #ap_conf_srvaddr = ap_conf_srvgrp.servers.server.add('192.168.1.5')
  #ap_conf_srvaddr.config.address = '192.168.1.5'
  #ap_conf_srvaddr.radius.config.auth_port = 1812
  #ap_conf_srvaddr.config.timeout = 5
  #ap_conf_srvaddr.radius.config.secret_key = 'test_secret'
  #ap_conf_phy5G.config.dca = False
  #ap_conf_phy5G.config.scanning_defer_traffic = True
  #ap_conf_phy5G.config.dtp = False
  #ap_conf_phy5G.config.scanning = True
  ## 2.4GHz Radio
  #ap_conf_phy2G = ap_conf.radios.radio.add(1)
  #ap_conf_phy2G.config.id = 1
  #ap_conf_phy2G.config.operating_frequency = 'FREQ_2GHZ'
  #ap_conf_phy2G.config.enabled = True
  #ap_conf_phy2G.config.dca = True
  #ap_conf_phy2G.config.transmit_power = 3
  #ap_conf_phy2G.config.channel_width = 20
  #ap_conf_phy2G.config.dtp = False
  #ap_conf_phy2G.config.scanning = True
  ## Interface configs
  ap_conf_interface = ap_conf.interfaces.interface.add('Gi0/0')
  ap_conf_interface.config.name = 'Gi0/0'
  ap_conf_vlan_map = ap_conf_interface.ethernet.switched_vlan.dot1x_vlan_map.vlan_name.add('Corp-VLAN')
  ap_conf_vlan_map.config.vlan_name = 'Corp-VLAN'
  ap_conf_vlan_map.config.id = 260
  ## Add MAC config
  ap_conf_company_a = ap_conf.ssids.ssid.add('test-ssid1')
  ap_conf_company_a.config.enabled = True
  ap_conf_company_a.config.name = 'test-ssid1'
  #ap_conf_company_a.config.hidden = False
  ap_conf_company_a.config.default_vlan = 200
  ap_conf_company_a.config.vlan_list = [200, 260, 270]
  #ap_conf_company_a.config.operating_frequency = 'FREQ_5GHZ'
  #ap_conf_company_a.config.basic_data_rates = ['RATE_36MB', 'RATE_48MB', 'RATE_54MB']
  #ap_conf_company_a.config.supported_data_rates = ['RATE_36MB', 'RATE_48MB', 'RATE_54MB']
  #ap_conf_company_a.config.broadcast_filter = True
  #ap_conf_company_a.config.multicast_filter = True
  #ap_conf_company_a.config.ipv6_ndp_filter = True
  #ap_conf_company_a.config.ipv6_ndp_filter_timer = 300
  #ap_conf_company_a.config.station_isolation = True
  #ap_conf_company_a.config.opmode = 'WPA2_ENTERPRISE'
  #ap_conf_company_a.config.server_group = 'prod-radius'
  #ap_conf_company_a.config.dva = True
  #ap_conf_company_a.config.dhcp_required = False
  #ap_conf_company_a.config.qbss_load = True
  #ap_conf_company_a.config.advertise_apname = True
  #ap_conf_company_a.config.csa = True
  #ap_conf_company_a.config.ptk_timeout = '28800'
  #ap_conf_company_a.config.gtk_timeout = '3600'
  #ap_conf_company_a.config.dot11k = True
  #ap_conf_company_a.dot11v.config.dot11v_bsstransition = True
  #ap_conf_company_a.dot11v.config.dot11v_dms = False
  #ap_conf_company_a.dot11v.config.dot11v_bssidle = False
  #ap_conf_company_a.dot11r.config.dot11r = True
  #ap_conf_company_a.dot11r.config.dot11r_method = 'OVA'
  #ap_conf_company_a.dot11r.config.dot11r_domainid = 5
  #ap_conf_company_a.dot1x_timers.config.max_auth_failures = '5'
  #ap_conf_company_a.dot1x_timers.config.blacklist_time = '60'
  #ap_conf_company_a.wmm.config.trust_dscp = True
  #ap_conf_company_a.band_steering.config.band_steering = False
  #ap_conf_company_guest = ap_conf.ssids.ssid.add('Corp-Guest')
  #ap_conf_company_guest.config.name = 'Corp-Guest'
  #ap_conf_company_guest.config.enabled = True
  #ap_conf_company_guest.config.hidden = False
  #ap_conf_company_guest.config.vlan_id = 666
  #ap_conf_company_guest.config.operating_frequency = 'FREQ_5GHZ'
  #ap_conf_company_guest.config.basic_data_rates = ['RATE_36MB', 'RATE_48MB', 'RATE_54MB']
  #ap_conf_company_guest.config.supported_data_rates = ['RATE_36MB', 'RATE_48MB', 'RATE_54MB']
  #ap_conf_company_guest.config.broadcast_filter = True
  #ap_conf_company_guest.config.multicast_filter = True
  #ap_conf_company_guest.config.ipv6_ndp_filter = True
  #ap_conf_company_guest.config.ipv6_ndp_filter_timer = 300
  #ap_conf_company_guest.config.station_isolation = True
  #ap_conf_company_guest.config.opmode = 'OPEN'
  #ap_conf_company_guest.config.dhcp_required = False
  #ap_conf_company_guest.config.qbss_load = True
  #ap_conf_company_guest.config.advertise_apname = True
  #ap_conf_company_guest.config.csa = True
  #ap_conf_company_guest.config.dot11k = True
  #ap_conf_company_guest.dot11v.config.dot11v_bsstransition = True
  #ap_conf_company_guest.dot11v.config.dot11v_dms = False
  #ap_conf_company_guest.dot11v.config.dot11v_bssidle = False
  #ap_conf_company_guest.wmm.config.trust_dscp = True
  #ap_conf_company_guest.band_steering.config.band_steering = False
  ##Guest PSK
  ## Add PHY config, adhering to OC Model Schema
  #ap_confpsk_company_guest = ap_conf.ssids.ssid.add('GuestPSK')
  #ap_confpsk_company_guest.config.name = 'GuestPSK'
  #ap_confpsk_company_guest.config.enabled = True
  #ap_confpsk_company_guest.config.hidden = False
  #ap_confpsk_company_guest.config.vlan_id = 666
  #ap_confpsk_company_guest.config.operating_frequency = 'FREQ_5GHZ'
  #ap_confpsk_company_guest.config.basic_data_rates = ['RATE_36MB', 'RATE_48MB', 'RATE_54MB']
  #ap_confpsk_company_guest.config.supported_data_rates = ['RATE_36MB', 'RATE_48MB', 'RATE_54MB']
  #ap_confpsk_company_guest.config.broadcast_filter = True
  #ap_confpsk_company_guest.config.multicast_filter = True
  #ap_confpsk_company_guest.config.ipv6_ndp_filter = True
  #ap_confpsk_company_guest.config.ipv6_ndp_filter_timer = 300
  #ap_confpsk_company_guest.config.station_isolation = True
  #ap_confpsk_company_guest.config.opmode = 'WPA2_PERSONAL'
  #ap_confpsk_company_guest.config.wpa2_psk = 'seevalentine'
  #ap_confpsk_company_guest.config.dhcp_required = False
  #ap_confpsk_company_guest.config.qbss_load = True
  #ap_confpsk_company_guest.config.advertise_apname = True
  #ap_confpsk_company_guest.config.csa = True
  #ap_confpsk_company_guest.config.dot11k = True
  #ap_confpsk_company_guest.dot11v.config.dot11v_bsstransition = True
  #ap_confpsk_company_guest.dot11v.config.dot11v_dms = False
  #ap_confpsk_company_guest.dot11v.config.dot11v_bssidle = False
  #ap_confpsk_company_guest.wmm.config.trust_dscp = True
  #ap_confpsk_company_guest.band_steering.config.band_steering = False

  return configs
  # Play with ordering the JSON for some human readability
  #configsJson = json.loads(pybindJSON.dumps(configs, mode="ietf"))
  #sortedJson = OrderedDict()
  #sortedJson['config-ids'] = configsJson['config-ids']

if __name__ == '__main__':
  main()
