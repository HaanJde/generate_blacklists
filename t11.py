#!/usr/bin/env python
# encoding utf-8

from __future__ import print_function
from IPy import IP, IPSet
import requests
import socket
from sys import stdout
from time import sleep
import syslog
import os
import re

syslogprefix = __file__ + '[' + str(os.getpid()) + ']:'

#nexthop = ' next-hop self community [64512:666]\n'

blocklists = ['https://www.spamhaus.org/drop/drop.txt',
              'https://www.spamhaus.org/drop/edrop.txt',
              'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
              'http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt']

def test():
    Bogons = set()
    f = open('drop.txt', 'rU')
    for line in f:
                                       # remove newlines from the end of the line
        line = line.rstrip("\n\r")
                                       # skip comments and empty lines
        if not re.search('^[#;$]',line):
            pf = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$",line)
                                       # prefix
            if not pf == 0:
                Bogons.add(pf)
            else:
                pf = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",line)
                                       # individual ip address
                if not pf == 0:
                    pf = pf + '/32'
                    Bogons.add(pf)
    return Bogons

if True:
    B = test()
    print(*B,sep='\n')

