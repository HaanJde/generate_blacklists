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

def fetch(blocklist):
    syslog.syslog('{0} fetching prefixes from {1}'.format(syslogprefix, blocklist))
                                       # force no duplicates
    bogons = set()
    noofprefixes = 0
                                       # wget
    r = requests.get(blocklist)
    for line in r.iter_lines():
                                       # remove newlines from the end of the line
        line = line.rstrip("\n\r")
                                       # skip comments and empty lines
        if not re.search('^[#;]',line) and not re.search('^$',line):
                                       # prefix, like 1.2.3.4/5
            pf = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}",line)
            if not pf == None:
                bogons.add(pf.group(0))
                noofprefixes += 1
            else:
                pf = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",line)
                                       # individual ip address 1.2.3.4
                if not pf == None:
                                       # add prefix /32
                    bogons.add(pf.group(0) + '/32')
                    noofprefixes += 1
    syslog.syslog('{0} fetched {1} prefixes from {2}'.format(syslogprefix, noofprefixes, blocklist))
    return bogons

def main():
    syslogprefix = str(os.path.realpath(__file__)) + '[' + str(os.getpid()) + ']:'
    #nexthop = ' next-hop self community [64512:666]\n'
    blocklists = ('https://www.spamhaus.org/drop/drop.txt',
                  'https://www.spamhaus.org/drop/edrop.txt',
                  'https://rules.emergingthreats.net/fwrules/emerging-Block-IPs.txt',
                  'http://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt')
    
                                       # list of bogons who's routes are 
				       # currently pointing to the blackhole
    currentbogons = set()
                                       # main loop
    while True:
        latestbogons = set()
        sizeoflb = 0
        for blocklist in blocklists:
	    previoussizeoflb = sizeoflb
            latestbogons = latestbogons | fetch(blocklist)
            sizeoflb = len(latestbogons)
            syslog.syslog('{0} added {1} new prefixes from {2}'.format(syslogprefix, sizeoflb - previoussizeoflb, blocklist))
        syslog.syslog('{0} total {1} uniqe prefixes'.format(syslogprefix, sizeoflb))
        latestbogons.remove("0.0.0.0/8")
        latestbogons.remove("240.0.0.0/4")
        latestbogons.remove("224.0.0.0/4")

        

#    for prefix in b:
#        if b.len() > 0 and b.__contains__(prefix) and not a.__contains__(prefix):
#            a.discard(prefix)
#            stdout.write('withdraw route ' + str(prefix) + nexthop)
#            stdout.flush()




#    for prefix in a:
#        if a.__contains__(prefix) and not b.__contains__(prefix):
#            stdout.write('announce route ' + str(prefix) + nexthop)
#            stdout.flush()
#
#    b.add(a)

	= LatestListofPrefixes

        print(*B,sep='\n')
        sleep (10*60)

if __name__ == "__main__": main()
