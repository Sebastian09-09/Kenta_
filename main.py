from flask import Flask, render_template, request, redirect, url_for, flash, session , send_from_directory
import dataFetcher
import mangaDownloaderLoops
import mangaDownloaderThreads
import time

app = Flask(__name__)
import os
import shutil
from threading import Thread

import random
import string
import json

#SETTINGS
app.config.update(SECRET_KEY='sus',
                  SESSION_COOKIE_SECURE=True,
                  REMEMBER_COOKIE_SECURE=True,
                  SESSION_COOKIE_HTTPONLY=True,
                  REMEMBER_COOKIE_HTTPONLY=True)

#ARC SERVER
@app.route("/arc-sw.js")
def arc():
	return send_from_directory(directory='',path='arc-sw.js',mimetype='application/javascript')

#REMOVE NUMBER OF TRIES
def removeFailCount():
    if 'failCount' in session:
        del session['failCount']
    


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


#METHOD
def getMethod():
    with open('method.json', 'r') as f:
        data = json.load(f)
    return data['method']


#SESSIONS
def addSession():
    if session == {}:
        dbs = os.listdir('static/downloads')
        db = str(random.randint(0, 1000000001)) + str(''.join(
            random.choices(string.ascii_uppercase + string.digits, k=5)))
        while db in dbs:
            dbs = os.listdir('static/downloads')
            db = str(random.randint(0, 1000000001)) + str(''.join(
                random.choices(string.ascii_uppercase + string.digits, k=5)))
        os.mkdir(f'static/downloads/{db}')
        with open(f'static/downloads/{db}/downloads.txt' , 'w' , encoding='utf-8'):
            pass
        with open(f'static/downloads/{db}/loading.json' , 'w' , encoding='utf-8') as f:
            f.write('{}')
        session['databaseID'] = db
    else:
        dbid = session['databaseID']
        dbs = os.listdir('static/downloads')
        if str(dbid) not in dbs:
            os.mkdir(f'static/downloads/{dbid}')
            with open(f'static/downloads/{dbid}/downloads.txt' , 'w' , encoding='utf-8'):
                pass
            with open(f'static/downloads/{dbid}/loading.json' , 'w' , encoding='utf-8') as f:
                f.write('{}')


#HOME
@app.route("/")
def home():
    removeFailCount()
    return render_template('index.html')



#DOWNLOAD Multiple Chapters
def downloadChap(chapters , website , sauce , name , dbid ):
    for chapter in chapters:
        chapterName = chapter
        chapterUrl = chapters[chapter]
        if website == 'kissmanga':
            fileName = str(website) + '-' + str(chapterName)
        else:
            fileName = str(website) + '-' + str(name) + '-' + str(chapterName)
        fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
        fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()
        print(f'---------------------> {fileName}')
        f = open(f'static/downloads/{dbid}/downloads.txt' , 'r'  , encoding='utf-8' )
        loading = mangaDownloaderThreads.Downloader.getLoading(session['databaseID'])
        if fileName in f.read() or fileName in loading:
            time.sleep(0.1)
        else:
            mangaDownloaderThreads.Downloader.getPages(chapterName, website, chapterUrl, sauce, name, dbid)
            
                

#MANGA
@app.route("/manga/", defaults={'url': ' '}, methods=["GET", "POST"])
@app.route("/manga/<url>/", methods=["GET", "POST"])
def manga(url):
    addSession()
    if request.method == "GET":
        return render_template('manga.html', placeholder="url", desc='Fetch')
    else:
        #print(request.form)
        sauce = None #nhentai is no more supported 
        url = request.form['url']
        if r"!@$%%$@!" in url:
            temp = url.split(r'!@$%%$@!')
            url = temp[0]
            '''
            sauce = temp[1]
            '''
        if url == '' or not url.startswith('http'):
            flash(f'Please provide a URL', 'warning')
            return redirect(url_for('manga'))

        website = 'kissmanga' if 'kissmanga.org' in url else 'mangakakalot' if 'mangakakalot.com' in url else 'manganato' if 'manganato.com' in url else 'readm.org' if 'readm.org' in url else None  # else 'mangaowl' if 'mangaowl.com' in url else 'nhentai' if 'nhentai.com' in url 

        if website == None:
            flash(f'This Website is not supported!', 'error')
            return redirect(url_for('manga'))

        absurl = str(url) + r"!@$%%$@!" + str(sauce)
        info = dataFetcher.Fetcher.getInfo(website, url, sauce)
        name = info[0]
        if name == '<!Failed!>':
            if 'failCount' not in session:
                temp=os.system('pip install -r requirements.txt');session['failCount'] = 1
                info = dataFetcher.Fetcher.getInfo(website, url, sauce)
                name = info[0]
                if name == '<!Failed!>':
                    flash(f'Failed to Fetch data', 'error')
                    return redirect(url_for('manga'))
            else:
                flash(f'Failed to Fetch data', 'error')
                return redirect(url_for('manga'))

        #if website != 'nhentai':
        desc = info[1]
        chapters = info[2]
        cover = info[3]
        try:
          firstChap = list(chapters.keys())[-1]
        except:
          firstChap = 'None'
        #else:
            #cover = info[1]

        """ DOWNLOAD ALL CHAPTERS """
        if 'downloadAllChapters' in request.form:
            flash(f'Downloading all the chapters' , 'success')
            loading=mangaDownloaderThreads.Downloader.getLoading(session['databaseID'])
            for i in chapters:
                if website == 'kissmanga':
                    fileName = str(website) + '-' + str(i)
                else:
                    fileName = str(website) + '-' + str(name) + '-' + str(i)
                fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
                fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()
                loading[fileName] = "True"
            mangaDownloaderThreads.Downloader.setLoading(session['databaseID'] , loading )
            thr = Thread(target=downloadChap, args=[chapters , website , sauce , name , session['databaseID'] ])
            thr.start()
            
            
            return render_template('manga.html',
                                   placeholder=absurl,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap)

        """ DOWNLOAD A RANGE OF CHAPTERS """
        if 'multipleChaptersStart' in request.form and request.form['multipleChaptersStart'] != request.form['multipleChaptersEnd']:
            newChapters = {}
            add = False

            chapkeys = list(chapters.keys())
            chapkeys = list(map(mangaDownloaderThreads.Downloader.clearName , chapkeys))
            chapkeys = list(map(mangaDownloaderThreads.Downloader.hardClearName , chapkeys))
            
            start_ = mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersStart'].split('@@@')[0])
            start_ = mangaDownloaderThreads.Downloader.hardClearName(start_)
            end_ = mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersEnd'].split('@@@')[0])
            end_ = mangaDownloaderThreads.Downloader.hardClearName(end_)
            startIndex = chapkeys.index(start_)
            endIndex = chapkeys.index(end_)

            loading=mangaDownloaderThreads.Downloader.getLoading(session['databaseID'])
            
            
            if startIndex < endIndex:  
                for i in chapters:
                    if mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(i)) == mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersStart'].split('@@@')[0])):
                        add = True
                    if add:
                        newChapters[i] = chapters[i]

                        if website == 'kissmanga':
                            fileName = str(website) + '-' + str(i)
                        else:
                            fileName = str(website) + '-' + str(name) + '-' + str(i)
                        fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
                        fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()
                        loading[fileName] = "True"
                        
                    if mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(i)) == mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersEnd'].split('@@@')[0])):
                        add = False

            else:
                for i in chapters:
                    if mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(i)) == mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersEnd'].split('@@@')[0])):
                        add = True
                    if add:
                        newChapters[i] = chapters[i]
                        
                        if website == 'kissmanga':
                            fileName = str(website) + '-' + str(i)
                        else:
                            fileName = str(website) + '-' + str(name) + '-' + str(i)
                        fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
                        fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()
                        loading[fileName] = "True"

                    if mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(i)) == mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersStart'].split('@@@')[0])):
                        add = False
            
            mangaDownloaderThreads.Downloader.setLoading(session['databaseID'] , loading )
            

            flash(f'Download started' , 'success')
            thr = Thread(target=downloadChap, args=[newChapters , website , sauce , name , session['databaseID'] ])
            thr.start()
                
            
            return render_template('manga.html',
                                   placeholder=absurl,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap)
            

        """ DOWNLOAD SINGLE CHAPTER """
        if 'chapter' in request.form:
            chapter = request.form['chapter'].split('@@@')
            chapterName = chapter[0]
            chapterUrl = chapter[1].replace('"', ' ').strip()
            if website == 'kissmanga':
                fileName = str(website) + '-' + str(chapterName)
            else:
                fileName = str(website) + '-' + str(name) + '-' + str(chapterName)
            fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
            fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()

            loading=mangaDownloaderThreads.Downloader.getLoading(session['databaseID'])
            loading[fileName] = "True"
            mangaDownloaderThreads.Downloader.setLoading(session['databaseID'] , loading )

            print(f'---------------------> {fileName}')
            #fileName2=fileName+'[downloading...].pdf'
            #fileName=fileName+'.pdf'
            
            f = open(f'static/downloads/{session["databaseID"]}/downloads.txt' , 'r'  , encoding='utf-8' )
            loading = mangaDownloaderThreads.Downloader.getLoading(session['databaseID'])
            if fileName in f.read() or fileName in loading:
                flash(f'Already Downloaded' , 'error')
                return render_template('manga.html',
                                   placeholder=absurl,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap)
                                   
            flash(f'Download started' , 'success')
            if getMethod() == 'loops':
                thr = Thread(target=mangaDownloaderLoops.Downloader.getPages,
                             args=[
                                 chapterName, website, chapterUrl, sauce, name,
                                 session['databaseID']
                             ])
                thr.start()
            else:
                thr = Thread(target=mangaDownloaderThreads.Downloader.getPages,
                             args=[
                                 chapterName, website, chapterUrl, sauce, name,
                                 session['databaseID']
                             ])
                thr.start()

        #if website != 'nhentai':
        return render_template('manga.html',
                                   placeholder=absurl,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap)


#SUPPORTED WEBSITES
@app.route("/supportedwebsites/")
def supportedwebsites():
    removeFailCount()
    return render_template('supported websites.html')


#CONTACT
@app.route("/contact/")
def contact():
    removeFailCount()
    return render_template('contact.html')


#DOWNLOADS
@app.route("/downloads/")
def downloads():
    removeFailCount()
    addSession()
    return render_template('downloads.html')


#DATABASE DETAILS
@app.route("/database/")
def database():
    removeFailCount()
    text = ''
    dbs = os.listdir('static/downloads')
    for db in dbs:
        if db != 'note':
            text += '----->' + db + '<br>'
            manga = os.listdir(f'static/downloads/{db}')
            for j in manga:
                text += '---------->' + j + '<br>'
    return text

#SESSION DATA
@app.route("/session/")
def sessionCheck():
    temp = ''
    for i in session:
      temp += f'{session[i]} <br>'
    return temp
    


if __name__ == '__main__':
    removeTempFiles()
    #temp=os.system('pip install -r requirements.txt')
    app.run()
