import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import pool

def get_html(url):
    response=requests.get(url)
    return response.text

def get_all_page_genre(html):
    url='https://zaycev.net'
    soup=BeautifulSoup(html,'lxml')
    lists=soup.find('ul',class_='genre__filter clearfix unstyled-list').findAll('li',class_='genre__filter-el')
    pages=[]
    for l in lists:
        a=l.find('a')
        if(a!=None):
            a=l.find('a').get('href')
            a=a.replace('.html','_1.html')
            style=l.find('a').text.strip()
        else:continue
        pages.append([url+a,style])
    return pages

def get_music_fromPage(url,style):
    url2='https://zaycev.net'
    musics=[]
    for j in range(0,1):
        url=url.replace('_'+str(j),'_'+str(j+1))
        soup=BeautifulSoup(get_html(url),'lxml')
        count=soup.find(class_='pager__page pager__page_current').text
        if(count=='1')and(j!=0):
            break
        songsOnPage=soup.find(class_='musicset-track-list__items').findAll(class_='musicset-track clearfix')
        for i in songsOnPage:
            try:
                name=i.find(class_='musicset-track__title track-geo__title').find(class_='musicset-track__fullname').find(class_='musicset-track__artist').find('a').text.strip()
                song_name=i.find(class_='musicset-track__title track-geo__title').find(class_='musicset-track__fullname').find(class_='musicset-track__track-name').find('a').text.strip()
                duration=i.find(class_='musicset-track__duration').text
                downloadURL=i.find(class_='musicset-track__download track-geo').find('a').get('href')
                downloadURL=url2+downloadURL
                musics.append([name,song_name,duration,downloadURL,style])
            except:
                continue
    return musics



def ToFileJSON(all_music):
    all_data=[]
    f=open('your_file.json', 'w', encoding='utf-8')
    for i in all_music:
        data={'name':i[0],'song_name':i[1],'duration':i[2],'downloadURL':i[3],'genre':i[4]}
        all_data.append(data)
    json.dump({'music':all_data},f,indent=4, ensure_ascii=False)
    f.close()


def main():
    start=datetime.now()

    all_music=[]
    url='https://zaycev.net/genres'
    all_page_genre=get_all_page_genre(get_html(url))
    
    all_music=get_music_fromPage(all_page_genre[14][0],all_page_genre[14][1])
    ToFileJSON(all_music)

    end=datetime.now()
    total=end-start
    print(str(total))

if __name__=='__main__':
    main()