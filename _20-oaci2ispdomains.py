#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import json
import re
import socket
import subprocess
import sys
import variables_iddomainslist
from urllib2 import urlopen
from variables_billmgrvars import * 

subprocess.call(["/usr/bin/clear"])

#######################################################################
######################## Variables ####################################
#######################################################################

# List with all user IDs. It's ID could be found in Billmanager -> Clients -> Clients -> Id column.
usersIDlist = []
# Dictionary with all user email:ID (key:value). It could be found in Billmanager -> Clients -> Clients -> Name(email part):Id
usersIDmaildict = {}
# List with all users active ID sessions. It could be found in Billmanager -> System Status -> Active sessions -> Session ID
sessionsIDlist = []
# List with all active users sessions, pairs are email:ID (key:value).
sessionsIDmaildict = {}

# These variables must be defined or changed in variables_billmgrvars.py file in the same directory. Don't uncomment! 
# Billmanager IP
# panelIP = '212.24.37.254'
# Dnsmanager IP
# dnsmgrIP = '212.24.37.248'
# dnsmgrPort = '1500'
# Dnsmanager slave IP
# dnsmgrS_IP = '212.24.43.88'
# Billmanager login and password
# login = 'root'
# password = 'equie4Eeph'

# URLs for requests in Billmanager and Dnsmanager
url = "https://" + panelIP + "/billmgr?authinfo=" + login + ":" + password + "&out=json&sform=ajax"
dnsmgr_url = "https://" + dnsmgrIP + ":" + dnsmgrPort + "/dnsmgr?authinfo="
# URL for login with authID, instead of login:password pair
user_login_url = "https://" + panelIP + "/billmgr?auth="
# List of OACI's clients ID and their domains.
imported_list = variables_iddomainslist.all_pull

#######################################################################
######################## Functions ####################################
#######################################################################

# Start session for each user from usersIDlist by client ID.
def sessions_start():
# Debug: starting session only for 2 users (ID 12, 13). Manage comments by yourself.
#        for clientID in usersIDlist:
#		print bcolors.OKBLUE + "Session for user ID " + str(clientID) + " starting.." + bcolors.ENDC
#                start_session_url = url + "&func=account.su&elid=" + str(clientID)
#                start_session_res = urlopen(start_session_url)
	print bcolors.OKBLUE + "Starting sessions.." + bcolors.ENDC
	start_session_url = url + "&func=account.su&elid=12"
	start_session_res = urlopen(start_session_url)
	start_session_url = url + "&func=account.su&elid=13"
	start_session_res = urlopen(start_session_url)

# Finish all users sessions (expect admin and root) by sessionID list.
def sessions_finish():
        if (len(sessionsIDlist) == 0):
                print "Sessions ID list is empty. I have no data to stop any session."
                sys.exit(1)
	for sessionID in sessionsIDlist:
		stop_session_url = url + "&elid=" + sessionID + "&func=session.delete"
		stop_session_res = urlopen(stop_session_url)

# Check if ports are open on the destination hosts 
def isOpen(ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, int(port)))
        if result == 0:
                return True
        else:
                return False

# Colored text
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

#######################################################################
###################### Starting Tests #################################
#######################################################################
# Check if Billmanager, Dnsmanager and Dnsmanager slave are available on 1500 ports. DNSes on port 53.
print bcolors.HEADER + "Configuration tests have been started, attention please..\n"
print "********************************************************"
print "    Billmanager IP: " + panelIP
print "    Dnsmanager IP: " + dnsmgrIP
print "    Dnsmanager Slave IP: " + dnsmgrS_IP
print "    Billmanager username: " + login
print "    Billmanager password: **********" + bcolors.ENDC
print bcolors.HEADER + "--------------------------------------------------------" + bcolors.ENDC
print bcolors.HEADER + bcolors.BOLD + "    Check it please. \n    You can stop the script and edit variables in the variables_billmgrvars.py file (it is in the same directory). \n    Is it correct? (yes/no)" + bcolors.ENDC
exitter = 0
while (exitter == 0):
	p = raw_input("What to do? ")
	if (p == "yes" or p == "y"):
		exitter = 1
	elif (p == "no" or p == "n"):
		exitter = 1
		print bcolors.FAIL + "    Terminated by user. Bye-bye" + bcolors.ENDC
		sys.exit(1)
	else:
		print ("Incorrect input.")
service_resultDict = {}
dnslist = [dnsmgrIP, dnsmgrS_IP]
fail_counter = 0
service_resultDict = dict.fromkeys([panelIP, dnsmgrIP, dnsmgrS_IP])
for key in service_resultDict.keys():
        if (isOpen(key, 1500)):
                service_resultDict[key] = 0
        else:
                service_resultDict[key] = 1
if (isOpen(panelIP, 3306)):
	print bcolors.OKGREEN + "OK: Service with IP " + panelIP + " port 3306 reachable." + bcolors.ENDC
else:
	fail_counter = fail_counter + 1
	print bcolors.FAIL + "Warning: Service with IP " + panelIP + " port 3306 unreachable!" + bcolora.ENDC
for key, value in service_resultDict.iteritems():
        if value == 1:
                print bcolors.FAIL + "Warning: Service with IP " + key + " port 1500 unreachable!" + bcolors.ENDC
		fail_counter = fail_counter + 1
        else:
                print bcolors.OKGREEN + "OK: Service with IP " + key + " port 1500 reachable." + bcolors.ENDC
for dns in dnslist:
	if (isOpen(dns, 53)):
		print bcolors.OKGREEN + "OK: Service with IP " + dns + " port 53 reachable." + bcolors.ENDC
	else:
		print bcolors.FAIL + "Warning: Service with IP " + dns + " port 53 unreachable!" + bcolors.ENDC
		fail_counter = fail_counter + 1
print "\nTry to log in the Billmanager with login and password.."
url_res = urlopen(url)
jurl_res = json.load(url_res)
if ("error" in jurl_res['doc'].keys()):
	print bcolors.FAIL + "Warning: Can't log in. Please, check login and password variables in the beginning of the script, it must me incorrect." + bcolors.ENDC
	fail_counter = fail_counter + 1
else:
	print bcolors.OKGREEN + "OK: Logged in successfully" + bcolors.ENDC
if (fail_counter > 0):
	print bcolors.BOLD + "Fix the services above and start script again." + bcolors.ENDC
	sys.exit(1)
print bcolors.HEADER + "Finished. Main programm will start in 3 seconds.."
print "********************************************************\n\n\n" + bcolors.ENDC
#######################################################################
########################### Main ######################################
#######################################################################

# JSON with all the users on the Billmanager (will get 'account_id' and 'emails' fields from it).
print bcolors.OKBLUE + "Generate the list with all clients ID and the dictionary with all pairs email:clientID.." + bcolors.ENDC
get_clients_url = url + "&func=user"
get_clients_res = urlopen(get_clients_url)
jget_clients_res = json.load(get_clients_res)

# Parse JSON and get 'account_id' and 'emails' fields. Put them into the list and dictionary.
clients_list = jget_clients_res['doc']['elem']
clients_count = len(clients_list)
# Print total count of users.
print bcolors.HEADER + "Total users: " + str(clients_count) + bcolors.ENDC
for client in clients_list:
	usersIDlist.append(client['account_id']['$'])
	dictkeyEmail = client['email']['$']
	dictvalueAccountID = client['account_id']['$']
	usersIDmaildict[dictkeyEmail] = dictvalueAccountID

# Start one session for each user in usersIDlist.
sessions_start()

# JSON with all current session IDs (will get 'SID' to be able to login with it as user).
# List example of the SIDs: [2ad18418f410, 3ff99213a112]
print bcolors.OKBLUE + "Generate the list with all session IDs and the dictionary with all pairs email:sessionID.." + bcolors.ENDC
get_sessionID_url = url + "&func=session"
get_sessionID_res = urlopen(get_sessionID_url)
jget_sessionID_res = json.load(get_sessionID_res)
sessions_list = jget_sessionID_res['doc']['elem']

# Parse JSON and get 'sessionID' and 'email'. Put them into the list and dictionary.
# IF condition ignores the user session ID "admin" and "root". We must not terminate their sessions.
for session in sessions_list:
	if ("admi" in str(session['name']['$']) or "root" in str(session['name']['$']) or "savin" in str(session['name']['$']) or "naumushkin" in str(session['name']['$'])):
		pass
	else:
		sessionsIDlist.append(session['id']['$'])
		sessionEmail = session['name']['$']
		sessionID = session['id']['$']
		sessionsIDmaildict[sessionEmail] = sessionID

# Log in with sessionID as users. Here I'm using two dictionaries: sessionsIDmaildict(email:sessionID) and usersIDmaildict(email:clientID). I need this to know what name I logged in by. Comparing the keys I'll be able to parse the list of the OACI's users with their domains.
print bcolors.OKGREEN + "\nWe are ready to log in by the each user and place an order." + bcolors.ENDC
for authID in sessionsIDlist:
	for email, sessionID in sessionsIDmaildict.iteritems():
		if sessionID == authID:
			userEmail = email
			for mailkeys in usersIDmaildict.keys():
				if mailkeys in userEmail:
					currentAccountID = usersIDmaildict[mailkeys]
	try:
		print bcolors.OKBLUE + "Log in with " + authID + " authID, user email: " + userEmail + ", client ID is: " + currentAccountID + bcolors.ENDC
	except Exception:
		print bcolors.FAIL + "\nWarning: Script running error. Please, check that there are no active users sessions in Billmanager and try again. (System status -> Active sessions menu)" + bcolors.ENDC
		print bcolors.HEADER + "\nDo you want to close all sessions and continue (y/n?)" + bcolors.ENDC
		exitter = 0
		while (exitter == 0):
        		p = raw_input("What to do? ")
        		if (p == "yes" or p == "y"):
                		exitter = 1
				sessions_finish()
				print bcolors.OKGEEN + "All sessions stopped. Restart script now." + bcolors.ENDC
				sys.exit(0)
        		elif (p == "no" or p == "n"):
                		exitter = 1
                		print bcolors.FAIL + "    Terminated by user. Bye-bye" + bcolors.ENDC
                		sys.exit(1)
        		else:
                		print ("Incorrect input.")
	print bcolors.OKBLUE + "Ordering the service.." + bcolors.ENDC

# Check if the service ordered already
	fails = 0
	check_DNSservice_url = user_login_url + authID + "&out=json&func=dnshost"
	check_DNSservice_res = urlopen(check_DNSservice_url)
	jcheck_DNSservice_res = json.load(check_DNSservice_res)
#	if ('item_status' not in jcheck_DNSservice_res['doc']['elem'][0].keys()):
	if ('elem' not in jcheck_DNSservice_res['doc'].keys()):
		pass
	else:
		fails = fails + 1
		print bcolors.FAIL + "Warning: There are " + str(len(jcheck_DNSservice_res['doc']['elem'])) + " DNS hosting services.." + bcolors.ENDC
		for DNSservice in jcheck_DNSservice_res['doc']['elem']:
			if (DNSservice['item_status']['$color'] == 'green'):
				print bcolors.FAIL + "\nWarning: Found DNS hosting service is in Active status!" + bcolors.ENDC
			else:
				print bcolors.FAIL + "\nWarning: Found DNS hosting service is not in Active status!" + bcolors.ENDC
	if (fails > 0):
		print bcolors.FAIL + "\nWhat should we do? \nType \"ignore\" - script will ignore found services. Creates new once and add domains to it. \nType \"stop\" - script will be terminated, and you will be able to edit found services by yourself. \nType \"repair\" and script will remove all found DNS hosting services, create new and add domains to it. \nType \"skip\" - script will pass current user and goes to the next." + bcolors.ENDC
		exitter = 0
		while (exitter == 0):
        		p = raw_input("What to do now? ")
	        	if (p == "ignore"):
				exitter = 1
				print bcolors.HEADER + "\nIgnoring..." + bcolors.ENDC
				pass
	        	elif (p == "stop"):
				exitter = 1
				print bcolors.HEADER + "\nTerminating script..." + bcolors.ENDC
                		sessions_finish()
				sys.exit(0)
			elif (p == "repair"):
				exitter = 1
				print bcolors.HEADER + "\nRemoving found DNS hosting service(s)..." + bcolors.ENDC
				for DNSservice in jcheck_DNSservice_res['doc']['elem']:
					DNShostingID = DNSservice['id']['$']
					service_delete_url = user_login_url + authID + "&out=json&elid=" + DNShostingID + "&func=dnshost.delete&plid="
					urlopen(service_delete_url)
					print bcolors.HEADER + "DNS hosting service with ID " + DNShostingID + " has been removed." + bcolors.ENDC
				print bcolors.OKGREEN + "\nRepaired user successfully. Now create new service, and domains for it.." + bcolors.ENDC
			elif (p == "skip"):
				exitter = 1
				print bcolors.HEADER + "\nSkipping this user, goes to the next..." + bcolors.ENDC
        		else:
                		print ("Incorrect input.")
# Check if p == "skip". If it is, we will continue, skip this loop iteration (this user).
	if (p == "skip"):
		continue

# DNS hosting ordering URL. Place an order for 1 year service, with maximum allowed 100 domain zones, automatic renewal available.
	get_dns_url = user_login_url + authID + "&out=json&addon_155=100&autoprolong=12&clicked_button=finish&datacenter=1&func=dnshost.order.param&itemtype=&newbasket=&&period=12&pricelist=154&progressid=false&skipbasket=&sok=ok&stylesheet="
	get_dns_res = urlopen(get_dns_url)
	print bcolors.OKBLUE + "Getting cart ID for apply.." + bcolors.ENDC

# Parse JSON to get cart ID. I need it to apply the order.
	get_basketID_url = user_login_url + authID + "&out=json&func=basket"
	get_basketID_res = urlopen(get_basketID_url)
	jget_basketID_res = json.load(get_basketID_res)
	cartID = jget_basketID_res['doc']['list'][0]['elem'][1]['id']['$']
	print bcolors.OKBLUE + "Applying.." + bcolors.ENDC

# Apply the order with the known cart ID.
	apply_url = user_login_url + authID + "&out=json&clicked_button=free&func=basket&id=" + cartID + "&progressid=false&sok=ok&stylesheet="
	apply_res = urlopen(apply_url)
# We must wait at least 5s untill service will get "Active" status
	subprocess.call(["/bin/sleep", "5"])
	print bcolors.OKGREEN + "Applied. Service status \"Active\"\n" + bcolors.ENDC
	print bcolors.OKBLUE + "Get DNS serviceID, DNSManager username and password.." + bcolors.ENDC

# Get and parse JSON to get an ID of the DNS hosting service. I need it to be able to parse username and password of the user's DNSmanager account
	serviceID = user_login_url + authID + "&out=json&func=dnshost"
	serviceID = urlopen(serviceID)
	jserviceID = json.load(serviceID)
	SID = jserviceID['doc']['elem'][0]['id']['$']
# Get and parse JSON with username and password (automatically generated by the system). We'll need it to log in DNSmanager.
	dnsmgrloginpass_url = user_login_url + authID + "&out=json&elid=" + str(SID) + "&elname=DNS%20Aero%20%23" + str(SID) + "&func=dnshost.edit&plid=&"
	dnsmgrloginpass_res = urlopen(dnsmgrloginpass_url)
	jdnsmgrloginpass_res = json.load(dnsmgrloginpass_res)
	dnsmgrUsername = jdnsmgrloginpass_res['doc']['username']['$']
	dnsmgrPassword = jdnsmgrloginpass_res['doc']['password']['$']
	
# Log in to the DNSmanager. Create domains from `imported_list` identified by OACI's client ID (must be equal ISP's client ID).
	for oaci_userID in imported_list:
# ATTENTION! CHECK YOUR variables_iddomainslist.py FILE! IF THERE ARE NO clientIDs EQUAL TO ISP'S clientIDs, SCRIPT WILL NOT SAY IT, JUST CONTINUE WORK WITHOUT CREATING DOMAINS!
		if (str(oaci_userID[0]) != str(currentAccountID)):
			pass
		else:
			for domainname in oaci_userID[1]:
				domainname = domainname.replace("'", "").encode('idna')
				print bcolors.OKBLUE + "    Logged in DNSmanager, create domain " + domainname + bcolors.ENDC
# Create domain URL. DNSmanager will create default empty file in /var/named/caravan.ru/domain.ltd. But we'll overwrite it by the `cp` next.
				create_domain_url = dnsmgr_url + str(dnsmgrUsername) + ":" + str(dnsmgrPassword) + "&out=json&clicked_button=ok&dtype=master&func=domain.edit&ip=&masterip=&name=" + domainname + "&progressid=false&sok=ok&zoom-ip="
				urlopen(create_domain_url)
				print bcolors.HEADER + "    Replacing default zone file with the user's once.." + bcolors.ENDC
				subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/bin/cp", "/root/rsyncdst/" + domainname, "/var/named/domains/caravan.ru/" + domainname])
				print bcolors.HEADER + "    Reloading named to read new zone file.." + bcolors.ENDC
				subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/sbin/rndc", "reconfig"])
                		subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/sbin/rndc", "reload", domainname + ".", "in", "caravan.ru"])
				print bcolors.HEADER + "    Checking zone with dig. 5 retries.." + bcolors.ENDC
				subprocess.call(["/root/scripts/billmanager/help_digcheck.sh", domainname, dnsmgrIP])
				subprocess.call(["/root/scripts/billmanager/help_digcheck.sh", domainname, dnsmgrS_IP])
                		print bcolors.OKGREEN + "    [Finished]" + bcolors.ENDC
                		print ("")

# Edit /etc/named.conf and /usr/local/mgr5/etc/ihttpd.conf with sed, like: sed -i.bak 's/212.24.37.248/212.24.37.249/g' /usr/local/mgr5/etc/ihttpd.conf
print bcolors.HEADER + " With sed, change /etc/named.conf and /usr/local/mgr5/etc/ihttpd.conf files..." + bcolors.ENDC
subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/bin/sed", "-i.bak", "'s/" + dnsmgrIP + "/" + ns1 + "/g'", "/usr/local/mgr5/etc/ihttpd.conf"])
subprocess.call(["/usr/bin/ssh", dnsmgrIP, "/usr/bin/sed", "-i.bak", "'s/" + dnsmgrIP + "/" + ns1 + "/g;s/" + dnsmgrS_IP + "/" + ns2 + "/g'", "/etc/named.conf"])
subprocess.call(["/usr/bin/ssh", dnsmgrS_IP, "/usr/bin/sed", "-i.bak", "'s/" + dnsmgrS_IP + "/" + ns2 + "/g'", "/usr/local/mgr5/etc/ihttpd.conf"])
subprocess.call(["/usr/bin/ssh", dnsmgrS_IP, "/usr/bin/sed", "-i.bak", "'s/" + dnsmgrIP + "/" + ns1 + "/g;s/" + dnsmgrS_IP + "/" + ns2 + "/g'", "/etc/named.conf"])
print bcolors.OKGREEN + "OK." + bcolors.ENDC

#Log out each all the users
print bcolors.OKGREEN + "Done." + bcolors.ENDC
sessions_finish()
sys.exit(0)
