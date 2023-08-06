import ipaddress

def iprangefinder(ipcidr):
	network4 = ipaddress.IPv4Network(ipcidr)
	# Exclude the network address and the broadcast address
	first_ip4 = network4.network_address + 1
	last_ip4 = network4.broadcast_address - 1
	#Similarly for ipv6
	network6 = ipaddress.IPv6Network(ipcidr)
# Exclude the network address and the broadcast address
	first_ip6 = network6.network_address + 1
	last_ip6 = network6.broadcast_address - 1
	for ip in range(int(first_ip4), int(last_ip4) + 1):
		print("Printing IPv4 addresses.")
		print(ipaddress.IPv4Address(ip))
	for ip in range(int(first_ip6), int(last_ip6) + 1):
		print("Printing IPv6 addresses.")
        	print(ipaddress.IPv6Address(ip))
