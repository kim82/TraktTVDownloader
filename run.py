#!/usr/bin/python
from trakttv import TraktTV
from torrentsearch import ThePirateBay
from transmission import Transmission
from datetime import datetime

CLIENT_ID = 'XXXX'
CLIENT_SECRET = 'YYYY'
TRANSMISSION = 'http://localhost:8081'

try:
	trakt = TraktTV(CLIENT_ID, CLIENT_SECRET)
	trakt.login()
	calendar = trakt.calendar(1)

	transmission = Transmission(TRANSMISSION)
	for item in calendar:
		id = item['show']['ids']['trakt']
		season = ('0' + str(item['episode']['season']))[-2:]
		number = ('0' + str(item['episode']['number']))[-2:]
		
		lastCollectedEpisode = trakt.collectionProgress(id)['last_episode']
		collected = (lastCollectedEpisode['season'] == int(season) and lastCollectedEpisode['number'] == int(number))
		
		if (collected == False):
			searchStr = '{title} S{season}E{episode}'.format(title=item['show']['title'], season=season, episode=number)
			torrents = ThePirateBay.search(searchStr, '720p')
			if (len(torrents) > 0 and transmission.addTorrent(torrents[0]['magnet'])):
				info = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				info = info + '    Added: ' + torrents[0]['title']
				
				if (trakt.addToCollection(item['show']['ids']['trakt'], item['episode']['season'], item['episode']['number'])):
					info = info + ' - Collected at Trakt.TV'
				
				print info
				
except Exception as e:
	print e