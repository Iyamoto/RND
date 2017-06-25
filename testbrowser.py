# Python serfing

import logging
from grab import Grab

logging.basicConfig(level=logging.DEBUG)

g = Grab()

g.go('http://www.syngress.com/')

