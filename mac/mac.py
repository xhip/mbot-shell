# coding=utf-8

import re
import sys
import requests

#---[ Configs ]---
# Command: !mac | Arg's: {n} {}
#../mylib.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mylib import print_console
#-----------------

# Manual
def man():
	# python mac.py <nick> <mac address>
	print_console('Usage: !mac <mac address>')
	exit(-1)

# If Error
def err(why):
	print_console('\0034*\003 Error - \002{0}\002'.format(why))
	exit(-1)

# API Get Info
def get(nick,mac):

	# Request Data
	r = requests.get('http://www.macvendorlookup.com/api/v2/{0}'.format(mac))
	
	# Check Status
	if r.status_code == 200:

		# Check Data
		j = r.json()
		if 'company' in j[0]:
			c = j[0]['company']
			if c != None:
				info = 'belongs to: \002"{0}"\002'.format(c)
			else:
				err("Company Empty")
		else:
			err("Company missing")

	# No match in API database
	elif r.status_code == 204:
		info = 'returned: \002"No Match Found!"\002'

	# Error
	else:
		err('returned: {0} Status Code'.format(r.status_code))

	# Send Info
	print_console(' \0033*\003 {0}\'s query mac: \002"{1}"\002 {2}'.format(nick,mac,info))
	return


# Main
if len(sys.argv) < 3:
    man()
else:

	# Get Nick
	mask = sys.argv[1]
	nick = mask.split("!")[0]

	# Check Mac
	m = re.search('([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})', sys.argv[2])
	if m:
		mac = m.group(0).upper()
		get(nick,mac)
	else:
		err('MAC Address Invalid!')
