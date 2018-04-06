import logging
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib2, base64
import sys
import socket

import xmlrpclib

import psycopg2

class ApiPOA:

	#def __init__(self, url, username, password):
	def __init__(self, ip):
		self.url = "http://" + ip + ":8440"
		self.ip = ip
#		self.username = username
#		self.password = password

	def doInit(self):
		self.Server = xmlrpclib.ServerProxy(self.url, verbose = False)


	def execute(self, name, params):
		try:
#			rv = self.Server.Execute(data)
			rv = getattr(self.Server, name)(params)
	#		print rv
		except xmlrpclib.Fault, err:
			logging.error("POA error: " + str(err.faultString))
			return None
		except socket.error:
			logging.error("POA connect error")
			return None

		if (not 'status' in rv and not 'result' in rv):
			logging.error("POA invalid result1")
			return None
	
		if (rv['status'] == -1):
#			logging.error("POA invalid result2")
			return None

                if (not 'result' in rv):
                        return rv['status']

		return rv['result']

	def getSubscription(self, id, resources = False):
		data = {}
		data['subscription_id'] = id
		data['get_resources'] = resources

		return self.execute("pem.getSubscription", data)


	def getDomains(self, id):
		data = {}
		data['subscription_id'] = id

		return self.execute("pem.getDomainList", data)

	def removeDomain(self, id):
		data = {}
		data['domain_id'] = id
		data['domain_name'] = 'dummy'

		return self.execute("pem.removeDomain", data)

        def removeSubscription(self, id):
		data = {}
		data['subscription_id'] = id

		return self.execute("pem.removeSubscription", data)
                


	def getPTRs(self):
		#conn = psycopg2.connect("dbname=plesk user=plesk host=" + self.ip)
		print (self.ip)
		conn = psycopg2.connect("dbname=oss user=oss host=" + self.ip)
		cur = conn.cursor()

		#rr_id hostname ip enabled changed_serial sync
		#cur.execute("SELECT rec.rr_id AS rr_id, rec.hostname AS hostname, rec.ip AS ip, rec.enabled AS enabled, rec.changed_serial AS changed_serial , CASE WHEN (rec.changed_serial <= z.serial) AND (z.ns1_serial IS NULL OR rec.changed_serial <= z.ns1_serial) AND (z.ns2_serial IS NULL OR rec.changed_serial <= z.ns2_serial) AND (z.ns3_serial IS NULL OR rec.changed_serial <= z.ns3_serial) THEN 'y' ELSE 'n' END AS sync FROM dns_ptr_records rec JOIN dns_ptr_record_references ref ON (rec.rr_id = ref.rr_id) JOIN dns_reverse_zones z ON (rec.ip BETWEEN z.ip_from AND z.ip_to)")
                cur.execute("SELECT rec.rr_id AS rr_id, rec.hostname AS hostname, rec.ip AS ip, rec.enabled AS enabled  FROM dns_ptr_records rec JOIN dns_ptr_record_references ref ON (rec.rr_id = ref.rr_id) JOIN dns_reverse_zones z ON (rec.ip BETWEEN z.ip_from AND z.ip_to)")
		
		data = cur.fetchall()

		cur.close()
		conn.close()

		return data
	#	print data
		pass
	
	def getPTR(self):
		data = self.getPTRs()

	def updatePTR(self, id, ip, host):
		data = {}
		data['record_id'] = id

		rv = self.execute("pem.removePTRRecord", data)
		if (rv != 1):
			print "errr"
			logging.error("error removing ip")
			return 0

		data = {}
		data['ip_address'] = ip
		data['hostname'] = host 		
		
		return self.execute("pem.addPTRRecord", data)




