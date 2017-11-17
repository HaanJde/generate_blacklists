#!/usr/bin/env python
# encoding utf-8

import sys
import re

for line in sys.stdin:
    line = line.rstrip("\n\r")
    if re.search('^[#;]',line) or re.search('^$',line):
#     if not re.search('^[#;]',line) and not re.search('^$',line):
        print line
