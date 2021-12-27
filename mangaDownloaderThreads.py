import requests
import threading
import time
from bs4 import BeautifulSoup
from requests.sessions import session
import dataFetcher
import urllib.parse
from PIL import Image
from io import BytesIO
import os


class Downloader:
    @staticmethod
    def getPages(name, website, url, sauce, fullName, databaseID):
        Downloader.createManga(name , website , fullName , databaseID , True)
        #print(url)
        pages = {}

        referer = 'https://kissmanga.org' if website == 'kissmanga' else 'https://mangakakalot.com' if website == 'mangakakalot' else 'https://manganato.com' if website == 'manganato' else 'https://cdn.nhentai.com' if website == 'nhentai' else 'https://readm.org' if website == 'readm.org' else None
        header = {'User-Agent': 'Mozilla/5.0', 'Referer': f'https://{referer}'}
        htmlText = requests.get(url, stream=True, headers=header)
        response = htmlText.status_code
        htmlText = htmlText.text
        if response == 200 and website != None:
            soup = BeautifulSoup(htmlText, 'lxml')

            if website == 'kissmanga':
                pages_ = soup.find(id='centerDivVideo')
                index = 0
                for i in pages_:
                    try:
                        pages[index] = i.attrs['src']
                        index += 1
                    except:
                        pass
                pagesData = Downloader.getBin(pages, referer)
                Downloader.toPdf(name, pages, pagesData, website, fullName,
                                 databaseID)
                Downloader.createManga(name , website , fullName , databaseID , False)

            if website == 'mangakakalot':
                pages_ = str(soup.find(class_='container-chapter-reader'))
                tempPages = pages_.strip().split('<img ')
                index = 0
                for i in tempPages:
                    if i != '' and 'src=' in i:
                        for j in i.split(' '):
                            if 'src=' in j:
                                pages[index] = j.strip('src=').strip('"')
                                index += 1
                                break
                pagesData = Downloader.getBin(pages, referer)
                Downloader.toPdf(name, pages, pagesData, website, fullName,
                                 databaseID)
                Downloader.createManga(name , website , fullName , databaseID , False)

            if website == 'manganato':

                pages_ = str(soup.find(class_='container-chapter-reader'))
                tempPages = pages_.strip().split('<img ')
                index = 0
                for i in tempPages:
                    if i != '' and 'src=' in i:
                        for j in i.split(' '):
                            if 'src=' in j:
                                pages[index] = j.strip('src=').strip('"')
                                index += 1
                                break
                pagesData = Downloader.getBin(pages, referer)
                Downloader.toPdf(name, pages, pagesData, website, fullName,
                                 databaseID)
                Downloader.createManga(name , website , fullName , databaseID , False)

            if website == 'nhentai':
                d = {}
                keepRunning = [True]
                killFrom = [0]
                pass_ = [True]
                baseUrl = f'https://cdn.nhentai.com/nhe/storage/images/{sauce}/'

                def get(page):
                    url = baseUrl + f'{page}.jpg'
                    #print(url)
                    header = {
                        'Accept':
                        'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
                        'Accept-Encoding':
                        'gzip, deflate, br',
                        'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                        'Version/13.1.2 Safari/605.1.15',
                        'Accept-Language':
                        'en-ca',
                        'Referer':
                        referer,
                        'Connection':
                        'keep-alive'
                    }

                    r = requests.get(url, headers=header)
                    #print('----------> Page ',  page , '- ', r)
                    if r.status_code == 200:
                        pages[page] = r
                        #print('----------------------->', r, ' for ' , url , ' page ' , page)
                    else:
                        url = baseUrl + f'{page}.png'
                        r = requests.get(url, headers=header)
                        #print('----------> Page ',  page , '- ', r)
                        if r.status_code == 200:
                            pages[page] = r
                            #print('----------------------->', r, ' for ' , url , ' page ' , page)
                        else:
                            keepRunning[0] = False
                            if pass_[0]:
                                killFrom[0] = page
                                pass_[0] = False

                def run():
                    page = 1
                    while keepRunning[0]:
                        #time.sleep(0.3)
                        #print(f'Starting Thread {page}')
                        d['x' + str(page)] = threading.Thread(target=get,
                                                              args=(page, ))
                        d['x' + str(page)].start()
                        page += 1

                run()
                for i in range(1, killFrom[0]):
                    d['x' + str(i)].join()
                    #print(f'Ending Thread {i}')

                for i in range(1, killFrom[0]):
                    if i not in pages:
                        #print('Failed to Fetch page ',i)
                        #print('retrying...')
                        url = baseUrl + f'{i}.jpg'
                        header = {
                            'Accept':
                            'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
                            'Accept-Encoding':
                            'gzip, deflate, br',
                            'User-Agent':
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                            'Version/13.1.2 Safari/605.1.15',
                            'Accept-Language':
                            'en-ca',
                            'Referer':
                            referer,
                            'Connection':
                            'keep-alive'
                        }
                        r = requests.get(url, headers=header)
                        #print('----------> Page ',  i , '- ', r)
                        if r.status_code == 200:
                            pages[i] = r
                            #print('----------------------->', r, ' for ' , url , ' page ' , i)
                        else:
                            url = baseUrl + f'{i}.png'
                            r = requests.get(url, headers=header)
                            if r.status_code == 200:
                                pages[i] = r
                                #print('----------------------->', r, ' for ' , url , ' page ' , i)
                            else:
                                pass
                                #print('Failed!')

                Downloader.toPdf(name, pages, None, website, fullName,
                                 databaseID)
                Downloader.createManga(name , website , fullName , databaseID , False)

            if website == 'readm.org':
                pages_ = soup.find(class_='ch-images ch-image-container')
                images = pages_.find_all('img')
                index = 0
                for i in images:
                    pages[index] = 'https://readm.org' + i.attrs['src']
                    index += 1
                pagesData = Downloader.getBin(pages, referer)
                Downloader.toPdf(name, pages, pagesData, website, fullName,
                                 databaseID)
            Downloader.createManga(name , website , fullName , databaseID , False)

    def toPdf(name, imagesDict, imagesData, website, fullName, dbid):
        if imagesData != None:
            tempIndex = list(imagesDict.keys())
            index = list(map(lambda x: int(x), tempIndex))
            index.sort()

            imageList = []
            for i in index:
                page = imagesDict[i]
                pageData = imagesData[page]
                img = Image.open(BytesIO(pageData.content))
                if i == 0:
                    im1 = img.convert('RGB')
                im = img.convert('RGB')
                if i != 0:
                    imageList.append(im)

            if website == 'kissmanga':
                savedAs = str(website) + '-' + str(name)
                savedAs = Downloader.clearName(savedAs)
                im1.save(f'static/downloads/{dbid}/{savedAs}.pdf',
                         save_all=True,
                         append_images=imageList)
            else:
                savedAs = str(website) + '-' + str(fullName) + '-' + str(name)
                savedAs = Downloader.clearName(savedAs)
                im1.save(f'static/downloads/{dbid}/{savedAs}.pdf',
                         save_all=True,
                         append_images=imageList)
            print(savedAs)

        else:
            name = Downloader.clearName(name)
            tempIndex = list(imagesDict.keys())
            index = list(map(lambda x: int(x), tempIndex))
            index.sort()

            imageList = []
            for i in index:
                img = Image.open(BytesIO(imagesDict[i].content))
                if i == 1:
                    im1 = img.convert('RGB')
                im = img.convert('RGB')
                if i != 1:
                    imageList.append(im)

            im1.save(f'static/downloads/{dbid}/nhentai-{name}.pdf',
                     save_all=True,
                     append_images=imageList)

    def getBin(pages, referer):
        d = {}
        pagesData = {}

        def get(url):
            header = {
                'Accept':
                'image/png,image/svg+xml,image/*;q=0.8,video/*;q=0.8,*/*;q=0.5',
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                'Version/13.1.2 Safari/605.1.15',
                'Accept-Language':
                'en-ca',
                'Referer':
                referer,
                'Connection':
                'keep-alive'
            }
            r = requests.get(url, headers=header)
            if r.status_code == 200:
                pagesData[url] = r
            #print(r, 'for', url)

        def run():
            index = 1
            for i in list(pages.values()):
                #time.sleep(0.1)
                #print(f'Starting thread {index}')
                d['x' + str(index)] = threading.Thread(target=get, args=(i, ))
                d['x' + str(index)].start()
                index += 1

        run()
        for i in range(1, len(pages) + 1):
            d['x' + str(i)].join()
            #print(f'Ending Thread {i}')

        return pagesData

    def createManga(name, website, fullName, dbid , create):
        if create:
            if website == 'kissmanga':
                savedAs = str(website) + '-' + str(name)
            else:
                savedAs = str(website) + '-' + str(fullName) + '-' + str(name)
            savedAs = Downloader.clearName(savedAs)
            with open(f'static/downloads/{dbid}/{savedAs}[downloading...].pdf', 'w') as fp:pass
        else:
            if website == 'kissmanga':
                savedAs = str(website) + '-' + str(name)
            else:
                savedAs = str(website) + '-' + str(fullName) + '-' + str(name)
            savedAs = Downloader.clearName(savedAs)
            try:
                os.remove(f'static/downloads/{dbid}/{savedAs}[downloading...].pdf')
            except:
                pass

            
            
        #print(savedAs)
        #return

    @staticmethod
    def clearName(name):
        newName = ''
        whitespace = 0
        for i in name:
            if i == ' ' and whitespace == 0:
                whitespace = 1
                newName += i
            if i != ' ':
                whitespace = 0
                newName += i
        if "\r" in newName:
            newName = newName.replace("\r", " ")
        if "\n" in newName:
            newName = newName.replace("\n", " ")
        for i in [":", "\\", "/", "|", "*", "<", ">", "?", '"']:
            if i in newName:
                newName = newName.replace(i, "_")
        return (newName)


#x=Downloader.getPages( 'yeah' , 'mangakakalot' ,  'https://mangakakalot.com/chapter/hj918822/chapter_1' , '')
#print(x)
