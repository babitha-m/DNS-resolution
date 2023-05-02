import socket

# Constants for DNS queries and OpenDNS resolver
DNS_PORT = 53
DNS_SERVER = "208.67.222.222"  # OpenDNS resolver

# Create a UDP socket to receive DNS queries from client
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("192.168.29.27", DNS_PORT))
print("Server running on port 53")
while True:
    # Wait for DNS query from client
    request, client_addr = sock.recvfrom(1024)

    # Send DNS query to OpenDNS resolver
    resolver_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    resolver_sock.sendto(request, (DNS_SERVER, DNS_PORT))

    # Wait for response from OpenDNS resolver
    response, _ = resolver_sock.recvfrom(1024)

    # Parse the IP address from the DNS response
    ip_address = socket.inet_ntoa(response[-4:])

    # Send IP address back to client
    sock.sendto(ip_address.encode(), client_addr)
