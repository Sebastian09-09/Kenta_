from flask import Flask ,  render_template , request , redirect , url_for , flash
import requests
import dataFetcher
import mangaDownloader
app = Flask(__name__)

#SETTINGS
app.config.update(
	SECRET_KEY='HIDETHISSHIT',
	SESSION_COOKIE_SECURE=True,
	REMEMBER_COOKIE_SECURE=True,
	SESSION_COOKIE_HTTPONLY=True,
	REMEMBER_COOKIE_HTTPONLY=True
)
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
			info = dataFetcher.Fetcher.getInfo(website, url, request.form['sauce'])
			absurl=str(url)+r"!@$%%$@!"+str(request.form['sauce'])
			if website == 'nhentai' and request.form['sauce'] == '':
				flash(f'Please input the sauce too!' , 'warning')
				return redirect(url_for('manga'))
		else:
			info = dataFetcher.Fetcher.getInfo(website, url, sauce)
			absurl=str(url)+r"!@$%%$@!"+str(sauce)
			if website == 'nhentai' and sauce == '':
				flash(f'Please input the sauce too!' , 'warning')
				return redirect(url_for('manga'))
		
		name = info[0]
		if name == '<!Failed!>':
			flash(f'Failed to Fetch data' , 'error')
			return redirect(url_for('manga'))
		
		if website != 'nhentai':
			desc = info[1]
			chapters = info[2]
			cover = info[3]
		else:
			cover = info[1]
			
		if 'allTheChapters' in request.form:
			allTheChapters=request.form['allTheChapters']
			#mangaDownloader.Downloader.getPages( website , url , request.form['sauce'])
		else:
			if 'from' in request.form:
				from_=request.form['from']
				if from_ == '': from_=None
			if 'to' in request.form:
				to_=request.form['to']
				if to_ == '': to_=None

		if website != 'nhentai':
			return render_template('manga.html'  , placeholder=absurl , desc='Start' , website=website , name=name , description=desc , chapters=chapters , cover=cover)
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


if __name__=='__main__':
	app.run()