# DNS-resolution
DNS query resolution using socket programming

This contains 2 files : client and server which can be run on two different machines . 
You need to configure and bind the IP address of the server machine in the client code.
Client machine connects and sends DNS query which is converted to a UDP socket and sent to the server machine.
The server machine connects to the OpenDNS resolver and gets the resource record which is given back to the client.
The output can be modified in a way that you can print only the required information or the whole RR(resource record).
