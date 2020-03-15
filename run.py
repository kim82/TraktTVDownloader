#!/usr/bin/python
import config
from trakttv import TraktTV
import torrentsearch
from pushover import Pushover
from transmission import Transmission
from datetime import datetime

try:
	trakt = TraktTV(config.CLIENT_ID, config.CLIENT_SECRET)
	trakt.login()
	calendar = trakt.calendar(1)

	transmission = Transmission(config.TRANSMISSION, config.TRANSMISSION_USER, config.TRANSMISSION_PWD)
	for item in calendar:
		id = item['show']['ids']['trakt']
		season = ('0' + str(item['episode']['season']))[-2:]
		number = ('0' + str(item['episode']['number']))[-2:]
		
		lastCollectedEpisode = trakt.collectionProgress(id)['last_episode']
		collected = (lastCollectedEpisode['season'] == int(season) and lastCollectedEpisode['number'] == int(number))
		
		if (collected == False):
			searchStr = '{title} S{season}E{episode}'.format(title=item['show']['title'], season=season, episode=number)
			torrents = torrentsearch.search(searchStr + ' 720p')
			if (len(torrents) > 0 and transmission.addTorrent(torrents[0]['magnet'])):
				info = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				info = info + '    Added: ' + torrents[0]['title']
				
				if (trakt.addToCollection(item['show']['ids']['trakt'], item['episode']['season'], item['episode']['number'])):
					info = info + ' - Collected at Trakt.TV'
				
				print info
			else:
				Pushover.send(config.PUSHOVER_USER, config.PUSHOVER_APP, 'No torrents found for ' + searchStr, 'Trakt TV Downloader')
				print 'No torrents found for ' + searchStr
				
except Exception as e:
	print e
