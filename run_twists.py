#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess

twistmon = os.path.join(os.getcwd(), "twistweb")
scanpath = os.path.join(twistmon, "scans")
dfile = os.path.join(twistmon, "domains.txt")
args = './dnstwist.py --mxcheck --geoip --registered --ssdeep --threads 25 --tld dictionaries/common_tlds.dict --format csv'

domains = open(dfile, 'r').readlines()
for domain in domains:
    cfile = "{}.csv".format(domain.strip())
    output = os.path.join(scanpath, cfile)
    arguments = "{} {} >> {}".format(args, domain, output)
    data = subprocess.Popen([arguments], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    data.communicate()
