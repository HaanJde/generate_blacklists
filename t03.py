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

# syslogprefix = sys.argv[0] + '[' + os.getpid() + ']:' 
syslogprefix = __file__ + '[' + str(os.getpid()) + ']:'

a = IPSet()
b = IPSet()
# how long should we sleep in minutes?
mins = 10
expires = ''
nexthop = ' next-hop 169.254.1.1 community [65535:65281]\n'
#nexthop = ' next-hop self community [64512:666]\n'

blocklists = ['https://www.spamhaus.org/drop/drop.txt',
               'https://www.spamhaus.org/drop/edrop.txt',
               'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
               'http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt']

def makeprefix(ip):
    net = IP(ip, make_net=True)
    net.NoPrefixForSingleIp = None
    return net

def test():
    mine = IP('123.45.78.0/24')
    mine = makeprefix(mine)
    return 0


if True:
    test()
