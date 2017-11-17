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

syslogprefix = str(os.truename(__file__) + '[' + str(os.getpid()) + ']:'

#nexthop = ' next-hop self community [64512:666]\n'

blocklists = ['https://www.spamhaus.org/drop/drop.txt',
              'https://www.spamhaus.org/drop/edrop.txt',
              'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
              'http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt']

def fetch(blocklist):
    syslog.syslog('{0} fetching prefixes from: {1}'.format(syslogprefix, blocklist))
                                       # force no duplicates
    bogons = set()
    noofprefixes = 0
    r = requests.get(blocklist)
    for line in r.iter_lines():
                                       # remove newlines from the end of the line
        line = line.rstrip("\n\r")
                                       # skip comments and empty lines
        if not re.search('^[#;]',line) and not re.search('^$',line):
                                       # prefix
            pf = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}",line)
            if not pf == None:
                bogons.add(pf.group(0))
                noofprefixes += 1
            else:
                pf = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",line)
                                       # individual ip address
                if not pf == None:
                    bogons.add(pf.group(0) + '/32')
                    noofprefixes += 1
    syslog.syslog('{0} fetched {1} prefixes from: {2}'.format(syslogprefix, noofprefixes, blocklist))
    return bogons

if True:
    B = set()
    totalnoofuniqueprefixes = 0
    for blocklist in blocklists:
        C = fetch(blocklist)
        orgsizeofB = len(B)
        B = B | C
        sizeofB = len(B)

    print(*B,sep='\n')

