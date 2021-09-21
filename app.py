from flask import Flask ,  render_template
import jyserver.Flask as js
app = Flask(__name__)

@js.use(app)
class App:
    def __init__(self):
        self.complete = False
        self.currentWebsite = 0
        self.websites = {
            0: ['bookwalker.png', '274' ,'BOOK☆WALKER is KADOKAWA &#039;s official eBook store &amp; app for Manga/Light Novel fans. Check out for free and exclusive eBooks, as well as special deals offered only on BOOK☆WALKER!' ,'Book Walker'],
            1: ['kissmanga.org.png' , '350' , 'Read manga online in high quality for free, fast update, daily update Unique reading type All pages just need to scroll to read next page, and many more.' , 'Kiss Manga'],
            2: ['logo_comicwalker.svg' , '300' , 'ComicWalker titles, updated every day, read over 3000 popular titles by KADOKAWA for free! English and Chinese (Traditional and Simplified) versions available also!' , 'Comic Walker'],
            3: ['mangakakalot.png' , '215' , 'Read manga online free at Mangakakalot.com, update fastest, most full, synthesized 24h free with high-quality imagesa and be the first one to publish new chapters.' , 'MangaKakalot'],
            4: ['manganelo.png' , '215' ,'Read manga online free at MangaNato, update fastest, most full, synthesized 24h free with high-quality images. We hope to bring you happy moments. Join and discuss','MangaNato'],
            5: ['mangaowl.png' , '70' , 'Read english manga online free with a huge collections at Manga Owl, update fastest, most full, synthesized, translate free with high-quality images. The best place to read the updated latest, greatest, best-quality english manga for FREE with our best service. Enjoy!','MangaOwl'],
            6: ['nhentai.svg' , '200' ,'nHentai is a free and frequently updated hentai manga and doujinshi reader packed with thousands of multilingual comics for reading and downloading.','nhentai'],
            7: ['readm.org.png' , '210' , 'Biggest manga library on the web. Absolutely free and daily updated English translated manga online for free!','Readm.org'],
        }
    def increment(self):
        if self.currentWebsite < 7:
            self.currentWebsite += 1
            self.js.document.getElementById('currentWebsite').innerHTML = str(self.currentWebsite + 1)+'/8'
            self.js.document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[self.currentWebsite][0]
            self.js.document.getElementById('logo').width = self.websites[self.currentWebsite][1]
            self.js.document.getElementById('about').innerHTML = self.websites[self.currentWebsite][2]
            self.js.document.getElementById('title').innerHTML = self.websites[self.currentWebsite][3]
    def decrement(self):
        if self.currentWebsite >= 1:
            self.currentWebsite -= 1
            self.js.document.getElementById('currentWebsite').innerHTML = str(self.currentWebsite + 1)+'/8'
            self.js.document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[self.currentWebsite][0]
            self.js.document.getElementById('logo').width = self.websites[self.currentWebsite][1]
            self.js.document.getElementById('about').innerHTML = self.websites[self.currentWebsite][2]
            self.js.document.getElementById('title').innerHTML = self.websites[self.currentWebsite][3]

#SETTINGS
app.config.update(
    SECRET_KEY='thisissoethingsupposedtobesecret',
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
@app.route("/manga/")
def manga():
    return render_template('manga.html')


#SUPPORTED WEBSITES
@app.route("/supportedwebsites/")
def supportedwebsites():
    return App.render(render_template('supported websites.html'))


#CONTACT
@app.route("/contact/")
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run()