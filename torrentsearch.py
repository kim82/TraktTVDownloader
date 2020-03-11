#!/usr/bin/python
class Util:
	@staticmethod
	def extract(content, regexSearchResult, regexLinks, totalGroupCount, titleGroupNo, linkGroupNo):
		import re
		items = []
		searchResult = re.search(regexSearchResult, content)
		if searchResult:
			links = re.finditer(regexLinks, searchResult.group())
			for matchNum, match in enumerate(links, start=1):
				if len(match.groups()) >= totalGroupCount:
					items.append({'title': match.group(titleGroupNo), 'magnet': match.group(linkGroupNo) })

		return items

	@staticmethod
	def getHTMLContent(url):
		from urllib2 import Request, urlopen, HTTPError, URLError
		import socket
		
		user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
		headers = {'User-Agent':user_agent} 
		request = Request(url, None, headers)
		try:
			return urlopen(request, timeout=4).read()
		except:
			return ""
			
class ThePirateBay:
	@staticmethod
	def search(search):
		from urllib import quote
				
		content = Util.getHTMLContent("https://tpb.party/search/" + quote(search) + "/0/99/0")
		
		regexSearchResult = "<table id=\"searchResult\">(.|\n)*?<\/table>"
		regexLinks = r"(class=\"detLink\"(.|\n)*?>)((.|\n)*?)(</a>)((.|\n)*?)(href=\"((.|\n)*?)\")"
		
		return Util.extract(content, regexSearchResult, regexLinks, 10, 3, 9)

class MagnetDL:
	@staticmethod
	def search(search):
		from urllib import quote_plus
		import re
		
		hiddenFields = ""
		mainPage = Util.getHTMLContent("https://www.magnetdl.com")
		regex = r'<input type="hidden" name="(.*)" value="(.*)" \/>'
		matches = re.finditer(regex, mainPage, re.MULTILINE)
		for matchNum, match in enumerate(matches, start=1):    
			hiddenFields = hiddenFields + "&" + match.group(1) + "=" + match.group(2)
			
		search = search.replace(" ", "-");
		content = Util.getHTMLContent("https://www.magnetdl.com/search/?q=" + quote_plus(search) + hiddenFields)
		
		regexSearchResult = "<table class=\"download\">(.|\n)*?<\/table>"
		regexLinks =  r"(\"(magnet:.*?)\")((.|\n)*?) (title=\"((.|\n)*?)\") title=\"((.|\n)*?)\""
		
		return Util.extract(content, regexSearchResult, regexLinks, 9, 8, 2)

def search(search):
	torrents = ThePirateBay.search(search)
	if len(torrents) == 0:
		torrents = MagnetDL.search(search)
	return torrents