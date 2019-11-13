import requests
import json
from bs4 import BeautifulSoup
from random import choice
from multiprocessing import Pool


def get_html(url,useragent=None,proxy=None):
    response = requests.get(url,headers=useragent,proxies=proxy)
    return response.text

def get_all_pages_genre(html):
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

def get_music_fromPage(url,style,proxy=None,useragent=None):
    url2='https://zaycev.net'
    all_music=[]
    for j in range(0,1):
        url=url.replace('index_'+str(j),'index_'+str(j+1))
        try:
            soup=BeautifulSoup(get_html(url,useragent,proxy),'lxml')
        except:
            soup=BeautifulSoup(get_html(url),'lxml')
        count=soup.find(class_='pager__page pager__page_current').text
        if(count=='1')and(j!=0):#если дошли до первой страницы,то выходим
            break
        songsOnPage=soup.find(class_='musicset-track-list__items').findAll(class_='musicset-track clearfix')
        for i in songsOnPage:
            try:
                name=i.find(class_='musicset-track__title track-geo__title').find(class_='musicset-track__fullname').find(class_='musicset-track__artist').find('a').text.strip()
                song_name=i.find(class_='musicset-track__title track-geo__title').find(class_='musicset-track__fullname').find(class_='musicset-track__track-name').find('a').text.strip()
                duration=i.find(class_='musicset-track__duration').text.strip()
                downloadURL=i.find(class_='musicset-track__download track-geo').find('a').get('href').strip()
                downloadURL=url2+downloadURL
                all_music.append([name,song_name,duration,downloadURL,style])
            except:
                continue
    return all_music

def ToFileJSON(all_music):
    all_data=[]
    f=open('your_file.json', 'a', encoding='utf-8')
    for i in all_music:
        data={'name':i[0],'song_name':i[1],'duration':i[2],'downloadURL':i[3],'genre':i[4]}
        all_data.append(data)
    json.dump({'music':all_data},f,indent=4, ensure_ascii=False)
    f.close()

def make_all(page_genre):
    useragents=open('user_agent.txt').read().split('\n')
    proxies=open('proxy_file.txt').read().split('\n')
    proxy={'http':'http://'+choice(proxies)}
    useragent={'User-Agent':choice(useragents)}
    return get_music_fromPage(page_genre[0],page_genre[1],proxy,useragent)

def main():

    f=open('your_file.json', 'w', encoding='utf-8')#? для очистки файла(на время)
    f.close()

    url='https://zaycev.net/genres'
    all_pages_genre=get_all_pages_genre(get_html(url))
    all_music=[]
    all_music2=[]
    with Pool(14) as p:
        all_music+=p.map(make_all,all_pages_genre)

    for i in all_music:
        all_music2+=i
    
    ToFileJSON(all_music2)

if __name__=='__main__':
    main()