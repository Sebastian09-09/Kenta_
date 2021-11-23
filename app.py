from flask import Flask ,  render_template , request , redirect , url_for , flash , session
import dataFetcher
import mangaDownloader
app = Flask(__name__)
import os 
from threading import Thread
import random


#SETTINGS
app.config.update(
	SECRET_KEY=os.environ['SECRET_KEY'],
	SESSION_COOKIE_SECURE=True,
	REMEMBER_COOKIE_SECURE=True,
	SESSION_COOKIE_HTTPONLY=True,
	REMEMBER_COOKIE_HTTPONLY=True
)

#SESSIONS
def addSession():
	if session == {}:
		dbs = os.listdir('static\downloads')	
		db = random.randint(0,1000000001)
		while db in dbs:
			dbs = os.listdir('static\downloads')
			db = random.randint(0,1000000001)
		os.mkdir(f'static\downloads\{db}')
		session['databaseID'] = db
	else:
		dbid = session['databaseID']
		dbs = os.listdir('static\downloads')
		if str(dbid) not in dbs:
			os.mkdir(f'static\downloads\{dbid}')

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
		if url == '':
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
			thr = Thread(target=mangaDownloader.Downloader.getPages , args=[chapterName , website , chapterUrl ,  sauce , name , session['databaseID']])
			thr.start()
			#mangaDownloader.Downloader.getPages(chapterName, website, chapterUrl, sauce )
		
		if website == 'nhentai' and 'sauce' not in request.form:
			thr = Thread(target=mangaDownloader.Downloader.getPages , args=[name , website , url ,  sauce , name , session['databaseID']])
			thr.start()
			#mangaDownloader.Downloader.getPages(name, website, url, sauce )

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


if __name__=='__main__':
	app.run()
