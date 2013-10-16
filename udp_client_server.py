"""
Simple UDP client and server.

Client connects and sends a simple message.
Server randomly drops packets to simulate actual network packet loss.
Simple delay timer mechanism.
Reference: Foundations of Python Network Programming
"""

#!/usr/bin/env python

import socket
import sys
import optparse
import random


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
DELAY = 0.1

def send_line(sock, line, delay):
  while True:
    sock.send(line) # send them one by one
    print '  [-] Waiting up to', delay, 'seconds for a reply.'
    sock.settimeout(delay)
    try:
      data = sock.recv(MAX)
      print '  [+] The server says', repr(data) # print server reply for each recieved lin
      print
      return True # Success
    except socket.timeout:
      delay *= 2 # wait longer
      if delay > 2.0:
        raise RuntimeError('[-] No reply. Server seems down')
    except:
      raise # a real error so let user see it




# Arg. Parser
parser = optparse.OptionParser('usage %prog -s [-i <interface>] | -c -H <hostname>')
parser.add_option('-s', '--server', action='store_false', dest='client', default=True, help=\
'Run as server.')
parser.add_option('-c', '--client', action='store_true', dest='client', help=\
'Run as client.', default=True)
parser.add_option('-i', '--interface', action='store', dest='interface', help=\
'IP interface to bind to. Leave empty for any.', default='0')
parser.add_option('-p', '--port', action='store', dest='port', help=\
'Port to bind to. Leave empty for 1600.', default='1600')
parser.add_option('-H', '--host', action='store', dest='hostname', help=\
'Server hostname or address.')
parser.add_option('-f', '--file', action='store', dest='dataFile', help=\
'File to send to server.')
(options, args) = parser.parse_args()

# If run in client mode
if options.client and options.hostname:
  print '[*] Client Mode: '
  s.connect((options.hostname, int(options.port)))
  # print '  Client socket name: ', s.getsockname()
  # If a file has been specified
  if options.dataFile:
    f = open(options.dataFile, 'r')
    for line in f.readlines(): # loop over all lines
      send_line(s, line.strip('\n'), DELAY)
    f.close() # close the file
  else: # if no file is specified, print usage and exit 
      # To do: send data from stdin
      #for line in sys.stdin:
      #  send_line(s, line, DELAY)
    parser.print_help()
    exit(0) 

# if run in server mode
elif not options.client and options.interface:
  print '[*] Server Mode: '
  s.bind((options.interface, int(options.port)))
  print '  [+] Listening at: ', s.getsockname()
  while True:
    data, address = s.recvfrom(MAX)
    if random.randint(0,2) < 2: # drop approx. 1/3 of recieved packets  
      print
      print '  [+] Listening to client: ', address
      print '  [+]  Data: ', repr(data)
      s.sendto('Your data was %d bytes' % len(data), address)
    else:
      print
      print '  [-] Pretending to drop packet from', address

# In case of incorrect args
else:
  parser.print_help()
  exit(0)
