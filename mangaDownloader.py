import requests 
import threading
import time
from bs4 import BeautifulSoup
import dataFetcher
import urllib.parse

class Downloader:
	@staticmethod
	def getPages(name , website , url  , sauce , allTheChapters , from_ , to_ ):
		referer = 'https://kissmanga.org' if website == 'kissmanga' else 'https://mangakakalot.com' if website == 'mangakakalot' else 'https://manganato.com' if website == 'manganato' else 'https://cdn.nhentai.com' if website == 'nhentai' else 'https://readm.org' if website == 'readm.org' else None
		header={
				'User-Agent': 'Mozilla/5.0',
				'Referer' : f'https://{referer}'
				}
		htmlText = requests.get(url , stream=True , headers=header)
		response = htmlText.status_code
		htmlText = htmlText.text
		if response == 200 and website != None:
			soup = BeautifulSoup(htmlText , 'lxml')
			#for kissmanga
			if website == 'kissmanga':
				rawChapters = soup.find( class_='listing listing8515 full' )
				chapters = {}
				for i in rawChapters:
					try:
						key = Downloader.clear(i.a.text.strip())
						chapters[key] = ('https://kissmanga.org'+i.a.attrs['href'] , i.a.text.strip() )
					except:
						pass
				chapters = dict(reversed(list(chapters.items())))
				print(chapters)
				if allTheChapters:
					pass
				else:
					pass

			if website == 'mangakakalot':
				pass
			if website == 'manganato':
				pass
			if website == 'nhentai':
				pass
			if website == 'readm.org':
				pass

				

		

	def toPdf(imagesDict):
		pass
		
	@staticmethod
	def clear(string):
		newString = ''
		for i in string:
			if i != ' ':
				newString += i
		newString = newString.lower().replace('\n', '')
		return newString


x=Downloader.getPages( 'yesm' , 'kissmanga' ,  'https://kissmanga.org/manga/manga-ho985297/' , '' , True , None , None) 
print(x)