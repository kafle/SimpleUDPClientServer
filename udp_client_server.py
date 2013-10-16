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


# Arg. Parser
parser = optparse.OptionParser('usage %prog -s [-i <interface>] | -c -H <hostname>')
parser.add_option('-s', '--server', action='store_false', dest='client', default=True, help=\
'Run as server.')
parser.add_option('-c', '--client', action='store_true', dest='client', help=\
'Run as client.', default=True)
parser.add_option('-i', '--interface', action='store', dest='interface', help=\
'IP interface to bind to. Leave empty for any.', default='0')
parser.add_option('-o', '--port', action='store', dest='PORT', help=\
'Port to bind to. Leave empty for 1600.', default='1600')
parser.add_option('-H', '--host', action='store', dest='hostname', help=\
'Server hostname or address.')
parser.add_option('-d', '--data', action='store', dest='message', help=\
'Message to send to server.', default='Default message.')
(options, args) = parser.parse_args()

# If run in client mode
if options.client and options.hostname:
  print 'Client Mode: '
  s.connect((options.hostname, PORT))
  print '  Client socket name: ', s.getsockname()
  delay = 0.1
  while True:
    s.send(options.message)
    print '  Waiting up to', delay, 'seconds for a reply.'
    s.settimeout(delay)
    try:
      data = s.recv(MAX)
    except socket.timeout:
      delay *= 2 # wait longer
      if delay > 2.0:
        raise RuntimeError(' No reply in ' + str(delay) + 's. Server seems down')
    except:
      raise # a real error so let user see it
    else:
      break # no need to loop anymore
  print ' The server says', repr(data)

# if run in server mode
elif not options.client and options.interface:
  print 'Server Mode: '
  s.bind((options.interface, PORT))
  print '  Listening at: ', s.getsockname()
  while True:
    data, address = s.recvfrom(MAX)
    if random.randint(0,1):  
      print '  Listening to client: ', address
      print '  Data: ', repr(data)
      s.sendto('Your data was %d bytes' % len(data), address)
    else:
      print '  Pretending to drop packet from', address

# In case of incorrect arguments
else:
  parser.print_help()
  exit(0)
