# Working with GeoIP

import pygeoip
import os
import json

geopath = os.path.join('data', 'GeoLiteCity.dat')
gi = pygeoip.GeoIP(geopath)

def getrecord(tgt):
    rec = gi.record_by_name(tgt)
    return rec

tgt = '173.255.226.98'
data = getrecord(tgt)
print(json.dumps(data, indent=4))