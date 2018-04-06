#!/usr/bin/env python

from datetime import datetime
import sys
import time
import os
import urllib

reload(sys)
sys.setdefaultencoding('utf-8')

from pbaapi import ApiPBA
from poaapi import ApiPOA
from credentials import getCreds

isLab = True
# isLab = False
paciUrl, paciUsername, paciPassword, pcsUsername, pcsPassword, pbaUrl, pbaUsername, pbaPassword, ids, poaIp, subdomain = getCreds(isLab)

if (__name__ != "__main__"):
        sys.exit()

pbaApi = ApiPBA(pbaUrl, pbaUsername, pbaPassword)
pbaApi.doInit()

poaApi = ApiPOA(poaIp)
poaApi.doInit()

ns1 = '10.10.20.6'

# Generating output filename
currdate = 0
scriptname = sys.argv[0]
scriptbasename = scriptname[2:-3]
pid = os.getpid()
now = datetime.now()
currdate = now.strftime("%Y%m%d-%H%M%S")
filename = '/root/scripts/output/' + scriptbasename + '.' + str(currdate) + '_' + str(pid)

print ''
print ('Script has beed started')
print ('You will find an output in /root/scripts/output/' + scriptbasename + ' file')
f = open(filename, 'a')

# Get account list 
accounts = pbaApi.getFullAccounts()
# It's count for dynamic counter
accounts_count = len(accounts)
i=0
# Generate file for oaci2isp.py script
f.write ("#!/usr/bin/env python\n")
f.write ("# -*- coding: utf-8 -*-\n")
f.write ("all_pull = ")
# "Level 3 list. I will place 2 more lists inside."
main_l3_list = []
for acs in accounts:
    print ('Running ' + str(i) + '/' + str(accounts_count) + ' checked...')
# "The deepest" list with domains
    domains_list = []
# List with 2 elements: accountID, domains_list variable.
    acc_domains_l2_list = []
    i += 1
# Get subscriptionID by accountID
    sublist = (pbaApi.CustomerSubscriptionList(acs[0], "1"))
    for sublists in sublist:
# Get domains by subscriptionID 
        dns_sub = poaApi.getDomains(sublists[0])
	if (dns_sub):
	    for domains in dns_sub:
# Add domain(s) into the list
		domains_list.append(repr(domains['domain_name']).decode('unicode-escape'))
    if (domains_list):
	    acc_domains_l2_list = [acs[0], domains_list]
	    main_l3_list.append(acc_domains_l2_list) 
	    msg = repr(main_l3_list).decode('unicode-escape')
f.write ("")
f.write ("")
# Write to the file
f.write (msg + '\n')
f.close()
