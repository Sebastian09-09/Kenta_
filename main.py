from flask import Flask ,  render_template , request , redirect , url_for , flash , session
import dataFetcher
import mangaDownloaderThreads
import mangaDownloaderLoops
app = Flask(__name__)
import os;import shutil
from threading import Thread

import random
import string
import json 

#SETTINGS
app.config.update(
	SECRET_KEY='SECRET_KEY',
	SESSION_COOKIE_SECURE=True,
	REMEMBER_COOKIE_SECURE=True,
	SESSION_COOKIE_HTTPONLY=True,
	REMEMBER_COOKIE_HTTPONLY=True
)

#REMOVE TEMP FILES
def removeTempFiles():
  temp = os.listdir('static/temp')
  for i in temp:
    if i != 'note':
      os.remove(f'static/temp/{i}')
  downloads_ = os.listdir('static/downloads')
  for i in downloads_:
    if i != 'note':
      shutil.rmtree(f'static/downloads/{i}')

#USER
def getUser():
	with open('method.json' , 'r') as f:
		data = json.load(f)
	return data['method']

#SESSIONS
def addSession():
	if session == {}:
		dbs = os.listdir('static/downloads')	
		db = str(random.randint(0,1000000001))+str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)))
		while db in dbs:
			dbs = os.listdir('static/downloads')
			db = str(random.randint(0,1000000001))+str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)))
		os.mkdir(f'static/downloads/{db}')
		session['databaseID'] = db
		print(db)
	else:
		dbid = session['databaseID']
		dbs = os.listdir('static/downloads')
		if str(dbid) not in dbs:
			os.mkdir(f'static/downloads/{dbid}')

#HOME
@app.route("/")
def home():
	return render_template('index.html')


#SERVICE
@app.route("/services/")
def services():
	return render_template('services.html')


#MANGA
@app.route("/manga/" , defaults={'url' : ' '} , methods=["GET","POST"])
@app.route("/manga/<url>/" , methods=["GET","POST"])
def manga(url):
	addSession()
	if request.method == "GET":
		return render_template('manga.html' , placeholder="url" , desc='Fetch')
	else:
		url = request.form['url']
		if r"!@$%%$@!" in url:
			temp=url.split(r'!@$%%$@!')
			url=temp[0]
			sauce=temp[1]
		if url == '' or not url.startswith('http'):
			flash(f'Please provide a URL' , 'warning')
			return redirect(url_for('manga'))
		
		website = 'kissmanga' if 'kissmanga.org' in url else 'mangakakalot' if 'mangakakalot.com' in  url else 'manganato' if 'manganato.com' in url else 'nhentai' if 'nhentai.com' in url else 'readm.org' if 'readm.org' in url else None # else 'mangaowl' if 'mangaowl.com' in url 

		if website == None:
			flash(f'This Website is not supported!' , 'error')
			return redirect(url_for('manga'))
		
		if 'sauce' in request.form:
			sauce = request.form['sauce']
			if website == 'nhentai' and sauce == '':
				flash(f'Please input the sauce too!' , 'warning')
				return redirect(url_for('manga'))
			info = dataFetcher.Fetcher.getInfo(website, url, sauce)
			absurl=str(url)+r"!@$%%$@!"+str(sauce)
		else:
			if website == 'nhentai' and sauce == '':
				flash(f'Please input the sauce too!' , 'warning')
				return redirect(url_for('manga'))
			info = dataFetcher.Fetcher.getInfo(website, url, sauce)
			absurl=str(url)+r"!@$%%$@!"+str(sauce)
		
		name = info[0]
		if name == '<!Failed!>':
			flash(f'Failed to Fetch data' , 'error')
			return redirect(url_for('manga'))
		
		if website != 'nhentai':
			desc = info[1]
			chapters = info[2]
			cover = info[3]
			firstChap = list(chapters.keys())[-1]
		else:
			cover = info[1]
		

		if 'chapter' in request.form:
			chapter = request.form['chapter'].split('@@@')
			chapterName = chapter[0]
			chapterUrl = chapter[1].replace('"' , ' ').strip()
			if getUser() == 'loops':
				thr = Thread(target=mangaDownloaderThreads.Downloader.getPages , args=[chapterName , website , chapterUrl ,  sauce , name , session['databaseID']])
				thr.start()
			else:
				thr = Thread(target=mangaDownloaderLoops.Downloader.getPages , args=[chapterName , website , chapterUrl ,  sauce , name , session['databaseID']])
				thr.start()

			#mangaDownloaderThreads.Downloader.getPages(chapterName, website, chapterUrl, sauce )
		
		if website == 'nhentai' and 'sauce' not in request.form:
			if getUser() == 'loops':
				thr = Thread(target=mangaDownloaderThreads.Downloader.getPages , args=[name , website , url ,  sauce , name , session['databaseID']])
				thr.start()
			else:
				thr = Thread(target=mangaDownloaderLoops.Downloader.getPages , args=[name , website , url ,  sauce , name , session['databaseID']])
				thr.start()
			#mangaDownloaderThreads.Downloader.getPages(name, website, url, sauce )

		if website != 'nhentai':
			return render_template('manga.html'  , placeholder=absurl , desc='Start' , website=website , name=name , description=desc , chapters=chapters , cover=cover , firstChap = firstChap  )
		else:
			return render_template('manga.html'  , placeholder=absurl , desc='Start' , website=website , name=name , cover=cover)			

#SUPPORTED WEBSITES
@app.route("/supportedwebsites/")
def supportedwebsites():
	return render_template('supported websites.html')


#CONTACT
@app.route("/contact/")
def contact():
	return render_template('contact.html')

#DOWNLOADS
@app.route("/downloads/")
def downloads():
	addSession()
	return 'your downloads will be here'

#DATABASE DETAILS
@app.route("/database/")
def database():
	text = ''
	dbs = os.listdir('static/downloads')
	for db in dbs:
		if db != 'note':
			text += '----->'+db+'<br>'
			manga = os.listdir(f'static/downloads/{db}')
			for j in manga:
				text += '---------->'+j+'<br>'
	return text


if __name__=='__main__':
  removeTempFiles()
  app.run(host='0.0.0.0', port=8080)