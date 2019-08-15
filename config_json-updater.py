import json
from boltons.iterutils import remap
import sys

config_json = json.load(open(sys.argv[1], 'r'))
bad_keys = ['dot11r-method']

def change_val(path, key, value):
  # Set dot11r config to false, if it's currently set to true.
  if key == 'dot11r' and value == True:
    return key, False
  return key, value

changed_values = remap(config_json, visit=change_val)
drop_keys = lambda path, key, value: key not in bad_keys
clean = remap(changed_values, visit=drop_keys)

print(json.dumps(clean, indent=2))  # Dump to stdout.
