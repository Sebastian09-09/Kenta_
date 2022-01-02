from flask import Flask, render_template, request, redirect, url_for, flash, session , send_from_directory
import dataFetcher
import mangaDownloaderThreads
import time

app = Flask(__name__)
import os
import shutil
from threading import Thread

import random
import string

#SETTINGS
app.config.update(SECRET_KEY="os.environ['SECRET_KEY']",
                  SESSION_COOKIE_SECURE=True,
                  REMEMBER_COOKIE_SECURE=True,
                  SESSION_COOKIE_HTTPONLY=True,
                  REMEMBER_COOKIE_HTTPONLY=True)

#SEE DOWNLOADS
def seeDownloads(dbid):
    downloads_ = os.listdir(f'static/downloads/{dbid}')
    downloadsList = list(filter(lambda x: x.endswith('.pdf'), downloads_))
    loading = mangaDownloaderThreads.Downloader.getLoading(dbid , 'all')
    for i in downloadsList:
        temp = mangaDownloaderThreads.Downloader.clearName(mangaDownloaderThreads.Downloader.hardClearName(i.split('.pdf')[0]))
        if temp in loading:
            del loading[temp]
    newLoading = []
    item = ''
    for i in loading:
        for j in i:
            if j.islower():
                item += j
            else:
                item += ' '+j
        newLoading.append(item);item = ''
    
    return downloadsList , newLoading

#ARC SERVER
@app.route("/arc-sw.js")
def arc():
	return send_from_directory(directory='',path='arc-sw.js',mimetype='application/javascript')

#REMOVE NUMBER OF TRIES
def removeFailCount():
    if 'failCount' in session:
        del session['failCount']
    
#WEBTOON PAGINATION 
def getWebToonPage(url,info , website):
    if website == 'webtoon':
        page = info[4]
        pages = info[5]
        if '&' in url:
            baseUrl = url.split('&')[0]
        else:
            baseUrl = url
        links = {}
        for i in pages:
            if i == '>':
                links[i] = (baseUrl+'&page='+str( int(pages[pages.index(i)-1])+1))
            elif i == '<':
                links[i] = (baseUrl+'&page='+str( int(pages[pages.index(i)+1])-1))
            else:
                links[i] = (baseUrl+'&page='+i)
        
        return page , pages , links
    else:
        return 0 , [] , []


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



#RANDOM loadingID FOR LOADING.JSON
def getFilename(dbid):
    toCheckFrom = []
    loadingID = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
    files = os.listdir(f'static/downloads/{dbid}')
    for i in files:
        if i.startswith('loading'):
            toCheckFrom.append(i[7:12])
    while loadingID in toCheckFrom:
        loadingID = str(''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))

    return loadingID
    


    

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
        session['databaseID'] = db
    else:
        dbid = session['databaseID']
        dbs = os.listdir('static/downloads')
        if str(dbid) not in dbs:
            os.mkdir(f'static/downloads/{dbid}')
            with open(f'static/downloads/{dbid}/downloads.txt' , 'w' , encoding='utf-8'):
                pass


#HOME
@app.route("/")
def home():
    removeFailCount()
    return render_template('index.html')



#DOWNLOAD Multiple Chapters
def downloadChap(chapters , website , sauce , name , dbid  , loadingID):
    for chapter in chapters:
        chapterName = chapter
        chapterUrl = chapters[chapter]
        if website == 'kissmanga':
            fileName = str(website) + '-' + str(chapterName)
        else:
            fileName = str(website) + '-' + str(name) + '-' + str(chapterName)
        fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
        fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()

        f = open(f'static/downloads/{dbid}/downloads.txt' , 'r'  , encoding='utf-8' )
        loading = mangaDownloaderThreads.Downloader.getLoading(dbid , f'except{loadingID}')
        if fileName in f.read() or fileName in loading:
            time.sleep(0.01)
        else:
            mangaDownloaderThreads.Downloader.getPages(chapterName, website, chapterUrl, sauce, name, dbid , loadingID)
            
                

#MANGA
@app.route("/manga/", defaults={'url': ' '}, methods=["GET", "POST"])
@app.route("/manga/<url>/", methods=["GET", "POST"])
def manga(url):
    addSession()
    if request.method == "GET":
        return render_template('manga.html', placeholder="url", desc='Fetch')
    else:
        sauce = None #nhentai is no more supported 
        url = request.form['url']
        if url == '' or not url.startswith('http'):
            flash(f'Please provide a URL', 'warning')
            return redirect(url_for('manga'))
        website = 'kissmanga' if 'kissmanga.org' in url else 'mangakakalot' if 'mangakakalot.com' in url else 'manganato' if 'manganato.com' in url else 'mangaread.org' if 'mangaread.org' in url else 'readm.org' if 'readm.org' in url else 'webtoon' if 'webtoons.com' in url else None
        if website == None:
            flash(f'This Website is not supported!', 'error')
            return redirect(url_for('manga'))
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
        desc = info[1];chapters = info[2];cover = info[3]
        try:
          firstChap = list(chapters.keys())[-1]
        except:
          firstChap = 'None'

        """ DOWNLOAD ALL CHAPTERS """
        if 'downloadAllChapters' in request.form:
            loadingID = getFilename(session['databaseID'])
            with open(f'static/downloads/{session["databaseID"]}/loading{loadingID}.json' , 'w'  , encoding='utf-8') as f:
                f.write('{}')
            loadingCheck = mangaDownloaderThreads.Downloader.getLoading(session['databaseID'] , f'except{loadingID}' )
            loading=mangaDownloaderThreads.Downloader.getLoading(session['databaseID'] , loadingID)
            f = open(f'static/downloads/{session["databaseID"]}/downloads.txt' , 'r'  , encoding='utf-8' )
            fread = f.read();f.close()
            for i in chapters:
                if website == 'kissmanga':
                    fileName = str(website) + '-' + str(i)
                else:
                    fileName = str(website) + '-' + str(name) + '-' + str(i)
                fileName=mangaDownloaderThreads.Downloader.clearName(fileName).strip()
                fileName=mangaDownloaderThreads.Downloader.hardClearName(fileName).strip()
                if fileName in fread or fileName in loadingCheck:
                    pass
                else:
                    loading[fileName] = "True"
            mangaDownloaderThreads.Downloader.setLoading(session['databaseID'] , loading , loadingID)
            if len(loading) != 0:
                flash(f'Download started' , 'success')
                thr = Thread(target=downloadChap, args=[chapters , website , sauce , name , session['databaseID'] , loadingID ])
                thr.start()
            else:
                flash('Already Downloaded' , 'error')
                os.remove(f'static/downloads/{session["databaseID"]}/loading{loadingID}.json')
            
            page,pages,links=getWebToonPage(url,info , website)

            return render_template('manga.html',
                                   placeholder=url,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap , 
                                   page=page,
                                   pages=pages,
                                   links=links)

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

            loadingID = getFilename(session['databaseID'])
            with open(f'static/downloads/{session["databaseID"]}/loading{loadingID}.json' , 'w'  , encoding='utf-8') as f:
                f.write('{}')

            loadingCheck = mangaDownloaderThreads.Downloader.getLoading(session['databaseID'] , f'except{loadingID}' )
            loading=mangaDownloaderThreads.Downloader.getLoading(session['databaseID'] , loadingID )
            
            
            f = open(f'static/downloads/{session["databaseID"]}/downloads.txt' , 'r'  , encoding='utf-8' )
            fread = f.read();f.close()
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
                        if fileName in fread or fileName in loadingCheck:
                            pass
                        else:
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
                        if fileName in fread or fileName in loadingCheck:
                            pass
                        else:
                            loading[fileName] = "True"

                    if mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(i)) == mangaDownloaderThreads.Downloader.hardClearName(mangaDownloaderThreads.Downloader.clearName(request.form['multipleChaptersStart'].split('@@@')[0])):
                        add = False
            
            mangaDownloaderThreads.Downloader.setLoading(session['databaseID'] , loading , loadingID )
            
            if len(loading) != 0:
                flash(f'Download started' , 'success')
                thr = Thread(target=downloadChap, args=[newChapters , website , sauce , name , session['databaseID'] , loadingID ])
                thr.start()
            else:
                flash(f'Already Downloaded' , 'error')
                os.remove(f'static/downloads/{session["databaseID"]}/loading{loadingID}.json')
                
            page,pages,links=getWebToonPage(url,info , website)
            return render_template('manga.html',
                                   placeholder=url,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap,
                                   page=page,
                                   pages=pages,
                                   links=links)
            

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
            
            f = open(f'static/downloads/{session["databaseID"]}/downloads.txt' , 'r'  , encoding='utf-8' )
            fread = f.read();f.close()
            loading = mangaDownloaderThreads.Downloader.getLoading(session['databaseID'] , 'all' )
            if fileName in fread or fileName in loading:
                flash(f'Already Downloaded' , 'error')
                page,pages,links=getWebToonPage(url,info , website)
                return render_template('manga.html',
                                   placeholder=url,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap,
                                   page=page,
                                   pages=pages,
                                   links=links)

            loadingID=getFilename(session['databaseID'])
            with open(f'static/downloads/{session["databaseID"]}/loading{loadingID}.json' , 'w'  , encoding='utf-8') as f:
                f.write('{}')
            
            loading=mangaDownloaderThreads.Downloader.getLoading(session['databaseID'] , loadingID)
            loading[fileName] = "True"
            mangaDownloaderThreads.Downloader.setLoading(session['databaseID'] , loading , loadingID )
                                   
            flash(f'Download started' , 'success') 
            thr = Thread(target=mangaDownloaderThreads.Downloader.getPages,
                             args=[
                                 chapterName, website, chapterUrl, sauce, name,
                                 session['databaseID'] , loadingID
                             ])
            thr.start()
        
        page,pages,links=getWebToonPage(url,info , website)

        return render_template('manga.html',
                                   placeholder=url,
                                   desc='Start',
                                   website=website,
                                   name=name,
                                   description=desc,
                                   chapters=chapters,
                                   cover=cover,
                                   firstChap=firstChap,
                                   page=page,
                                   pages=pages,
                                   links=links)


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
    downloadsList,newLoading=seeDownloads(session['databaseID'])
    return render_template('downloads.html' , downloads_=downloadsList , loading=newLoading)


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
    
@app.route('/downloads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    addSession()
    removeFailCount()
    return send_from_directory(directory=f'static/downloads/{session["databaseID"]}/', path=f'{filename}')

if __name__ == '__main__':
    removeTempFiles()
    #temp=os.system('pip install -r requirements.txt')
    app.run()