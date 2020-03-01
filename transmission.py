class Transmission:
	rpcAddress = ''
	username = ''
	password = ''
	sessionId = ''
	
	# init method or constructor   
	def __init__(self, rpcAddress, username = '', password = ''):
		self.rpcAddress = rpcAddress
		if not self.rpcAddress.endswith("/transmission/rpc"):
			self.rpcAddress = '%s/transmission/rpc' % rpcAddress 
				
		self.username = username
		self.password = password
		
		if (self.sessionId == ''):
			self._setSessionId();
	
	def _rpc(self, data):
		from urllib2 import Request, urlopen, HTTPError
		import base64
		import json
				
		base64string = base64.b64encode('%s:%s' % (self.username, self.password))		
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers =	{
						'User-Agent':user_agent,
						'Authorization': 'Basic ' + base64string,
						'X-Transmission-Session-Id': self.sessionId
					} 
		request = Request(self.rpcAddress, json.dumps(data), headers)
				
		try:
			return urlopen(request).read()
		except HTTPError as e:
			if (e.code == 409):
				return e.hdrs['X-Transmission-Session-Id']
			else:
				print e
			return ''
			
	def _setSessionId(self):
		data = {"method":"", "arguments":{}}
		self.sessionId = self._rpc(data);

	def addTorrent(self, magnetLink):
		import json
			
		data = { "method": "torrent-add", "arguments": { "paused": "false", "filename": magnetLink } }
		result = json.loads(self._rpc(data))
		return result['result'] == 'success'
