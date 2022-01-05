import requests
class Tools:

    urlInfo = {}

    def __init__(self , url):
        self.url = url

    def getWebsite(self):
        url = self.url
        website = 'kissmanga' if 'kissmanga.org' in url \
            else 'mangakakalot' if 'mangakakalot.com' in url \
            else 'manganato' if 'manganato.com' in url \
            else 'mangaread.org' if 'mangaread.org' in url \
            else 'readm.org' if 'readm.org' in url \
            else 'webtoon' if 'webtoons.com' in url \
            else 'mangabat' if 'mangabat.com' in url \
            else None
        return website
            #else 'webtoon.uk' if 'webtoon.uk' in url \
            #else 'mangasy' if 'mangasy.com' in url \
            #else 'readlightnovel' if 'readlightnovel.me' in url \
            #else 'wuxiaworld' if 'wuxiaworld.name' in url \
            #else 'zinmanhwa' if 'zinmanhwa.com' in url \
            

    def getabsurl(self):
        website = self.getWebsite()
        if website == 'kissmanga':
            url = str(self.url)
            absurl = url
            url=url.split('/')
            for i in url:
                if i.startswith('manga-'):
                    absurl = f'https://kissmanga.org/manga/{i}/'
            return absurl

        elif website == 'mangakakalot':
            url = str(self.url)
            absurl = url
            url=url.split('/')
            if 'chapter' in url:
                mangaID = url[4]
                absurl = f'https://mangakakalot.com/manga/{mangaID}'
            return absurl
        
        elif website == 'manganato':
            url = str(self.url)
            absurl = url
            url=url.split('/')
            for i in url:
                if i.startswith('manga-'):
                    absurl = f'https://readmanganato.com/{i}/'
            return absurl
        
        elif website == 'mangaread.org':
            url = str(self.url)
            absurl = url
            url=url.split('/')
            for i in url:
                if i.startswith('chapter-'):
                    url.remove(i)
                    absurl = '/'.join(url)
            return absurl

        elif website == 'readm.org':
            url = str(self.url)
            absurl = url
            url=url.split('/')
            if len(url) > 4:
                mangaID = url[4]
                absurl = f'https://readm.org/manga/{mangaID}/'
            return absurl

        elif website == 'webtoon':
            url = str(self.url)
            absurl = url
            if 'viewer?' in url:
                url=url.split('/')
                lan = url[3]
                genre = url[4]
                name = url[5]
                mangaID = url[7].split('viewer?')[-1].split('&')[0].split('=')[-1]
                absurl = f'https://www.webtoons.com/{lan}/{genre}/{name}/list?title_no={mangaID}'
            return absurl
        
        elif website == 'mangabat':
            url = str(self.url)
            absurl = url
            if '-chap-' in url:
                absurl = url.split('-chap-')[0]
            return absurl

        elif website == 'zinmanhwa':
            url = str(self.url)
            absurl = url
            url = url.split('/')
            if len(url) > 4:
                mangaID = url[4]
                absurl = f'https://zinmanhwa.com/manga/{mangaID}'
            return absurl

    def getReferer(self):
        website = self.getWebsite()
        referer = 'https://kissmanga.org/' if website == 'kissmanga' \
            else 'https://mangakakalot.com/' if website == 'mangakakalot' \
            else 'https://manganato.com/' if website == 'manganato' \
            else 'https://readm.org/' if website == 'readm.org' \
            else 'https://mangaread.org/' if website == 'mangaread.org' \
            else  'https://webtoon.com/' if website == 'webtoon' \
            else  'https://read.mangabat.com/' if website == 'mangabat' \
            else None
        return referer

    def addtourlInfo(self , name , desc, chapters , image , currentPage=None , pages=None):
        website = self.getWebsite()
        if website == 'webtoon':
            self.urlInfo[str(self.url)] = [name,desc,chapters,image,currentPage,pages]
        else:
            self.urlInfo[str(self.url)] = [name,desc,chapters,image]

    def checkurlInfo(self):
        if str(self.url)  in self.urlInfo:
            website = self.getWebsite()
            if website == 'webtoon':
                return True , self.urlInfo[str(self.url)][0] , self.urlInfo[str(self.url)][1] , self.urlInfo[str(self.url)][2] , self.urlInfo[str(self.url)][3] , self.urlInfo[str(self.url)][4] , self.urlInfo[str(self.url)][5]
            return True , self.urlInfo[str(self.url)][0] , self.urlInfo[str(self.url)][1] , self.urlInfo[str(self.url)][2] , self.urlInfo[str(self.url)][3] , None , None
        else:
            return False, None , None , None , None , None , None

    def removefromurlInfo(self):
        try:
            del self.urlInfo[str(self.url)]
        except:
            pass

    def getHTML(self):
        referer = self.getReferer()
        header = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': f'https://{referer}'
        }
        htmlText = requests.get(self.url , stream=True, headers=header)
        response = htmlText.status_code
        htmlText = htmlText.text
        return response , htmlText