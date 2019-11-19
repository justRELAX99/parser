import requests 
from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Pool

import parser_proxy
import parser_user_agent

from random import choice
from datetime import datetime
import os   
import time
import json

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

def get_music_from_Page(url,style,proxy=None,useragent=None):
    url2='https://zaycev.net'
    all_music=[]
    for j in range(0,1):
        if(j%100==0):
            change_proxy_and_user_agent(proxy,useragent)#меняем прокси и юзер агента каждые 100 страниц
        url=url.replace('index_'+str(j),'index_'+str(j+1))
        try:
            soup=BeautifulSoup(get_html(url,useragent,proxy),'lxml')
        except:
            soup=BeautifulSoup(get_html(url),'lxml')
            change_proxy_and_user_agent(proxy,useragent)
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

def To_File_JSON(all_music):
    all_data=[]
    f=open('your_file.json', 'w', encoding='utf-8')
    for i in all_music:
        data={'name':i[0],'song_name':i[1],'duration':i[2],'downloadURL':i[3],'genre':i[4]}
        all_data.append(data)
    json.dump({'music':all_data},f,indent=4, ensure_ascii=False)

def change_proxy_and_user_agent(proxy,useragent):
    useragents=open('user_agent.txt').read().split('\n')
    proxies=open('proxy_file.txt').read().split('\n')
    new_proxy=choice(proxies)
    new_useragent=choice(useragents)
    proxy['http']=new_proxy
    useragent['User-Agent']=new_useragent


def make_all(page_genre):
    useragents=open('user_agent.txt').read().split('\n')
    proxies=open('proxy_file.txt').read().split('\n')
    proxy={'http':'http://'+choice(proxies)}
    useragent={'User-Agent':choice(useragents)}
    all_music=get_music_from_Page(page_genre[0],page_genre[1],proxy,useragent)#для каждого жанра свой прокси и юзер агент
    return all_music

def create_user_agent_txt():
    user_agents=[]
    html=parser_user_agent.get_html('https://myip.ms/browse/comp_browseragents/1/sort/4#comp_browseragents_tbl_top')
    user_agents=parser_user_agent.get_user_agents(html)
    parser_user_agent.ToFileTXT(user_agents)

def update_proxy_txt():
    driver=webdriver.Chrome('C:\\Users\\justRELAX\\Downloads\\chromedriver_win32\\chromedriver.exe')
    html=parser_proxy.get_html(driver)
    proxys=parser_proxy.get_proxy(html)
    parser_proxy.ToFileTXT(proxys)
    driver.quit()

def main():
    start=datetime.now()
    url='https://zaycev.net/genres'
    html=get_html(url)
    all_pages_genre=get_all_pages_genre(html)
    all_music=[]
    all_music2=[]
    #update_proxy_txt()
    file_path = "user_agent.txt"
    if((os.path.exists(file_path)==False) or (os.stat(file_path).st_size == 0)):
       create_user_agent_txt()
    with Pool(14) as p:
       all_music+=p.map(make_all,all_pages_genre)#? почему то создает список со списками по жанрам
    
    all_music2=[item for sublist in all_music for item in sublist]
    To_File_JSON(all_music2)
    end=datetime.now()
    total=end-start
    print(str(total))

if __name__=='__main__':
    main()