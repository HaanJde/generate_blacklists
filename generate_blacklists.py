#!/usr/bin/env python
# encoding utf-8
"""
exabgp: aggregate_requests.py
based partially on aggregate.py from https://adamkuj.net/blog/2014/04/08/a-utility-to-perform-ipv4-ipv6-prefix-aggregation/
"""

from IPy import IP, IPSet
import requests
import socket
from sys import stdout
from time import sleep
import syslog

a = IPSet()
b = IPSet()
# how long should we sleep in minutes?
mins = 30
expires = ''
nexthop = ' next-hop 169.254.1.1 community [65535:65281]\n'
#nexthop = ' next-hop self community [64512:666]\n'

blocklists = ['https://www.spamhaus.org/drop/drop.txt',
               'https://www.spamhaus.org/drop/edrop.txt',
               'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
               'http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt']

#blocklists = ['http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt']
#blocklists = ['https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt']
#blocklists = ['https://www.spamhaus.org/drop/drop.txt']

def makeprefix(ip):
	net = IP(ip, make_net=True)
	net.NoPrefixForSingleIp = None
        #print str(net)
	return net


def fetch():
	a = IPSet([])
	for blocklist in blocklists:
                syslog.syslog('generate-blacklist.py - fetching prefixes from: %s ' %blocklist)
                #print blocklist
                r = requests.get(blocklist)
                for line in r.iter_lines():
                        # Dont ask me why but like this it works. 
                        if line != "0.0.0.0/8" and line != "240.0.0.0/4" and line != "224.0.0.0/4":
                                if linefilter(line):
                                        myprefix = makeprefix(linefilter(line))
                                        #a.add(makeprefix(linefilter(line)))
                                        a.add(myprefix)
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
        syslog.syslog('generate-blacklist.py - Fetch process started')
        fetch()
        syslog.syslog('generate-blacklist.py - Fetch process ended')
        sleep(mins * 20)
