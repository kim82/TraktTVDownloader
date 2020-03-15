#!/usr/bin/python
import config
import json
from urllib2 import Request, urlopen, HTTPError
from trakttv import TraktTV

trakt = TraktTV(config.CLIENT_ID, config.CLIENT_SECRET)
trakt.login()
calendar = trakt.calendar(14)

database = {}
try:
	file = open('calendar.db', 'r')
	database = json.load(file)
	file.close()
except Exception as e:
	print e
	database = {}	

for item in calendar:
	id = item['show']['ids']['trakt']
	season = ('0' + str(item['episode']['season']))[-2:]
	number = ('0' + str(item['episode']['number']))[-2:]
	first_aired = item['first_aired']
	title = '{title} S{season}E{episode}'.format(title=item['show']['title'], season=season, episode=number)
	
	dbValue = (item['episode']['season'] * 1000) + item['episode']['number']
	if database[str(id)] < dbValue:
		print title + ' : ' + first_aired[0:10]
		database[str(id)] = dbValue
		
		url = config.IFTTT_MAKER_URL
		header = {'Content-Type':'application/json'}
		data = {"value1": title, "value2": first_aired[0:10]}
		try:
			request = Request(url, json.dumps(data), header)
			print urlopen(request).read()
		except HTTPError as e:
			print e

file = open('calendar.db', 'w')
json.dump(database, file, ensure_ascii=False)
file.close()