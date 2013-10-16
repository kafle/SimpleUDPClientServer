SimpleUDPClientServer
=====================
A simple command line UDP client server.
Set up for testing UDP packet loss handling mechanisms.

udp_packet_loss.py is incomplete and currently holds functions to assist in packet loss mechanisms. 

Server: python udp_client_server.py -s -p PORT -I INTERFACE

Client: python udp_client_server.py -H HOST -p PORT -f FILE

Run with arg. --help for more usage information.

To do:
 - Send data from standard input
 - Packet loss handling


Reference:
Foundations of Python Network Programming
