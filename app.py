from flask import Flask ,  render_template
import jyserver.Flask as jsf
app = Flask(__name__)

@jsf.use(app)
class App:
    def __init__(self):
        self.count = 0
        self.websites = {
            0: ['bookwalker.png', '274' ,'nice site'],
            1: ['kissmanga.org.png' , '350' , 'very nice'],
            2: ['logo_comicwalker.svg' , '300' , 'top notch'],
            3: ['mangakakalot.png' , '215' , 'fast'],
            4: ['manganelo.png' , '215' ,'haha nice'],
            5: ['mangaowl.png' , '80' , 'umm'],
            6: ['nhentai.svg' , '200' ,'copy ??'],
            7: ['readm.org.png' , '210' , 'fast asf'],
        }
    def increment(self):
        if self.count < 7:
            self.count += 1
            self.js.document.getElementById('count').innerHTML = str(self.count + 1)+'/8'
            self.js.document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[self.count][0]
            self.js.document.getElementById('logo').width = self.websites[self.count][1]
            self.js.document.getElementById('about').innerHTML = self.websites[self.count][2]
    def decrement(self):
        if self.count >= 1:
            self.count -= 1
            self.js.document.getElementById('count').innerHTML = str(self.count + 1)+'/8'
            self.js.document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[self.count][0]
            self.js.document.getElementById('logo').width = self.websites[self.count][1]
            self.js.document.getElementById('about').innerHTML = self.websites[self.count][2]
        

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
@app.route("/services")
def services():
    return render_template('services.html')


#MANGA
@app.route("/manga")
def manga():
    return render_template('manga.html')


#SUPPORTED WEBSITES
@app.route("/supportedwebsites")
def supportedwebsites():
    return App.render(render_template('supported websites.html'))


#CONTACT
@app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run()