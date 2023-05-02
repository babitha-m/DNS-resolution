import socket
import struct

# Constants for DNS queries and OpenDNS resolver
DNS_PORT = 53
DNS_SERVER = "0.0.0.0"  # You need to add the server computer's IP address here.

# Create a UDP socket to send DNS query to server
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get domain name from user input
domain_name = input("Enter domain name: ")

# Construct DNS query message
transaction_id = 1234
flags = 256
question_count = 1
answer_count = 0
authority_count = 0
additional_count = 0

# Convert domain name to DNS format
dns_name = b''
for label in domain_name.split('.'):
    dns_name += struct.pack('B', len(label)) + label.encode()
dns_name += b'\x00'

# Construct DNS query message
dns_query = struct.pack('!HHHHHH', transaction_id, flags, question_count,
                        answer_count, authority_count, additional_count)
dns_query += dns_name
dns_query += struct.pack('!H', 1)  # Query type A
dns_query += struct.pack('!H', 1)  # Query class IN

# Send DNS query to OpenDNS resolver
sock.sendto(dns_query, (DNS_SERVER, DNS_PORT))

# Receive DNS response from server
response, _ = sock.recvfrom(1024)

# Extract the resource record from the DNS response
transaction_id, flags, question_count, answer_count, authority_count, additional_count = struct.unpack('!HHHHHH', response[:12])
answer_section = response[12:]

# Extract the domain name from the question section
domain_name = b''
pos = 0
label_length = answer_section[pos]
while label_length != 0:
    if (label_length & 0xc0) == 0xc0:  # pointer
        pos = struct.unpack('!H', answer_section[pos:pos+2])[0] & 0x3fff
    else:  # label
        domain_name += answer_section[pos+1:pos+1+label_length] + b'.'
        pos += label_length + 1
    label_length = answer_section[pos]

# Convert the domain name to a string
domain_name = domain_name.decode('ascii')[:-1]

# Parse the resource record from the DNS response
answer = answer_section[pos+1:]
rr_type, rr_class, rr_ttl, rdlength = struct.unpack('!HHIH', answer[:10])
resource_record = answer[10:10+rdlength]
# Receive DNS response from server
response, _ = sock.recvfrom(1024)

# Extract IP address from DNS response
ip_address = socket.inet_ntoa(response[-4:])

# Print the resource record
print("Resource Record for", domain_name)
print("IP address for", domain_name, "is", ip_address)
print("Type:", rr_type)
print("Class:", rr_class)
print("TTL:", rr_ttl)
print("Data Length:", rdlength)
print("Resource Data:", resource_record)
