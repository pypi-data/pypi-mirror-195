import ipaddress

def iprangefinder(ipcidr):
	try:
        	# Try to create an IPv4 address object
		ipaddress.IPv4Address(ipcidr)
		# If no exception was raised, it's an IPv4 address
		print("IPv4")
		network4 = ipaddress.IPv4Network(ipcidr)
		# Exclude the network address and the broadcast address
		print(f"Network address: {network.network_address}")
		print(f"Broadcast address: {network.broadcast_address}")
		print("Available hosts:")
		for host in network.hosts():
			print(host)
	except ipaddress.AddressValueError:
		pass
	#Similarly for ipv6
	try:
		# Try to create an IPv6 address object
		ipaddress.IPv6Address(ipcidr)
		# If no exception was raised, it's an IPv6 address
		print("IPv6")
		network6 = ipaddress.IPv6Network(ipcidr)
		# Exclude the network address and the broadcast address
		print(f"Network address: {network.network_address}")
		print(f"Broadcast address: {network.broadcast_address}")
		print("Available hosts:")
		for host in network.hosts():
			print(host)
	except ipaddress.AddressValueError:
		pass
	# If both attempts failed, it's not a valid IP address
	return "Invalid"
