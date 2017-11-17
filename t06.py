#!/usr/bin/env python
# encoding utf-8



from IPy import IP, IPSet
import requests
import socket
from sys import stdout
from time import sleep
import syslog
import os

syslogprefix = __file__ + '[' + str(os.getpid()) + ']:'

#nexthop = ' next-hop self community [64512:666]\n'

blocklists = ['https://www.spamhaus.org/drop/drop.txt',
              'https://www.spamhaus.org/drop/edrop.txt',
              'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
              'http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt']

def test():
    Bogons = {}
    f = open('drop.txt', 'rU')
    for line in f:
        Bogons[line] = line
    return Bogons

if True:
    B = test()
    print B 

