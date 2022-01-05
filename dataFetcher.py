import requests
from bs4 import BeautifulSoup
#from urllib.request import Request, urlopen
from PIL import Image
import os
from tools import Tools

class Fetcher:
    @staticmethod
    def getInfo(website, url):
        try:
            urlObj = Tools(url)
            stored,name,desc,chapters,image,currentPage,pages=urlObj.checkurlInfo()
            if stored:
                if website == 'webtoon':
                    return(name,desc,chapters,image,currentPage,pages,'stored')
                return(name,desc,chapters,image,'stored')
            else:
                response , htmlText = urlObj.getHTML()
                if response == 200 and website != None:
                    soup = BeautifulSoup(htmlText, 'lxml')
                    if website == 'kissmanga':
                        name = soup.find(class_='bigChar')
                        desc = soup.find(class_='summary')
                        cover = soup.find(class_='a_center')

                        rawChapters = soup.find(class_='listing listing8515 full')
                        chapters = {}
                        for i in rawChapters:
                            try:
                                chapters[i.a.text.strip(
                                )] = 'https://kissmanga.org' + i.a.attrs['href']
                            except:
                                pass
                        chapters = dict(reversed(list(chapters.items())))
                        urlObj.addtourlInfo(name.text.strip() , desc.text.strip() , chapters , 'https://kissmanga.org' + cover.img.attrs['src'] )
                        return (name.text.strip(), desc.text.strip(), chapters,
                                'https://kissmanga.org' + cover.img.attrs['src'] , 'newReq')
                    
                    elif website == 'readm.org':
                        name = soup.find(class_='page-title')
                        desc = soup.find(class_='series-summary-wrapper')
                        desc = desc.text.split('Genres:')[0].split(
                            'SUMMARY')[1].strip()
                        image = soup.find('img', class_='series-profile-thumb')
                        image = 'https://readm.org' + image.attrs['src']
                        path = r'static/temp'
                        files = os.listdir(path)
                        extent = image.split('.')[-1]
                        location = f"static/temp/{name.text.strip()}.{extent}"
                        if name.text.strip() + '.' + extent not in files:
                            r = requests.get(image, stream=True).raw
                            im = Image.open(r)
                            nim = im.convert('RGB')
                            nim.save(location)

                        rawChapters = soup.find_all(class_='item season_start')
                        chapters = {}
                        for i in rawChapters:
                            chapters[i.h6.text.strip(
                            )] = 'https://readm.org' + str(i.a.attrs['href'])
                        chapters = dict(reversed(list(chapters.items())))
                        urlObj.addtourlInfo(name.text.strip(), desc, chapters, '/' + location)
                        return (name.text.strip(), desc, chapters, '/' + location , 'newReq')
                    
                    elif website == 'mangakakalot':
                        #checking for redirect 
                        body = soup.find('body').text
                        if 'REDIRECT :' in body:
                            redirectedURL = body.split('REDIRECT :')[1].strip()
                            rurlObj = Tools(redirectedURL);response , htmlText = rurlObj.getHTML()
                            del rurlObj #Delete Redirect Url Object 
                            soup = BeautifulSoup(htmlText, 'lxml')

                        name = soup.find('ul', class_='manga-info-text').li.h1.text
                        desc = soup.find(id='noidungm').text.split('summary:')[1]
                        rawChapters = soup.find_all(class_='row')
                        chapters = {}
                        for i in rawChapters:
                            href = str(i.span.a).split('href=')[-1].split(
                                'title=')[0].strip('"')
                            chapters[i.span.text.strip()] = href
                        chapters = dict(reversed(list(chapters.items())))
                        if 'Chapter name' in chapters:
                            chapters.pop('Chapter name')
                        cover = soup.find(class_='manga-info-pic')
                        image = cover.img.attrs['src']
                        urlObj.addtourlInfo(name.strip(), desc.strip(), chapters, image)
                        return (name.strip(), desc.strip(), chapters, image , 'newReq')

                    elif website == 'manganato':
                        name = soup.find(class_='story-info-right').h1.text
                        desc = soup.find(id='panel-story-info-description').text.split('Description :')[1]
                        rawChapters = soup.find_all(class_='chapter-name text-nowrap')
                        chapters = {}
                        for i in rawChapters:
                            chapters[i.text.strip()] = str(i.attrs['href'])
                        chapters = dict(reversed(list(chapters.items())))
                        image = soup.find('span',class_='info-image').img.attrs['src']
                        urlObj.addtourlInfo(name.strip(), desc.strip(), chapters, image)
                        return (name.strip(), desc.strip(), chapters, image , 'newReq')
                    
                    elif website == 'mangabat':
                        name = soup.find(class_='story-info-right').h1.text
                        splitAt = soup.find(id='panel-story-info-description').h3.text.strip()
                        desc = soup.find(id='panel-story-info-description').text.split(splitAt)[1]
                        rawChapters = soup.find_all(class_='chapter-name text-nowrap')
                        chapters = {}
                        for i in rawChapters:
                            chapters[i.text.strip()] = str(i.attrs['href'])
                        chapters = dict(reversed(list(chapters.items())))
                        image = soup.find('span', class_='info-image').img.attrs['src']
                        urlObj.addtourlInfo(name.strip(), desc.strip(), chapters , image)
                        return (name.strip(), desc.strip(), chapters , image , 'newReq')
                        

                    elif website == 'mangaread.org':
                        name = soup.find(class_='post-title').h1.text
                        desc = soup.find(class_ = 'summary__content').text
                        rawChapters = soup.find_all(class_='wp-manga-chapter')
                        chapters = {}
                        for i in rawChapters:
                            chapters[i.a.text.strip()] = str(i.a.attrs['href'])
                        chapters = dict(reversed(list(chapters.items())))
                        image = soup.find(class_='summary_image').img.attrs['data-src']
                        urlObj.addtourlInfo(name.strip() , desc.strip() , chapters , image)
                        return (name.strip() , desc.strip() , chapters , image , 'newReq')

                    elif website == 'webtoon':
                        try:
                            name = soup.find('h1' , class_='subj').text
                        except:
                            name = soup.find('h3' , class_='subj').text
                        desc = soup.find('p' , class_='summary').text
                        try:
                            image = str(soup.find(class_='detail_body')["style"])
                            image = image.split('(')[1].split(')')[0]
                        except:
                            image = soup.find('span',class_='thmb').img.attrs['src']
                        extent = image.split('.')[-1]
                        if '?' in extent:
                            extent = extent.split('?')[0]
                        location = f"static/temp/{name.strip()}.{extent}"
                        path = r'static/temp'
                        files = os.listdir(path)
                        if name.strip() + '.' + extent not in files:
                            r = requests.get(image , headers={'Referer':url} , stream=True).raw
                            im = Image.open(r)
                            nim = im.convert('RGB')
                            nim.save(location)
                        chapters = {}
                        
                        rawChapters = soup.find(id='_listUl')
                        for i in rawChapters.find_all('li'):
                            chapters[i.find('span' , class_='subj').span.text.strip()] = i.a.attrs['href']
                        
                        chapters = dict(reversed(list(chapters.items())))

                        paginate = soup.find(class_='paginate')
                        currentPage = paginate.find('span' , class_='on').text
                        pages = []
                        for i in paginate:
                            if i.text.isnumeric() or i.text == 'Next Page' or i.text == 'Previous Episode':
                                if i.text == 'Next Page':
                                    pages.append('>')
                                elif i.text == 'Previous Episode':
                                    pages.append('<')
                                else:
                                    pages.append(i.text)
                        urlObj.addtourlInfo(name.strip() , desc.strip() , chapters , '/'+location , currentPage , pages)
                        return (name.strip() , desc.strip() , chapters , '/'+location , currentPage ,pages  , 'newReq' )

                else:
                    return ('<!Failed!>', )

            del urlObj #Delete Url Object 

        except:
            return ('<!Failed!>', )

#details=Fetcher.getInfo('manganato' , 'https://mangaowl.com/single/71513/brave-star-romantics' , None)
#print(details)