import ipaddress

def iprangefinder(ipcidr):
	for ip in ipaddress.IPv4Network(ipcidr):
		print(ip)
	for ip in ipaddress.IPv6Network(ipcidr):
        	print(ip)

	
