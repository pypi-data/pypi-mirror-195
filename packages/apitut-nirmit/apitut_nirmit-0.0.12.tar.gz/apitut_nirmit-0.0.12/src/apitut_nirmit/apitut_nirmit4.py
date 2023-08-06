import ipaddress

def iprangefinder(ipcidr):
	try:
        	# Try to create an IPv4 address object
		ipaddress.IPv4Address(ip_address)
		# If no exception was raised, it's an IPv6 address
		print("IPv4")
		network6 = ipaddress.IPv4Network(ipcidr)
		# Exclude the network address and the broadcast address
		first_ip4 = network4.network_address + 1
		last_ip4 = network4.broadcast_address - 1
		for ip in range(int(first_ip4), int(last_ip4) + 1):
			print("Printing IPv4 addresses.")
			print(ipaddress.IPv4Address(ip))
	except ipaddress.AddressValueError:
		pass
	#Similarly for ipv6
	try:
		# Try to create an IPv6 address object
		ipaddress.IPv6Address(ip_address)
		# If no exception was raised, it's an IPv6 address
		print("IPv6")
		network6 = ipaddress.IPv6Network(ipcidr)
		# Exclude the network address and the broadcast address
		first_ip6 = network6.network_address + 1
		last_ip6 = network6.broadcast_address - 1
		for ip in range(int(first_ip6), int(last_ip6) + 1):
			print("Printing IPv6 addresses.")
			print(ipaddress.IPv6Address(ip))
	except ipaddress.AddressValueError:
		pass
	# If both attempts failed, it's not a valid IP address
	return "Invalid"
