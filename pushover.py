#!/usr/bin/python
class Pushover:
	@staticmethod
	def send(user_key, app_token, message, title = ''):
		import httplib, urllib
		conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request("POST", "/1/messages.json",
		  urllib.urlencode({
			"token": app_token,
			"user": user_key,
			"message": message,
			"title": title
		  }), { "Content-type": "application/x-www-form-urlencoded" })
		conn.getresponse()