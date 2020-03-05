"""Simple python3 utility to re-write JSON files.
Example:
python3 config_json-updater.py  json-files/
"""

import os
import json
from boltons.iterutils import remap
import sys

# Change values in each of the files in a directory
directory = sys.argv[1]  # Make sure to add a trailing "/" when running.

bad_keys = ['dot11r-method']

def change_val(path, key, value):
  # Set dot11r config to false, if it's currently set to true.
  if key == 'dot11r' and value == False:
    return key, True
  return key, value

def iterate_files(directory):
  """Itreate over files in the given directory and change values."""
  for filename in os.listdir(directory):
    if filename.endswith('.json'):
      config_json = json.load(open(directory + filename, 'r'))
      changed_values = remap(config_json, visit=change_val)
      drop_keys = lambda path, key, value: key not in bad_keys
      new_file = remap(changed_values, visit=drop_keys)
      out_file = open(directory + filename, 'w')  # Over-write the input file
      # Separators added for no spaces b/w key/val in JSON.
      out_file.write(json.dumps(new_file, indent=2, separators=(',', ':')))
      out_file.close()

new_file = iterate_files(directory)
