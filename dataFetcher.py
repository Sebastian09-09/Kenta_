import requests
from bs4 import BeautifulSoup
#from urllib.request import Request, urlopen
from PIL import Image
import os


class Fetcher:
    @staticmethod
    def getInfo(website, url, sauce):
        try:
            if website == 'readm.org':
                ext = '/'
            elif website == 'kissmanga':
                ext = '.org/'
            else:
                ext = '.com/'
            header = {
                'User-Agent': 'Mozilla/5.0',
                'Referer': f'https://{website}{ext}'
            }
            if website != 'mangaowl':
                htmlText = requests.get(url, stream=True, headers=header)
                response = htmlText.status_code
                htmlText = htmlText.text
            '''
			else:
				r=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
				x=urlopen(r)
				htmlText=str(x.read() , 'utf-8')
				response = x.status
			'''
            if response == 200 and website != None:
                #htmlText = htmlText
                soup = BeautifulSoup(htmlText, 'lxml')
                if website == 'kissmanga':
                    name = soup.find(class_='bigChar')
                    desc = soup.find(class_='summary')
                    cover = soup.find(class_='a_center')
                    #chapters = soup.find( class_='barContent episodeList full' )
                    #chapter = chapters.a

                    rawChapters = soup.find(class_='listing listing8515 full')
                    chapters = {}
                    for i in rawChapters:
                        try:
                            chapters[i.a.text.strip(
                            )] = 'https://kissmanga.org' + i.a.attrs['href']
                        except:
                            pass
                    chapters = dict(reversed(list(chapters.items())))

                    return (name.text.strip(), desc.text.strip(), chapters,
                            'https://kissmanga.org' + cover.img.attrs['src'])
                if website == 'readm.org':
                    name = soup.find(class_='page-title')
                    desc = soup.find(class_='series-summary-wrapper')
                    desc = desc.text.split('Genres:')[0].split(
                        'SUMMARY')[1].strip()
                    #chapters = soup.find( class_='ui vertical fluid tabular menu' )
                    #chapter=chapters.a.text.split('-')[0]
                    image = soup.find('img', class_='series-profile-thumb')
                    image = 'https://readm.org' + image.attrs['src']
                    path = r'static/temp'
                    files = os.listdir(path)
                    extent = image.split('.')[-1]
                    location = f"static/temp/{name.text.strip()}.{extent}"
                    if name.text.strip() + '.' + extent not in files:
                        im = Image.open(requests.get(image, stream=True).raw)
                        im.save(location)

                    rawChapters = soup.find_all(class_='item season_start')
                    chapters = {}
                    for i in rawChapters:
                        chapters[i.h6.text.strip(
                        )] = 'https://readm.org' + str(i.a.attrs['href'])
                    chapters = dict(reversed(list(chapters.items())))
                    return (name.text.strip(), desc, chapters, '/' + location)
                if website == 'mangakakalot':
                    name = soup.find('ul', class_='manga-info-text').li.text
                    desc = soup.find(id='noidungm').text.split('summary:')[1]
                    #chapters = soup.find( class_='chapter-list' )
                    #chapter = chapters.div.span.a
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
                    return (name.strip(), desc.strip(), chapters, image)
                if website == 'manganato':
                    name = soup.find(class_='story-info-right').h1.text
                    desc = soup.find(id='panel-story-info-description'
                                     ).text.split('Description :')[1]
                    #chapter = soup.find( 'ul' , class_='row-content-chapter' ).li.a.text.strip()
                    rawChapters = soup.find_all(
                        class_='chapter-name text-nowrap')
                    chapters = {}
                    for i in rawChapters:
                        chapters[i.text.strip()] = str(i.attrs['href'])
                    chapters = dict(reversed(list(chapters.items())))
                    image = soup.find('span',
                                      class_='info-image').img.attrs['src']
                    return (name.strip(), desc.strip(), chapters, image)
                '''
				if website == 'mangaowl':
					#print(soup)
					name = soup.find( class_='col-xs-12 col-md-8 single-right-grid-right' )
					desc = soup.find( class_='single-right-grids description' )
					chapter = soup.find( 'li' , class_='list-group-item chapter_list' ).a.label.text.strip()
					image = f'https://image.mostraveller.com/uploads/images/comics/{url.split("https://mangaowl.com/single/")[1].split("/")[0]}/thumbnail.png'
					return(str(name).split('h2')[1].split('</i>')[1].rstrip('</').strip()  , str(desc).split('</span>')[1].rstrip('</div>').strip() , chapter , image)
				'''
                if website == 'nhentai':
                    name = soup.find('title').text.split(
                        '- Comic | nHentai')[0].strip()
                    if 'Ongoing' in name:
                        name = name.rstrip('(Ongoing)')
                    if name == '':
                        raise AssertionError()
                    #desc=None
                    #chapter=None
                    image = f'https://cdn.nhentai.com/nhe/storage/comics/{sauce}.jpg'
                    r = requests.get(image)
                    if r.status_code != 200:
                        image = f'https://cdn.nhentai.com/nhe/storage/comics/{sauce}.png'
                        r = requests.get(image)
                        if r.status_code != 200: raise AssertionError()

                    return (name, image)
            else:
                return ('<!Failed!>', )

        except:
            return ('<!Failed!>', )


#details=Fetcher.getInfo('manganato' , 'https://mangaowl.com/single/71513/brave-star-romantics' , None)
#print(details)
