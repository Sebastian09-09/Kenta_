import threading
import time
import requests
import urllib.parse

d={}
pages = {}
keepRunning = True
killFrom = 0
pass_ = True
baseUrl = 'https://cdn.nhentai.com/nhe/storage/images/377242/'

def get(page):
	global pass_
	global keepRunning
	global pages
	global killFrom
	url = baseUrl+f'{page}.jpg' 
	print(url)
	header = {
				'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
				'Accept-Encoding': 'gzip, deflate, br',
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
							'Version/13.1.2 Safari/605.1.15',
				'Accept-Language': 'en-ca', 'Referer': f'https://cdn.nhentai.com',
				'Connection': 'keep-alive'
			}

	r = requests.get(url , headers=header)
	print('----------> Page ',  page , '- ', r)
	if r.status_code == 200:
		pages[page] = r
		print('----------------------->', r, ' for ' , url , ' page ' , page)
	else:
		url = baseUrl+f'{page}.png' 
		r = requests.get(url , headers=header)
		if r.status_code == 200:
			pages[page] = r
			print('----------------------->', r, ' for ' , url , ' page ' , page)
		else:
			keepRunning = False
			if pass_:
				killFrom = page
				pass_ = False

def run():
	global keepRunning
	global pages
	global d
	page = 1
	while keepRunning:
		time.sleep(0.2)
		print(f'Starting Thread {page}')
		d['x'+str(page)] = threading.Thread(target=get , args=(page,)) 
		d['x'+str(page)].start()
		page += 1
		
run()

for i in range(1,killFrom):
	d['x'+str(i)].join()
	print(f'Ending Thread {i}')

for i in range(1,killFrom):
	if i not in pages:
		print('Failed to Fetch page ',i)
		print('retrying...')
		url = baseUrl+f'{i}.jpg' 
		header = {
				'Accept': 'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
				'Accept-Encoding': 'gzip, deflate, br',
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
							'Version/13.1.2 Safari/605.1.15',
				'Accept-Language': 'en-ca', 'Referer': f'https://readm.org',
				'Connection': 'keep-alive'
			}
		r = requests.get(url , headers=header)
		print('----------> Page ',  i , '- ', r)
		if r.status_code == 200:
			pages[i] = r
			print('----------------------->', r, ' for ' , url , ' page ' , i)
		else:
			url = baseUrl+f'{i}.png'
			r = requests.get(url , headers=header)
			if r.status_code == 200:
				pages[i] = r
				print('----------------------->', r, ' for ' , url , ' page ' , i)
			else:
				print('Failed!')
		
print(pages)