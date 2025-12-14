#!/usr/bin/python

# THIS CODE IS PUBLISHED UNDER THE GNU Affero General Public License v3.0
# Originally obtained from gopher://rdlmda.me:70/0/guestbook/guestbook.py
# Mirrored at https://github.com/rdlmda/gopher-guestbook

import os
import sys
import time
from datetime import datetime, timezone
import textwrap
import requests # pip install requests
import csv
import hashlib

csv_file_path = './guestbook.csv'

def wrap(string):
	lines = textwrap.wrap(string, width=67)
	newlines = []
	for line in lines:
		# Fix lines starting with selectors or special chars
		newlines.append(f"i{line}	.")
	return("\n".join(newlines))

def read_entries():
	with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		rows = list(csv_reader)
		for i, row in enumerate(reversed(rows)):
			timestamp = datetime.fromtimestamp(int(row['time']), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
			print(f"{timestamp} (UTC):")
			print()
			print(wrap(f"{row['message']}"))
			print()
			hash = hashlib.sha256(row['ip'].encode()).hexdigest()[0:6]
			is_server = "via a server " if ("true" in (row['proxy'], row['hosting'])) else ""
			print(wrap(f"Someone {is_server}({hash}) located in {row['city']}, {row['country']}"))
			if not (i == len(rows)-1):
				print("\n                                * * *\n")

def add_entry(message):
	ip = os.environ['REMOTE_ADDR']
	ip_data = requests.get(f"http://ip-api.com/line/{ip}?fields=country,city,proxy,hosting").text.splitlines()
	country = ip_data[0]
	city = ip_data[1]
	proxy = ip_data[2]
	hosting = ip_data[3]
	with open(csv_file_path, mode='a', newline='') as file:
        	writer = csv.writer(file)
	        writer.writerow([int(time.time()), ip, country, city, proxy, hosting, message])

# if len(os.environ['QUERY_STRING']) is too long (apparently 1024 minus the length of the location?), errors happen
query = os.environ['QUERY_STRING']
if(query):
	add_entry(query)

read_entries()
