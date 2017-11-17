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
    mine = IP()
    return 0

def fetch():
    a = IPSet([])
    totalnoofnewprefixes = 0
    for blocklist in blocklists:
        syslog.syslog('{0} fetching prefixes from: {1}'.format(syslogprefix, blocklist))
#	'{0} in {1}'.format(unicode(self.author,'utf-8'),  unicode(self.publication,'utf-8'))
        r = requests.get(blocklist)
        for line in r.iter_lines():
            # Dont ask me why but like this it works. 
            if line != "0.0.0.0/8" and line != "240.0.0.0/4" and line != "224.0.0.0/4":
                if linefilter(line):
                    myprefix = makeprefix(linefilter(line))
#                   if myprefix not in a                    
		    a.add(myprefix)
        noofprefixes = a.__len__
        syslog.syslog('{0} got {1} prefixes from: {2}'.format(syslogprefix, noofprefixes, blocklist))
        totalnoofnewprefixes = totalnoofnewprefixes + noofprefixes
    syslog.syslog('{0} got {1} prefixes in total from upstream'.format(syslogprefix, totalnoofprefixes))
    for prefix in b:
        if b.len() > 0 and b.__contains__(prefix) and not a.__contains__(prefix):
            a.discard(prefix)
            stdout.write('withdraw route ' + str(prefix) + nexthop)
            stdout.flush()

    for prefix in a:
        if a.__contains__(prefix) and not b.__contains__(prefix):
            stdout.write('announce route ' + str(prefix) + nexthop)
            stdout.flush()

    b.add(a)

def linefilter(line):
    if line.startswith(';'):
        if line.startswith('; Expires:'):
            expires = line.lstrip('; Expires: ')
        else:
            pass
        pass
    elif line.startswith('#'):
        pass
    else:
        ip = line.split(' ')[0].split(';')[0].split('#')[0].strip().decode()
        return ip


while True:
        syslog.openlog('exabgp')
        syslog.syslog('{0} Fetch process started'.format(syslogprefix))
        fetch()
        syslog.syslog('{0} Fetch process ended'.format(syslogprefix))
        sleep(mins * 60)
