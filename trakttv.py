import sys
import json
import time
from datetime import datetime, date
from urllib import urlencode
from urllib2 import Request, urlopen, HTTPError

		
class TraktTV:
	APIURL = 'https://api.trakt.tv'
	clientId = ''
	clientSectret = ''
	token = ''
	authFile = ''
	
	# init method or constructor   
	def __init__(self, clientId, clientSecret):
		self.clientId = clientId
		self.clientSecret = clientSecret
		self.authFile = sys.path[0] + '/trakt.auth'
		
		#tries to read trakt.auth file - creates an empty if not
		try:
			open(self.authFile, 'r')
		except IOError:
			file = open(self.authFile, "w")
			file.write('{"access_token":""}');
			file.close();
	def _header(self):
		return {
				'trakt-api-version': '2',
				'trakt-api-key': self.clientId,
				'Authorization': 'Bearer ' + self.token,
				'Content-Type': 'application/json'
			   }
	def _post(self, url, data, header = {'Content-Type':'application/json'}):
		try:
			request = Request(self.APIURL + url, json.dumps(data), header)
			return urlopen(request).read()
		except HTTPError as e:
			print e
			return ""
	
	def _get(self, url):
		from urllib2 import Request, urlopen, HTTPError
		
		try:
			request = Request(self.APIURL + url, None, self._header())
			return urlopen(request).read()
		except HTTPError as e:
			return ""
	
	#Login to Trakt.TV - Gets the access token
	def login(self):
		#Clears token
		self.token = ''
		
		#reads token from trakt.auth file
		file = open(self.authFile, "r")
		tokenJson = json.loads(file.read())
		file.close()
		
		#is token is found locally - renew it if it expires within 10 days
		if (tokenJson['access_token'] != ''):
			expiration = datetime.utcfromtimestamp(tokenJson['created_at'] + tokenJson['expires_in']).date()
			
			refreshToken = (abs((expiration - date.today()).days) <= 10)	#if expiration is within 10 days, renew the token
			if refreshToken:
				#Token exists in storage, refresh the token
				data = { 'refresh_token': tokenJson['refresh_token'], 
						 'grant_type': 'refresh_token', 
						 'client_id': self.clientId, 
						 'client_secret': self.clientSecret, 
						 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob'
					   }
				tokenReponse = self._post('/oauth/token', data)

				if(tokenReponse != ''):
					file = open(self.authFile, "w")
					file.write(tokenReponse)
					file.close()
			self.token = tokenJson['access_token']
			return
		else:	
			#else get a new token
			data = { 'client_id': self.clientId }
			codeResponse = self._post('/oauth/device/code', data)
			code = json.loads(codeResponse)
			
			#Writes info for login
			print 'Go to ' + code['verification_url'] + ' to authorize the app'
			print 'And enter the code: ' + code['user_code']
			
			expiration = int(code['expires_in'])
			while self.token == '':
				time.sleep(int(code['interval']))
				expiration = expiration - int(code['interval'])
				
				if (expiration <= 0):
					print 'Activation timed out - please try again'
					return
				
				data = { 'code': code['device_code'], 
						 'client_id': self.clientId, 
						 'client_secret': self.clientSecret }
				tokenReponse = self._post('/oauth/device/token', data)
				if(tokenReponse != ''):
					print 'Succesfully activated'
					
					tokenJson = json.loads(tokenReponse)
					file = open(self.authFile, "w")
					file.write(tokenReponse)
					file.close()
					
					self.token = tokenJson['access_token']
					return

	#Gets the shows for today
	#{days}:	Number of days to fetch data from
	def calendar(self, days):
		today = date.today()
		todayStr = today.strftime("%Y-%m-%d")
		
		response = self._get('/calendars/my/shows/{date}/{days}'.format(date=todayStr, days=days))

		return json.loads(response)
		
	def collectionProgress(self, id):
		response = self._get('/shows/{id}/progress/collection'.format(id=id))
		return json.loads(response)
		
	def addToCollection(self, traktId, season, episode):
		data = {
		  "shows": [
			{
			  "ids": {
				"trakt": traktId
			  },
			  "seasons": [
				{
				  "number": season,
				  "episodes": [
					{
					  "number": episode
					}
				  ]
				}
			  ]
			}
		  ]
		}
		return self._post('/sync/collection', data, self._header()) != ''
