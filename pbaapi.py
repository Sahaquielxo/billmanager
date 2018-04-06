import logging
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib2, base64
import sys
import socket

import xmlrpclib

class ApiPBA:

	def __init__(self, url, username, password):
		self.url = url
		self.username = username
		self.password = password

	def doInit(self):
		self.Server = xmlrpclib.ServerProxy(self.url, verbose = False)


	def formData(self, name, params):
		data = {}
		data['Server'] = "BM"
		data['Method'] = name
		data['Params'] = params
                data['Lang'] = 'ru'

		return data

	def formDataWithCredentials(self, name, params):
		data = self.formData(name, params)
		
		data['Username'] = self.username
		data['Password'] = self.password

		return data
		
	def executeWithCredentials(self, name, params):
		data = self.formDataWithCredentials(name, params)

		return self.executeInt(data)

	def execute(self, name, params):
		data = self.formData(name, params)

		return self.executeInt(data)

	def executeInt(self, data):
		try:
			rv = self.Server.Execute(data)
		except xmlrpclib.Fault, err:
			logging.error("PBA xml error: " + str(err.faultString))
			return None
		except socket.error:
			logging.error("PBA connect error")
			return None

		if (not 'Result' in rv):
			logging.error("PBA invalid result")
			return None

		return rv['Result'][0]

        def updatePeriod(self, data):
		response = self.executeWithCredentials("PlanPeriodUpdate", data)
                if (response is None):
                    return False

                if ('Status' in response):
                    return True

                return False
                

        def getPeriod(self, planId):
		response = self.execute("PlanPeriodGet", [planId, 1])
                if (response is None):
                    return False

                return response

        def getPeriods(self, planId):
		response = self.execute("PlanPeriodListGet_API", [planId, 1])
                if (response is None):
                    return False

                return response


        def getPlans(self, catId):
		response = self.execute("PlanListAvailableGet_API", [1000002, 'PEMGATE', catId, 1])
                if (response is None):
                    return False

                return response
                

	def getHostingSubscriptionsEx(self, hostingPlanIds):
		subscriptions = self.getSubscriptions() 
		if (subscriptions is None):
			return False

		needed = []
		for subscriptionId in subscriptions:
			response = self.execute("SubscriptionDetailsGetEx_API", [subscriptionId])
			if (response is None):
				return False
			
			id = response[3]
			if (id in hostingPlanIds):
                                needed.append(response)

		return needed

                

	def getHostingSubscriptions(self, hostingPlanIds):
		subscriptions = self.getSubscriptions() 
		if (subscriptions is None):
			return False

		needed = []
		for subscriptionId in subscriptions:
			response = self.execute("SubscriptionDetailsGet_API", [subscriptionId])
			if (response is None):
				return False
			
			id = response[3]
			if (id in hostingPlanIds):
                                needed.append(subscriptionId)

		return needed

        def getSubscriptionDetails(self, subscriptionId):
                response = self.execute("SubscriptionDetailsGet_API", [subscriptionId])

		if (response is None):
			return False

                return response

        def getSubscriptionHistory(self, subscriptionId):
                # 3 - is sorted by 3rd element -> time
		response = self.execute("GetServStatusHist", [subscriptionId, 3])

		if (response is None):
			return False

                return response            

	def isSubscriptionTrial(self, subscriptionId):
		response = self.execute("SubscriptionDetailsGet_API", [subscriptionId])

		#print subscriptionId, response
		if (response is None):
			return False

		return True if (response[5] == 15) else False


        def updateSubscriptionStatus(self, subscriptionId, subStatus, srvStatus):
		response = self.execute("SubscriptionStatusUpdate_API", [subscriptionId, subStatus, srvStatus])
	
        	if (response is None):
			return False
            
                return True

	def blockSubscription(self, subscriptionId):
		response = self.execute("SubscriptionStop_API", [subscriptionId, "Automatic block due to resource overuse"])
	
		if (response is None):
			return False
		
		return True

        def getSubscriptionDates(self, subscriptionId):
		response = self.executeWithCredentials("SubscriptionDetailsGetEx_API", [subscriptionId])
		if (response is None):
			return None

                return response

        def getAccountDetails(self, accountId):
		response = self.executeWithCredentials("AccountDetailsGet_API", [accountId])
		if (response is None):
			return ""

                return response

	def getAccountEmailBySubscription(self, subscriptionId):
		response = self.executeWithCredentials("SubscriptionDetailsGet_API", [subscriptionId])
		if (response is None):
			return ""

		accountId = response[2]
		response = self.executeWithCredentials("AccountDetailsGet_API", [accountId])
		if (response is None):
			return ""

		email = response[13]
		return [accountId, email]

		

	def getSubscriptions(self):
		response = self.executeWithCredentials("SubscriptionGetSubscriptionMenuList", [])
	
		if (response is None):
			return []
		
		# We get all subscriptions here (not only TRIAL) to be able to deal with common tasks
		data = [ x[0] for x in response ]

		return data

	def getSubscriptionAutoRenew(self, subscriptionId):
		response = self.executeWithCredentials("SubscriptionGet", [subscriptionId])
		return response

        def getAccountEmails(self, id):
		response = self.executeWithCredentials("AccountExtendedDetailsGet_API", [id])
            
		if (response is None):
			return []
            
                data = [response[12], response[24], response[36]]

                response = self.executeWithCredentials("GetUsersListForAccount_API", [id, 1])
		if (response is None):
			return data

                for user in response:
                        userId = user[0]
                        nr = self.executeWithCredentials("UserDetailsGet_API", [userId])
        		if (nr is None):
	        		continue
            
                        email = nr[6]
                        data.append(email)

                return data

        def getAccountListByCustomAttribute(self, name, value):
                response = self.executeWithCredentials("GetAccountListByCustomAttribute_API", [name, value, 0])

                if (response is None):
                        return []
    
                return response

        def getCLOrders(self):
                response = self.executeWithCredentials("OrderByStatusListGet_API", [1000002, "CF", "", 0, 0])
		if (response is None):
			return []

                data = []
                for order in response:
                        oitem = {}
                        oitem['id'], oitem['status'], oitem['number'], oitem['customer'], oitem['sales'], oitem['comment'] = order[0], order[4], order[1], order[2], order[17], order[18]
                        data.append(oitem)
                
                return data

        def getFailedOrders(self):
                response = self.executeWithCredentials("OrderByStatusListGet_API", [1000002, "", "PF", 0, 0])

		if (response is None):
			return []
        
                data = []
                for order in response:
                        oitem = {}  
                        oitem['id'], oitem['number'], oitem['customer'], oitem['sales'], oitem['comment'] = order[0], order[1], order[2], order[17], order[18]
                        data.append(oitem)
    
                response = self.executeWithCredentials("OrderByStatusListGet_API", [1000002, "", "SF", 0, 0])
		if (response is None):
			return data

                for order in response:
                        oitem = {}  
                        oitem['id'], oitem['number'], oitem['customer'], oitem['sales'], oitem['comment'] = order[0], order[1], order[2], order[17], order[18]
                        data.append(oitem)

                return data

        def getOrderSKUs(self, id):
                response = self.executeWithCredentials("OrderFinDetailsListGetExt_API", [id, 0])
                if (response is None):
                        return False
        
                skus = []
                for order in response:
                        sku = order[1]
                        skus.append(sku)
    
                return skus

        def getAccounts(self):
                response = self.executeWithCredentials("AccountGetMyCustomersList", [])

		if (response is None):
			return []

		data = [ x[0] for x in response ]

                return data


	def getFullAccounts(self):
		response = self.executeWithCredentials("AccountGetMyCustomersList", [])
		if (response is None):
			return []

		return response
        
        def updateObjAttr(self, accountId, name, value):
                response = self.executeWithCredentials("UpdateObjAttrList_API", [0, accountId, name, value])
    
                return 

        def getObjAttrList(self, accountId):
                response = self.executeWithCredentials("GetObjAttrList_API", [0, accountId, 1])
            
		if (response is None):
			return []

		data = [ x[0] for x in response ]

                return data

        def getAccountBalances(self):
                response = self.executeWithCredentials("GetAccountBalanceList", [])
        
                return response
            

	def close(self):
		pass
 
        def CustomerSubscriptionList(self, accountId, value):
                response = self.executeWithCredentials("GetCustomerSubscriptionList_API", [accountId, value])
                return response

        def getSubscriptionsByPlanId(self, planId):
            response = self.executeWithCredentials("SubscriptionPlan_GetSubscriptionList", [planId, 0])

            if (response is None):
                return []

            return response
