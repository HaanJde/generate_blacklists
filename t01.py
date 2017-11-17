#!/usr/bin/env python
# encoding utf-8
"""
exabgp: generate_blacklists.py v1.1
based on generate_blacklists.py v1.0
author: Jan de Haan
exabgp: generate_blacklists.py v1.0
based on https://github.com/infowolfe/exabgp-edgerouter/blob/master/blocklists_simple.py
author: Simone Spinelli
exabgp: aggregate_requests.py
based partially on aggregate.py from https://github.com/infowolfe/exabgp-edgerouter/blob/master/blocklists_simple.py
"""

from IPy import IP, IPSet
import requests
import socket
from sys import stdout
from time import sleep
import syslog
import os
