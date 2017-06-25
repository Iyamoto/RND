# Working with GeoIP

import pygeoip
import os
import json

def getrecord(tgt):
    geopath = os.path.join('data', 'GeoLiteCity.dat')
    gi = pygeoip.GeoIP(geopath)
    rec = gi.record_by_name(tgt)
    return rec

tgt = '127.0.0.1'
data = getrecord(tgt)
print(json.dumps(data, indent=4))