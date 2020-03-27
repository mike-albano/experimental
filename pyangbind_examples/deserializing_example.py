# Lint as: python3
"""Simple example of deserializing a JSON response
back into PyangBind classes.

Assumes a model named oc_model_version.yang.
"""

import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import json

from oc_version_binding import oc_model_version

oc_version_obj = oc_model_version()
# Shown for example we use two different objects.
oc_version_obj_loaded = oc_model_version()

# Populate the objects with sites.
oc_version_obj.sites.site.add('foo')
oc_version_obj.sites.site.add('bar')
site_json = json.loads(pybindJSON.dumps(oc_version_obj, mode='ietf'))

# Reload the JSON into objects
new_ocver_obj = pybindJSONDecoder.load_ietf_json(site_json, None, None, obj=oc_version_obj_loaded)
new_ocver_obj.sites.site.add('baz')
#print(pybindJSON.dumps(new_ocver_obj, mode='ietf'))
print(pybindJSON.dumps(new_ocver_obj.sites.site['bar']))
