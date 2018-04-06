#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import re
import socket
import subprocess
import sys
import variables_iddomainslist
from netaddr import IPAddress
from netaddr.core import  ZEROFILL
from urllib2 import urlopen
from variables_billmgrvars import * 

from pbaapi import ApiPBA
from poaapi import ApiPOA
from credentials import getCreds

url = "https://" + dnsmgrIP + ":" + dnsmgrPort + "/dnsmgr?authinfo=" + resellerlogin + ":" + resellerpass + "&out=json&sform=ajax"

subprocess.call(["/usr/bin/clear"])
subprocess.call(["/root/scripts/billmanager/_31-getPTRs.sh"])
with open ("variables_PTRlist.py") as PTRfile:
	for RRPTR in PTRfile.readlines():
		print "Add " + RRPTR.replace('\n', "") + " zone in dnsmanager..."
		addPTRurl = url + "&clicked_button=ok&dtype=master&email=tech%40caravan.ru&func=domain.edit&ip=&masterip=&name=" + str(RRPTR).replace("-", "%2D").replace('\n', "") + "&progressid=false&sok=ok&zoom-ip="
		urlopen(addPTRurl)
		print "OK, replacing default files with rsynced PTR-zones files..."
		subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/bin/cp", "/root/rsyncdst_rev/" + RRPTR.replace('\n', ""), "/var/named/domains/caravan.ru/" + RRPTR.replace('\n', "")])
PTRfile.close()
subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/bin/systemctl", "restart", "named"])
print "Done."
