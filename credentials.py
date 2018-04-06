
def getCreds(isLab):

	if (isLab):
	        paciUsername, paciPassword = ('admin', 'XXXXX')
        	paciUrl = "http://10.10.20.9:4465/paci/v1.0/"
	        pcsUsername, pcsPassword = ('root', 'XXXXX')
	        pbaUrl = "http://10.10.20.7:5224/RPC2";
	        pbaUsername, pbaPassword = ('user', 'XXXXX')
		poaIp  = "10.10.20.10"
		subdomain = "lab.example.com"
	        #ids = [51, 52, 53]
	        ids = [51, 52, 53, 80, 81, 82]
	else:   
	        paciUsername, paciPassword = ('admin', 'XXXXX')
        	#paciUrl = "http://10.10.0.8:4465/paci/v1.0/"
        	paciUrl = "https://10.10.0.8:4475/paci/v1.0/"
	        pcsUsername, pcsPassword = ('root', 'XXXXX')
	        pbaUrl = "http://10.10.0.6:5224/RPC2";
	        pbaUsername, pbaPassword = ('user', 'XXXXX')
		poaIp  = "10.10.0.9"
		subdomain = "example.com"
        	#ids = [41, 43, 44]
        	ids = [41, 43, 44, 47, 48, 49]

	return paciUrl, paciUsername, paciPassword, pcsUsername, pcsPassword, pbaUrl, pbaUsername, pbaPassword, ids, poaIp, subdomain
