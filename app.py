from flask import Flask ,  render_template

app = Flask(__name__)
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


#ABOUT
@app.route("/about")
def about():
    return render_template('about.html')


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
    return render_template('supported websites.html')


#CONTACT
@app.route("/contact")
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run()