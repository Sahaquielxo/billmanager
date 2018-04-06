#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import re
import socket
import subprocess
import sys
import iddomainslist
from urllib2 import urlopen

url = 'https://212.24.37.254/billmgr?auth=141818b8a174&out=json&sform=ajax&func=dnshost'
url2 = 'https://212.24.37.254/billmgr?auth=c78d2ab6226c&out=json&sform=ajax&func=dnshost'
res = urlopen(url)
res2 = urlopen(url2)
jsonRes = json.load(res)
jsonRes2 = json.load(res2)
# print (jsonRes['doc']['elem'][0]['item_status']['$color'])
print (jsonRes['doc'])
print (len(jsonRes['doc']['elem']))
print (jsonRes['doc']['elem'][0]['id']['$'])
print ("")
# print (jsonRes2['doc']['elem'])
