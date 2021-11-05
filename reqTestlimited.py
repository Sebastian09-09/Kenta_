import threading
import time
import requests
import urllib.parse

chapters={
	'random1': [ 'https://kissmanga.org/chapter/manga-ho985297/chapter-1' , 'random 1' ] , 
	'random2': [ 'https://kissmanga.org/chapter/manga-ho985297/chapter-2' , 'random 2' ] , 
}

d = {}
data = {}
pages = {}

def get(url):
	global data
	global pages 
	print(url)
	header = {
				'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
				'Accept-Encoding': 'gzip, deflate, br',
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
							'Version/13.1.2 Safari/605.1.15',
				'Accept-Language': 'en-ca', 'Referer': f'https://kissmanga.org',
				'Connection': 'keep-alive'
			}

	r = requests.get(url[0] , headers=header)
	print(r, 'for ' , url[1])
	if r == 200:
		pass


def run():
	global d
	for i in range(1,len(chapters)+1):
			#time.sleep(0.2)
			print(f'Starting Thread {i}')
			d['x'+str(i)] = threading.Thread(target=get , args=(list(chapters.values())[i-1],)) 
			d['x'+str(i)].start()
				
run()
for i in range(1,len(chapters)+1):
	d['x'+str(i)].join()
	print(f'Ending Thread {i}')