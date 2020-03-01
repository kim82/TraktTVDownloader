#!/usr/bin/python
def _getHTMLContent(url):
		from urllib2 import Request, urlopen, HTTPError
		
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers = {'User-Agent':user_agent} 
		request = Request(url, None, headers)
		try:
			return urlopen(request).read()
		except HTTPError as e:
			print e
			return ""
			
class ThePirateBay:
	@staticmethod
	def search(search, quality):
		import sys, getopt
		import re
		from urllib import quote_plus
		
		search = search + ' ' + quality
		content = _getHTMLContent("https://thepiratebay.org/search/" + quote_plus(search) + "/0/99/0")
		
		regexSearchResult = "<table id=\"searchResult\">(.|\n)*?<\/table>"
		regexLinks = r"(class=\"detLink\"(.|\n)*?>)((.|\n)*?)(</a>)((.|\n)*?)(href=\"((.|\n)*?)\")"
		
		searchResult = re.search(regexSearchResult, content)
		if searchResult:
			links = re.finditer(regexLinks, searchResult.group())

			items = []
			for matchNum, match in enumerate(links, start=1):
				if len(match.groups()) >= 10:
					items.append({'title': match.group(3), 'magnet': match.group(9) })
			return items
